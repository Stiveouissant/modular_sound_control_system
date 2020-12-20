import sounddevice
from scipy.io.wavfile import write
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from gui import Ui_Widget


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

    def _createMenuBar(self):
        menu_bar = self.menuBar()
        # Creating menus using a QMenu object
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

    def _createActions(self):
        self.change_profile_action = QAction("&Change Profile", self)
        self.extract_profile_action = QAction("&Extract Profile", self)
        self.exit_action = QAction("&Exit", self)
        self.settings_action = QAction("&Settings", self)
        self.help_content_action = QAction("&Help Content", self)
        self.about_action = QAction("&About...", self)

    def _connectActions(self):
        # Connect File actions
        self.change_profile_action.triggered.connect(self.change_profile)
        self.extract_profile_action.triggered.connect(self.extract_profile)
        self.exit_action.triggered.connect(self.exit_action_triggered)
        # Connect Settings actions
        self.settings_action.triggered.connect(self.settings)
        # Connect Help actions
        self.help_content_action.triggered.connect(self.help_content)
        self.about_action.triggered.connect(self.about)

    def change_profile(self):
        print("Change Profile")

    def extract_profile(self):
        print("Extract Profile")

    def exit_action_triggered(self):
        self.close()

    def settings(self):
        print("Settings")

    def help_content(self):
        print("Help Content")

    def about(self):
        print("About")

    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Info',
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def exit(self):
        self.close()


class MainWidget(QWidget, Ui_Widget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setup_ui(self)

        # self.logujBtn.clicked.connect(self.loguj)
        self.koniecBtn.clicked.connect(self.koniec)
        # self.dodajBtn.clicked.connect(self.dodaj)
        # self.zapiszBtn.clicked.connect(self.zapisz)

    def koniec(self):
        self.close()

    # def zapisz(self):
    #     baza.zapiszDane(model.tabela)
    #     model.layoutChanged.emit()
    #
    # def dodaj(self):
    #     """ Dodawanie nowego zadania """
    #     zadanie, ok = QInputDialog.getMultiLineText(self, 'Zadanie', 'Co jest do zrobienia?')
    #     if not ok or not zadanie.strip():
    #         QMessageBox.critical(self, 'Błąd', 'Zadanie nie może być puste.', QMessageBox.Ok)
    #         return
    #
    #     zadanie = baza.dodajZadanie(self.osoba, zadanie)
    #     model.tabela.append(zadanie)
    #     model.layoutChanged.emit()  # wyemituj sygnał: zaszła zmiana!
    #     if len(model.tabela) == 1:  # jeżeli to pierwsze zadanie
    #         self.odswiezWidok()     # trzeba przekazać model do widoku
    #
    # def loguj(self):
    #     """ Logowanie użytkownika """
    #     login, haslo, ok = LoginDialog.getLoginHaslo(self)
    #     if not ok:
    #         return
    #
    #     if not login or not haslo:
    #         QMessageBox.warning(self, 'Błąd',
    #                             'Pusty login lub hasło!', QMessageBox.Ok)
    #         return
    #
    #     self.osoba = baza.loguj(login, haslo)
    #     if self.osoba is None:
    #         QMessageBox.critical(self, 'Błąd', 'Błędne hasło!', QMessageBox.Ok)
    #         return
    #
    #     QMessageBox.information(self,
    #         'Dane logowania', 'Podano: ' + login + ' ' + haslo, QMessageBox.Ok)
    #
    #     zadania = baza.czytajDane(self.osoba)
    #     model.aktualizuj(zadania)
    #     model.layoutChanged.emit()
    #     self.odswiezWidok()
    #     self.dodajBtn.setEnabled(True)
    #     self.zapiszBtn.setEnabled(True)
    #
    # def odswiezWidok(self):
    #     self.widok.setModel(model)  # przekazanie modelu do widoku
    #     self.widok.hideColumn(0)  # ukrywamy kolumnę id
    #     # ograniczenie szerokości ostatniej kolumny
    #     self.widok.horizontalHeader().setStretchLastSection(True)
    #     # dopasowanie szerokości kolumn do zawartości
    #     self.widok.resizeColumnsToContents()
    #


class Recorder(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):

        # etykiety
        etykieta1 = QLabel("Naciśnij przycisk, aby rozpocząć nagrywanie:", self)


        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)

        # przyciski
        koniecBtn = QPushButton("&Koniec", self)
        recordBtn = QPushButton("&Nagraj", self)
        koniecBtn.resize(koniecBtn.sizeHint())

        ukladH = QHBoxLayout()
        ukladH.addWidget(recordBtn)

        ukladT.addLayout(ukladH, 2, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 3, 0, 1, 3)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)

        koniecBtn.clicked.connect(self.koniec)
        recordBtn.clicked.connect(self.voice_recording)


        # self.liczba1Edt.setFocus()
        self.setGeometry(20, 20, 300, 100)
        # self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Voice recording")
        self.show()

    def voice_recording(self):
        fs = 44100
        second = 3
        print("recording......")
        record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=1)
        sounddevice.wait()
        write("output.wav", fs, record_voice)

    def koniec(self):
        self.close()

    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Info',
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # baza.polacz()
    # model = TabModel(baza.pola)
    window = MainWindow()
    window.show()
    window.move(350, 200)
    sys.exit(app.exec_())
