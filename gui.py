# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton, QMenuBar, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QMessageBox


class Ui_Widget(object):

    def setup_ui(self, widget):
        widget.setObjectName("Widget")

        # table data view
        self.view = QTableView()

        # przyciski Push ###
        # self.logujBtn = QPushButton("Za&loguj")
        self.koniecBtn = QPushButton("&Koniec")
        # self.dodajBtn = QPushButton("&Dodaj")
        # self.dodajBtn.setEnabled(False)
        # self.zapiszBtn = QPushButton("&Zapisz")
        # self.zapiszBtn.setEnabled(False)

        # Push buttons layout ###
        layout = QHBoxLayout()
        # layout.addWidget(self.logujBtn)
        # layout.addWidget(self.dodajBtn)
        # layout.addWidget(self.zapiszBtn)
        layout.addWidget(self.koniecBtn)

        # main view ###
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.view)
        layoutV.addLayout(layout)

        self.setWindowTitle("Modular Sound Control System")
        self.resize(500, 300)