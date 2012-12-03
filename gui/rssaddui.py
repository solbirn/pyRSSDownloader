# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RSSAddFeedDialog.ui'
#
# Created: Sun Dec 02 21:22:51 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RSSAddFeedDialog(object):
    def setupUi(self, RSSAddFeedDialog):
        RSSAddFeedDialog.setObjectName(_fromUtf8("RSSAddFeedDialog"))
        RSSAddFeedDialog.resize(589, 410)
        self.gridLayout = QtGui.QGridLayout(RSSAddFeedDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabs = QtGui.QTabWidget(RSSAddFeedDialog)
        self.tabs.setObjectName(_fromUtf8("tabs"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addfeed_easy_widget = QtGui.QWidget(self.tab)
        self.addfeed_easy_widget.setObjectName(_fromUtf8("addfeed_easy_widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.addfeed_easy_widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.functions_findrss_easy_input = QtGui.QLineEdit(self.addfeed_easy_widget)
        self.functions_findrss_easy_input.setEnabled(False)
        self.functions_findrss_easy_input.setObjectName(_fromUtf8("functions_findrss_easy_input"))
        self.horizontalLayout.addWidget(self.functions_findrss_easy_input)
        self.functions_findrss_easy = QtGui.QPushButton(self.addfeed_easy_widget)
        self.functions_findrss_easy.setEnabled(False)
        self.functions_findrss_easy.setObjectName(_fromUtf8("functions_findrss_easy"))
        self.horizontalLayout.addWidget(self.functions_findrss_easy)
        self.verticalLayout.addWidget(self.addfeed_easy_widget)
        self.tab_easy_list = QtGui.QListWidget(self.tab)
        self.tab_easy_list.setObjectName(_fromUtf8("tab_easy_list"))
        self.verticalLayout.addWidget(self.tab_easy_list)
        self.tabs.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QtGui.QWidget(self.tab_2)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.functions_findrss_adv_input = QtGui.QLineEdit(self.widget)
        self.functions_findrss_adv_input.setObjectName(_fromUtf8("functions_findrss_adv_input"))
        self.horizontalLayout_2.addWidget(self.functions_findrss_adv_input)
        self.function_findrss_adv = QtGui.QPushButton(self.widget)
        self.function_findrss_adv.setObjectName(_fromUtf8("function_findrss_adv"))
        self.horizontalLayout_2.addWidget(self.function_findrss_adv)
        self.verticalLayout_2.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(self.tab_2)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tab_adv_list = QtGui.QListWidget(self.widget_2)
        self.tab_adv_list.setObjectName(_fromUtf8("tab_adv_list"))
        self.horizontalLayout_3.addWidget(self.tab_adv_list)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.tabs.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabs.addTab(self.tab_3, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabs, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RSSAddFeedDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Abort|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(RSSAddFeedDialog)
        self.tabs.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RSSAddFeedDialog.save)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RSSAddFeedDialog.reject)
        QtCore.QObject.connect(self.functions_findrss_easy, QtCore.SIGNAL(_fromUtf8("clicked()")), RSSAddFeedDialog.RSSAddFeedByName)
        QtCore.QObject.connect(self.function_findrss_adv, QtCore.SIGNAL(_fromUtf8("clicked()")), RSSAddFeedDialog.RSSAddFeedByURL)
        QtCore.QMetaObject.connectSlotsByName(RSSAddFeedDialog)
        RSSAddFeedDialog.setTabOrder(self.functions_findrss_adv_input, self.function_findrss_adv)
        RSSAddFeedDialog.setTabOrder(self.function_findrss_adv, self.buttonBox)
        RSSAddFeedDialog.setTabOrder(self.buttonBox, self.tab_easy_list)
        RSSAddFeedDialog.setTabOrder(self.tab_easy_list, self.functions_findrss_easy)
        RSSAddFeedDialog.setTabOrder(self.functions_findrss_easy, self.functions_findrss_easy_input)
        RSSAddFeedDialog.setTabOrder(self.functions_findrss_easy_input, self.tab_adv_list)
        RSSAddFeedDialog.setTabOrder(self.tab_adv_list, self.tabs)

    def retranslateUi(self, RSSAddFeedDialog):
        RSSAddFeedDialog.setWindowTitle(QtGui.QApplication.translate("RSSAddFeedDialog", "Add an RSS feed", None, QtGui.QApplication.UnicodeUTF8))
        self.functions_findrss_easy_input.setText(QtGui.QApplication.translate("RSSAddFeedDialog", "Enter a supported \"easy add\" name here", None, QtGui.QApplication.UnicodeUTF8))
        self.functions_findrss_easy.setText(QtGui.QApplication.translate("RSSAddFeedDialog", "Find Show", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), QtGui.QApplication.translate("RSSAddFeedDialog", "Easy", None, QtGui.QApplication.UnicodeUTF8))
        self.function_findrss_adv.setText(QtGui.QApplication.translate("RSSAddFeedDialog", "Add Feed", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), QtGui.QApplication.translate("RSSAddFeedDialog", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_3), QtGui.QApplication.translate("RSSAddFeedDialog", "Advanced (batch)", None, QtGui.QApplication.UnicodeUTF8))

