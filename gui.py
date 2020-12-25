# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton, QMenuBar, QMainWindow, QWidget, QButtonGroup, QGroupBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QMessageBox


class Ui_Widget(object):

    def setup_ui(self, widget):
        widget.setObjectName("Widget")

        # przyciski PushButton ###
        button_layout_box = QHBoxLayout()
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)
        for v in ('Speech', 'Sound', 'Pitch'):
            self.btn = QPushButton(v)
            self.btn.setStyleSheet("background-color: lightblue")
            self.button_group.addButton(self.btn)
            button_layout_box.addWidget(self.btn)
        # grupujemy przyciski
        self.button_groupbox = QGroupBox('Recognition mode')
        self.button_groupbox.setLayout(button_layout_box)
        self.button_groupbox.setObjectName('Push')
        # koniec PushButton ###

        info_panel = QHBoxLayout()
        label1 = QLabel("Profile: Profile 1", self)
        label2 = QLabel("Placeholder for sound visuals", self)
        info_panel.addWidget(label1)
        info_panel.addWidget(label2)

        # table data view
        self.view = QTableView()

        # przyciski Push ###
        self.logujBtn = QPushButton("Za&loguj")
        # self.koniecBtn = QPushButton("&Koniec")
        self.dodajBtn = QPushButton("&Dodaj")
        self.dodajBtn.setEnabled(False)
        self.zapiszBtn = QPushButton("&Zapisz")
        self.zapiszBtn.setEnabled(False)

        # Push buttons layout ###
        layout = QHBoxLayout()
        layout.addWidget(self.logujBtn)
        layout.addWidget(self.dodajBtn)
        layout.addWidget(self.zapiszBtn)
        # layout.addWidget(self.koniecBtn)

        # main view ###
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.button_groupbox)
        layoutV.addLayout(info_panel)
        layoutV.addWidget(self.view)
        layoutV.addLayout(layout)


class LoginDialog(QDialog):
    """ Logon window """

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        # etykiety, pola edycyjne i przyciski ###
        loginLbl = QLabel('Login')
        hasloLbl = QLabel('Hasło')
        self.login = QLineEdit()
        self.haslo = QLineEdit()
        self.przyciski = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # układ główny ###
        uklad = QGridLayout(self)
        uklad.addWidget(loginLbl, 0, 0)
        uklad.addWidget(self.login, 0, 1)
        uklad.addWidget(hasloLbl, 1, 0)
        uklad.addWidget(self.haslo, 1, 1)
        uklad.addWidget(self.przyciski, 2, 0, 2, 0)

        # sygnały i sloty ###
        self.przyciski.accepted.connect(self.accept)
        self.przyciski.rejected.connect(self.reject)

        # właściwości widżetu ###
        self.setModal(True)
        self.setWindowTitle('Logowanie')

    def loginHaslo(self):
        return (self.login.text().strip(),
                self.haslo.text().strip())

    # metoda statyczna, tworzy dialog i zwraca (login, haslo, ok)
    @staticmethod
    def getLoginHaslo(parent=None):
        dialog = LoginDialog(parent)
        dialog.login.setFocus()
        ok = dialog.exec_()
        login, haslo = dialog.loginHaslo()
        return (login, haslo, ok == QDialog.Accepted)