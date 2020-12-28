# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton, QMenuBar, QMainWindow, QWidget, QButtonGroup, QGroupBox, \
    QRadioButton, QComboBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QMessageBox

import database


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

        self.info_panel = QHBoxLayout()
        self.label1 = QLabel("Profile: not selected", self)
        self.label2 = QLabel("Placeholder for sound visuals", self)
        self.info_panel.addWidget(self.label1)
        self.info_panel.addWidget(self.label2)

        # table for data-model-view
        self.view = QTableView()

        # lower buttons ###
        self.select_profile_button = QPushButton("Select Profile")
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.setEnabled(False)
        self.save_changes_button = QPushButton("Save Changes")
        self.save_changes_button.setEnabled(False)

        # lower buttons layout ###
        layout = QHBoxLayout()
        layout.addWidget(self.select_profile_button)
        layout.addWidget(self.add_task_button)
        layout.addWidget(self.save_changes_button)

        # vertical layout for all elements ###
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.button_groupbox)
        layoutV.addLayout(self.info_panel)
        layoutV.addWidget(self.view)
        layoutV.addLayout(layout)


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

    def __init__(self, parent=None):
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
        # grid_layout = QGridLayout()
        # grid_layout.addWidget(desc_label, 0, 0)
        # grid_layout.addWidget(self.desc_line, 0, 1)
        # grid_layout.addWidget(func_label, 1, 0)
        # grid_layout.addWidget(self.function_list, 1, 1)
        # grid_layout.addWidget(trigger_label, 2, 0)
        # grid_layout.addWidget(self.trigger_list, 2, 1)
        # grid_layout.addWidget(bonus_label, 3, 0)
        # grid_layout.addWidget(self.bonus_data, 3, 1)
        # grid_layout.addWidget(self.lower_buttons, 4, 0)

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
