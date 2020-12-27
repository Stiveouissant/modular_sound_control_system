# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton, QMenuBar, QMainWindow, QWidget, QButtonGroup, QGroupBox, \
    QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QMessageBox


class Ui_Widget(object):

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

        info_panel = QHBoxLayout()
        label1 = QLabel("Profile: Profile 1", self)
        label2 = QLabel("Placeholder for sound visuals", self)
        info_panel.addWidget(label1)
        info_panel.addWidget(label2)

        # table data model view
        self.view = QTableView()

        # lower buttons ###
        self.logujBtn = QPushButton("Za&loguj")
        # self.koniecBtn = QPushButton("&Koniec")
        self.dodajBtn = QPushButton("&Dodaj")
        self.dodajBtn.setEnabled(False)
        self.zapiszBtn = QPushButton("&Zapisz")
        self.zapiszBtn.setEnabled(False)

        # lower buttons layout ###
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


class ProfileDialog(QDialog):
    """ Logon window """

    def __init__(self, parent=None):
        super(ProfileDialog, self).__init__(parent)

        # radio buttons ###
        self.radio_layout = QVBoxLayout()
        for v in ('profile1', 'profile2'):
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
        self.setModal(True)
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
