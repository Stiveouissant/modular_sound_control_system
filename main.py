from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QAction, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from gui import UIMainWidget, ProfileDialog, AddTaskDialog, ManageProfilesDialog, SettingsDialog
import database
from tabmodel import TabModel
from pitch import PitchRecognition

import pyaudio
import speech_recognition as sr

import stylesheets

import numpy as np


class MainWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # widget settings ###
        self.setWindowTitle("Modular Sound Control System")
        self.resize(500, 300)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self._createActions()
        self._connectActions()
        self._createMenuBar()
        self._createStatusBar()

    def _createMenuBar(self):
        menu_bar = self.menuBar()
        # Creating menu using a QMenu object
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.change_profile_action)
        file_menu.addAction(self.extract_profile_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        settings_menu = QMenu("&Settings", self)
        settings_menu.addAction(self.settings_action)
        help_menu = QMenu("&Help", self)
        help_menu.addAction(self.help_content_action)
        help_menu.addAction(self.about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(settings_menu)
        menu_bar.addMenu(help_menu)

    def _createStatusBar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def _createActions(self):
        self.change_profile_action = QAction("&Manage Profiles", self)
        self.extract_profile_action = QAction("&Import Profile", self)
        self.exit_action = QAction("&Exit", self)
        self.settings_action = QAction("&Settings", self)
        self.help_content_action = QAction("&Help Content", self)
        self.about_action = QAction("&About...", self)

    def _connectActions(self):
        # Connect File actions
        self.change_profile_action.triggered.connect(self.manage_profiles)
        self.extract_profile_action.triggered.connect(self.import_profile)
        self.exit_action.triggered.connect(self.exit_action_triggered)
        # Connect Settings actions
        self.settings_action.triggered.connect(self.settings)
        # Connect Help actions
        self.help_content_action.triggered.connect(self.help_content)
        self.about_action.triggered.connect(self.about)

    def set_temporary_message(self, message):
        self.statusbar.showMessage(message)

    def manage_profiles(self):
        ManageProfilesDialog.manage_profiles()
        self.main_widget.activate_recognition_button.setDisabled(True)
        self.main_widget.add_task_button.setDisabled(True)
        self.main_widget.save_changes_button.setDisabled(True)

    def import_profile(self):
        print("Import Profile")

    def exit_action_triggered(self):
        self.close()

    def settings(self):
        self.main_widget.open_settings_menu()

    def help_content(self):
        print("Help Content")

    def about(self):
        print("About")

    def closeEvent(self, event):

        answer = QMessageBox.question(
            self, 'Closing program',
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


class GraphUpdateThread(QThread):
    signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(GraphUpdateThread, self).__init__(parent=parent)
        self.p = pyaudio.PyAudio()
        self.chunk = 1024
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                  rate=44000, input=True, frames_per_buffer=self.chunk)

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        while self.stream.is_active():
            data = np.frombuffer(self.stream.read(self.chunk), dtype=np.int16)
            data = [-2500 if x < -2500 else 2500 if x > 2500 else x for x in data]
            self.signal.emit(data)


class MainWidget(QWidget, UIMainWidget):
    """Widget that handles the main application"""
    # default recognition mode
    recognition_mode = 'Speech'
    # default microphone
    mic_input_index = -1

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setup_ui(self)

        self.activate_recognition_button.clicked[bool].connect(self.activate_recognition)
        self.select_profile_button.clicked.connect(self.select_profile)
        self.add_task_button.clicked.connect(self.add_task)
        self.save_changes_button.clicked.connect(self.save_changes)

        # mode change PushButtons ###
        for btn in self.button_group.buttons():
            btn.clicked.connect(self.mode_change)
        self.set_active_button_style()

        np.set_printoptions(threshold=np.inf)

        self.p = pyaudio.PyAudio()  # Mic input for visualising audio and pitch recognition
        self.chunk = 1024
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                  rate=44000, input=True, frames_per_buffer=self.chunk)

        # Plot graph setup
        self.graph_thread = GraphUpdateThread()
        self.initialize_graph()

        # # close the stream gracefully
        # self.stream.stop_stream()
        # self.stream.close()

        self.stop = None  # variable for storing stop function for background listening
        self.r = sr.Recognizer()  # recognizer for speech to text
        self.r.energy_threshold = 6000  # higher the value - louder the room
        # r.pause_threshold = 0.4  # how many seconds of silence before processing audio

        # Pitch tracking setup
        self.pitch_tracker = PitchRecognition()
        self.pitch_tracker.signal.connect(self.progress_pitch_data)

    def initialize_graph(self):
        self.graph_thread.start()
        self.graph_thread.signal.connect(self.graph_update)

    def graph_update(self, data):
        self.sound_visual.plot(np.arange(self.chunk), data, clear=True)

    def open_settings_menu(self):
        """ Opens settings menu """
        mics = self.valid_input_devices()
        microphone_index, ok = SettingsDialog.get_settings(mic_list=mics)
        if not ok:
            return
        self.mic_input_index = microphone_index
        if self.stop is not None:
            self.activate_recognition(False)

    # MICROPHONE SETUP ###

    def valid_test(self, device):
        """ Given a device ID and a rate, return TRUE/False if it's valid. """
        try:
            self.mic_info = self.p.get_device_info_by_index(device)
            if self.mic_info["maxInputChannels"] < 1 or self.mic_info["hostApi"] != 0:
                return False
            stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                 input_device_index=device, frames_per_buffer=self.chunk,
                                 rate=int(self.mic_info["defaultSampleRate"]), input=True)
            stream.close()
            return True
        except Exception:
            return False

    def valid_input_devices(self):
        """ See which devices can be opened for microphone input. """
        mics = []
        for device in range(self.p.get_device_count()):
            if self.valid_test(device):
                mics.append({'name': self.mic_info.get('name'), 'index': self.mic_info.get('index')})
        if len(mics) == 0:
            print("no microphone devices found!")
        return mics

    # END OF MICROPHONE SETUP ###

    def activate_recognition(self, activate):
        if activate:
            self.activate_recognition_button.setStyleSheet("background-color:lightblue;")
            if self.recognition_mode == "Speech":
                self.activate_speech_recognition()
            elif self.recognition_mode == "Sound":
                self.activate_sound_recognition()
            else:
                self.activate_pitch_recognition()
        else:
            self.activate_recognition_button.setChecked(False)
            self.activate_recognition_button.setStyleSheet("background-color:lightgrey;")
            if self.recognition_mode == "Speech":
                if self.stop is not None:
                    self.stop(wait_for_stop=False)  # wait_for_stop=False
            elif self.recognition_mode == "Sound":
                self.activate_sound_recognition()
            else:
                self.pitch_tracker.stop_stream()

    def activate_speech_recognition(self):
        window.set_temporary_message("Speech recognition activated")
        if self.mic_input_index == -1:
            mic = sr.Microphone()
        else:
            mic = sr.Microphone(device_index=self.mic_input_index)
        # try recognizing the speech from the mic
        self.stop = self.r.listen_in_background(mic, self.speech_callback)

    @staticmethod
    def speech_callback(recognizer, audio):  # this is called from the background thread
        try:
            speech = recognizer.recognize_sphinx(audio)
            print("You said: " + speech)
            window.set_temporary_message("You said: " + speech)
        except sr.RequestError:
            window.set_temporary_message("There was a problem with Voice Recognizer!")
        except sr.UnknownValueError:
            window.set_temporary_message("Oops! Didn't catch that. Could you repeat, please?")

    def activate_sound_recognition(self):
        print("sound recognition")

    def activate_pitch_recognition(self):
        self.pitch_tracker.start_stream()

    def progress_pitch_data(self, note):
        print(note)

    def mode_change(self):
        which_button = self.sender()
        self.activate_recognition(False)
        self.recognition_mode = which_button.text()
        self.set_active_button_style()

    def set_active_button_style(self):
        for btn in self.button_group.buttons():
            if self.recognition_mode == btn.text():
                btn.setStyleSheet("background-color: lightgreen;")
            else:
                btn.setStyleSheet("background-color: white")

    def save_changes(self):
        """ Saves changes in description, activation and if the task was selected for deletion - deletes it"""
        database.saveData(model.table)
        model.layoutChanged.emit()

    def add_task(self):
        """ Adds new task """
        desc, func, trigger, data, ok = AddTaskDialog.get_new_task()
        if not ok:
            return
        elif not desc.strip():
            QMessageBox.critical(self, 'Error', 'Description cannot be empty!', QMessageBox.Ok)
            return

        if self.recognition_mode == 'Speech':
            trigger_type = 0
        elif self.recognition_mode == 'Sound':
            trigger_type = 1
        else:
            trigger_type = 2
        task = database.add_task(desc, func, trigger, trigger_type, data, self.profile)
        model.table.append(task)
        model.layoutChanged.emit()  # signal that there was a change
        if len(model.table) == 1:  # if this is a first task
            self.refresh_view()     # model needs to be send to view

    def select_profile(self):
        """ From the poll of existing profiles allow user to pick one """
        login, ok = ProfileDialog.getProfile(self)
        if not ok:
            return

        self.profile = database.logon(login)
        if self.profile is None:
            QMessageBox.critical(self, 'Error', 'Could not find the profile!', QMessageBox.Ok)
            return

        tasks = database.read_tasks(self.profile)
        model.update(tasks)
        model.layoutChanged.emit()
        self.info_panel.itemAt(0).widget().setText("Profile: " + login)
        self.refresh_view()

        self.add_task_button.setEnabled(True)
        self.save_changes_button.setEnabled(True)
        self.activate_recognition_button.setEnabled(True)

    def refresh_view(self):
        self.view.setModel(model)  # send data to view
        self.view.hideColumn(0)  # hide id column
        # stretch last column and resize on main window resize
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.resizeColumnsToContents()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    database.connect()
    model = TabModel(database.fields)
    window = MainWindow()
    window.show()
    window.move(350, 200)
    sys.exit(app.exec_())
