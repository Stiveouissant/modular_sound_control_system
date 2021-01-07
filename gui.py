# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton, QButtonGroup, QGroupBox, QRadioButton, QComboBox, QInputDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QMessageBox

import database
import stylesheets
from tabmodel import ProfileTabModel


class UIMainWidget(object):

    def setup_ui(self, widget):
        widget.setObjectName("Widget")

        # mode buttons ###
        button_layout_box = QHBoxLayout()
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)
        for v in ('Speech', 'Sound', 'Pitch'):
            self.btn = QPushButton(v)
            self.btn.setStyleSheet("background-color: white")
            self.button_group.addButton(self.btn)
            button_layout_box.addWidget(self.btn)
        # group for recognition mode
        self.button_groupbox = QGroupBox('Recognition mode')
        self.button_groupbox.setLayout(button_layout_box)
        self.button_groupbox.setObjectName('Push')

        # info panel with profile and sound visuals
        self.info_panel = QHBoxLayout()
        self.label1 = QLabel("Profile: not selected", self)
        self.label2 = QLabel("Placeholder for sound visuals", self)
        self.info_panel.addWidget(self.label1)
        self.info_panel.addWidget(self.label2)

        # Activate button
        self.activate_recognition_button = QPushButton("Activate recognition")
        self.activate_recognition_button.setStyleSheet("background-color:lightgrey;")
        self.activate_recognition_button.setCheckable(True)
        self.activate_recognition_button.setDisabled(True)

        # table for data-model-view
        self.view = QTableView()

        # lower buttons ###
        self.select_profile_button = QPushButton("Select Profile")
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.setEnabled(False)
        self.save_changes_button = QPushButton("Save Changes")
        self.save_changes_button.setEnabled(False)

        # lower buttons layout ###
        lower_buttons_layout = QHBoxLayout()
        lower_buttons_layout.addWidget(self.select_profile_button)
        lower_buttons_layout.addWidget(self.add_task_button)
        lower_buttons_layout.addWidget(self.save_changes_button)

        # vertical layout for all elements ###
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.button_groupbox)
        layoutV.addLayout(self.info_panel)
        layoutV.addWidget(self.activate_recognition_button)
        layoutV.addWidget(self.view)
        layoutV.addLayout(lower_buttons_layout)


class ProfileDialog(QDialog):
    """ Select Profile window """

    def __init__(self, parent=None):
        super(ProfileDialog, self).__init__(parent)

        # radio buttons ###
        self.radio_layout = QVBoxLayout()
        for v in database.read_profiles():
            self.radio = QRadioButton(v)
            self.radio_layout.addWidget(self.radio)
        self.radio_layout.itemAt(0).widget().setChecked(True)

        self.lower_buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # main layout ###
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addLayout(self.radio_layout)
        vertical_layout.addWidget(self.lower_buttons)

        # button connects ###
        self.lower_buttons.accepted.connect(self.accept)
        self.lower_buttons.rejected.connect(self.reject)

        # properties ###
        self.setModal(True)  # can't leave the window before closing
        self.setWindowTitle('Select Profile')

    def get_login(self):
        for i in range(self.radio_layout.count()):
            if self.radio_layout.itemAt(i).widget().isChecked():
                return self.radio_layout.itemAt(i).widget().text()

    # creates dialog returns profile name and accept from dialog
    @staticmethod
    def getProfile(parent=None):
        dialog = ProfileDialog(parent)
        ok = dialog.exec_()
        return dialog.get_login(), ok == QDialog.Accepted


