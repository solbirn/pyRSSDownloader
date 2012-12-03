# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiInfoErrorDialog.ui'
#
# Created: Sat Nov 10 20:38:12 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GuiInfoErrorDialog(object):
    def setupUi(self, GuiInfoErrorDialog):
        GuiInfoErrorDialog.setObjectName(_fromUtf8("GuiInfoErrorDialog"))
        GuiInfoErrorDialog.resize(400, 142)
        self.gridLayout = QtGui.QGridLayout(GuiInfoErrorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.text_output = QtGui.QTextEdit(GuiInfoErrorDialog)
        self.text_output.setObjectName(_fromUtf8("text_output"))
        self.gridLayout.addWidget(self.text_output, 0, 0, 1, 1)
        self.InfoErrorDialog = QtGui.QDialogButtonBox(GuiInfoErrorDialog)
        self.InfoErrorDialog.setOrientation(QtCore.Qt.Horizontal)
        self.InfoErrorDialog.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.InfoErrorDialog.setObjectName(_fromUtf8("InfoErrorDialog"))
        self.gridLayout.addWidget(self.InfoErrorDialog, 1, 0, 1, 1)

        self.retranslateUi(GuiInfoErrorDialog)
        QtCore.QObject.connect(self.InfoErrorDialog, QtCore.SIGNAL(_fromUtf8("accepted()")), GuiInfoErrorDialog.accept)
        QtCore.QObject.connect(self.InfoErrorDialog, QtCore.SIGNAL(_fromUtf8("rejected()")), GuiInfoErrorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GuiInfoErrorDialog)

    def retranslateUi(self, GuiInfoErrorDialog):
        GuiInfoErrorDialog.setWindowTitle(QtGui.QApplication.translate("GuiInfoErrorDialog", "PRD Info/Errror Dialog", None, QtGui.QApplication.UnicodeUTF8))

