# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant


class TabModel(QAbstractTableModel):
    """ Table model view """

    def __init__(self, fields=[], data=[], parent=None):
        super(TabModel, self).__init__()
        self.fields = fields
        self.table = data

    def update(self, data):
        """ Assigns data source to the model """
        print(data)
        self.table = data

    def rowCount(self, parent=QModelIndex()):
        """ Returns amount of records """
        return len(self.table)

    def columnCount(self, parent=QModelIndex()):
        """ Returns column count """
        if self.table:
            return len(self.table[0])
        else:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        """ Displays data """
        i = index.row()
        j = index.column()

        if role == Qt.DisplayRole:
            return '{0}'.format(self.table[i][j])
        elif role == Qt.CheckStateRole and (j == 4 or j == 5):
            if self.table[i][j]:
                return Qt.Checked
            else:
                return Qt.Unchecked
        elif role == Qt.EditRole and j == 1:
            return self.table[i][j]
        else:
            return QVariant()

    def flags(self, index):
        """ Returns properties of the column """
        flags = super(TabModel, self).flags(index)
        j = index.column()
        if j == 1:
            flags |= Qt.ItemIsEditable
        elif j == 4 or j == 5:
            flags |= Qt.ItemIsUserCheckable

        return flags

    def setData(self, index, value, role=Qt.DisplayRole):
        """ Changes data """
        i = index.row()
        j = index.column()
        if role == Qt.EditRole and j == 1:
            self.table[i][j] = value
        elif role == Qt.CheckStateRole and (j == 4 or j == 5):
            if value:
                self.table[i][j] = True
            else:
                self.table[i][j] = False

        return True

    def headerData(self, section, direction, role=Qt.DisplayRole):
        """ Returns headers of the columns """
        if role == Qt.DisplayRole and direction == Qt.Horizontal:
            return self.fields[section]
        elif role == Qt.DisplayRole and direction == Qt.Vertical:
            return section + 1
        else:
            return QVariant()


class ProfileTabModel(QAbstractTableModel):
    """ Table model view """

    def __init__(self, fields=[], data=[], parent=None):
        super(ProfileTabModel, self).__init__()
        self.fields = fields
        self.table = data

    def update(self, data):
        """ Assigns data source to the model """
        print(data)
        self.table = data

    def rowCount(self, parent=QModelIndex()):
        """ Returns amount of records """
        return len(self.table)

    def columnCount(self, parent=QModelIndex()):
        """ Returns column count """
        if self.table:
            return len(self.table[0])
        else:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        """ Displays data """
        i = index.row()
        j = index.column()

        if role == Qt.DisplayRole:
            return '{0}'.format(self.table[i][j])
        elif role == Qt.CheckStateRole and j == 2:
            if self.table[i][j]:
                return Qt.Checked
            else:
                return Qt.Unchecked
        elif role == Qt.EditRole and j == 1:
            return self.table[i][j]
        else:
            return QVariant()

    def flags(self, index):
        """ Returns properties of the column """
        flags = super(TabModel, self).flags(index)
        j = index.column()
        if j == 1:
            flags |= Qt.ItemIsEditable
        elif j == 2:
            flags |= Qt.ItemIsUserCheckable

        return flags

    def setData(self, index, value, role=Qt.DisplayRole):
        """ Changes data """
        i = index.row()
        j = index.column()
        if role == Qt.EditRole and j == 1:
            self.table[i][j] = value
        elif role == Qt.CheckStateRole and j == 2:
            if value:
                self.table[i][j] = True
            else:
                self.table[i][j] = False

        return True

    def headerData(self, section, direction, role=Qt.DisplayRole):
        """ Returns headers of the columns """
        if role == Qt.DisplayRole and direction == Qt.Horizontal:
            return self.fields[section]
        elif role == Qt.DisplayRole and direction == Qt.Vertical:
            return section + 1
        else:
            return QVariant()