class AddTaskDialog(QDialog):
    """ Add new task window """

    def __init__(self, parent=None, mode="Speech"):
        super(AddTaskDialog, self).__init__(parent)

        # labels
        desc_label = QLabel("Description:", self)
        func_label = QLabel("Function:", self)
        trigger_label = QLabel("Trigger:", self)
        bonus_label = QLabel("Bonus data:", self)

        self.desc_line = QLineEdit()

        self.function_list = QComboBox(self)
        for v in ('Open File', 'Run Macro', 'Simulate keyboard press', 'Simulate mouse press'):
            self.function_list.addItem(v)

        self.trigger_list = QComboBox(self)
        for v in ('Say cheese', 'Say rumba', 'Say windows', 'Say mac'):
            self.trigger_list.addItem(v)

        self.bonus_data = QLineEdit()

        self.lower_buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # main layout ###
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(desc_label)
        vertical_layout.addWidget(self.desc_line)
        vertical_layout.addWidget(func_label)
        vertical_layout.addWidget(self.function_list)
        vertical_layout.addWidget(trigger_label)
        vertical_layout.addWidget(self.trigger_list)
        vertical_layout.addWidget(bonus_label)
        vertical_layout.addWidget(self.bonus_data)
        vertical_layout.addWidget(self.lower_buttons)

        # button connects ###
        self.lower_buttons.accepted.connect(self.accept)
        self.lower_buttons.rejected.connect(self.reject)

        # properties ###
        self.setModal(True)  # can't leave the window before closing
        self.setWindowTitle('Add new Task')

    def get_data(self):
        return (self.desc_line.text(),
                str(self.function_list.currentText()),
                str(self.trigger_list.currentText()),
                self.bonus_data)

    @staticmethod
    def get_new_task(parent=None):
        dialog = AddTaskDialog(parent)
        ok = dialog.exec_()
        desc, func, trigger, data = dialog.get_data()
        return desc, func, trigger, data, ok == QDialog.Accepted


class ManageProfilesDialog(QDialog):
    """ Manage Profiles window """
    # view = QTableView()

    def __init__(self, parent=None):
        super(ManageProfilesDialog, self).__init__(parent)

        profiles = database.read_profiles_full()
        fields = ['Id', 'Profile name', 'Delete']
        self.model = ProfileTabModel(fields)
        self.model.update(profiles)
        self.model.layoutChanged.emit()

        self.view = QTableView()
        self.refresh_view()

        horizontal_layout_buttons = QHBoxLayout()
        self.create_profile_button = QPushButton("Create Profile")
        self.save_button = QPushButton("Save changes")
        self.close_button = QPushButton("Close")
        horizontal_layout_buttons.addWidget(self.create_profile_button)
        horizontal_layout_buttons.addWidget(self.save_button)
        horizontal_layout_buttons.addWidget(self.close_button)

        # button connects ###
        self.create_profile_button.clicked.connect(self.create_new_profile)
        self.save_button.clicked.connect(self.save_changes)
        self.close_button.clicked.connect(self.close_dialog)

        # main layout ###
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(self.view)
        vertical_layout.addLayout(horizontal_layout_buttons)

        # properties ###
        self.setModal(True)
        self.setWindowTitle('Manage profiles')

    def create_new_profile(self):
        profilename, ok = QInputDialog.getText(self, 'Creating profile', 'Type in a name for the profile')
        if not ok:
            return
        elif not profilename.strip():
            QMessageBox.critical(self, 'Error', 'Profile name cannot be empty!', QMessageBox.Ok)
            return
        else:
            profile = database.add_profile(profilename)
            self.model.table.append(profile)
            self.model.layoutChanged.emit()
            if len(self.model.table) == 1:
                self.refresh_view()

    def save_changes(self):
        database.save_profiles(self.model.table)
        self.model.layoutChanged.emit()

    def close_dialog(self):
        self.close()

    def refresh_view(self):
        self.view.setModel(self.model)
        self.view.hideColumn(0)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.resizeColumnsToContents()

    @staticmethod
    def manage_profiles(parent=None):
        dialog = ManageProfilesDialog(parent)
        dialog.exec_()
        return


class SettingsDialog(QDialog):
    """ Settings window """

    def __init__(self, parent=None, mic_list=[]):
        super(SettingsDialog, self).__init__(parent)

        mic_label = QLabel("Recording devices:", self)

        # Microphone change combo box ###
        self.devices_list = QComboBox(self)
        self.devices_list.addItem('Default', -1)
        for v in mic_list:
            self.devices_list.addItem(v.get('name'), v.get('index'))

        self.lower_buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # main layout ###
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(mic_label)
        vertical_layout.addWidget(self.devices_list)
        vertical_layout.addWidget(self.lower_buttons)

        # button connects ###
        self.lower_buttons.accepted.connect(self.accept)
        self.lower_buttons.rejected.connect(self.reject)

        # properties ###
        self.setModal(True)  # can't leave the window before closing
        self.setWindowTitle('Settings')

    def get_data(self):
        return self.devices_list.currentData()

    # creates dialog returns profile name and accept from dialog
    @staticmethod
    def get_settings(parent=None, mic_list=[]):
        dialog = SettingsDialog(parent, mic_list)
        ok = dialog.exec_()
        return dialog.get_data(), ok == QDialog.Accepted
