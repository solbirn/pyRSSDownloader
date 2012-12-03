import gui
from PyQt4 import QtCore, QtGui

class GuiManager(object):
    """description of class"""
    def __init__(self):
        return
    def GuiAddFeedDialog(self, tab=0):
        dialog = GuiRSSAddFeedDialog(self.managers, tab)
        dialog.show()
        dialog.exec_()
    def GuiInfoDialog(self, text="Oops! There should be text here."):
        dialog = GuiInfoErrorDialog(self.managers, text)
        dialog.show()
        dialog.exec_()    
    def GuiUpdateAllFeeds(self):
        return
    def GuiAddFeedToTree(self, IRO, ui=None):
        return
    def GuiRemoveFeedFromTree(self, feedidorname):
        return
    def GuiClearFeedList(self):
        for i in range(0, self.ui.feedlist.topLevelItemCount()):
            t = self.ui.feedlist.takeTopLevelItem(0)
            c = t.takeChildren()
            del c, t
    def GuiClearFeedDetailsList(self):
        self.ui.rssitemlist.clear()
    def GuiGetDLDirectory(self):
        return str(self.ui.basic_dlfolder_input.text())
    def GuiSetRSSFeedItemsList(self, item):
        self.GuiClearFeedDetailsList()
        if item.itype == "e":
            info = QtGui.QListWidgetItem()
            info.setText(QtGui.QApplication.translate("MainUi", "Title: " + item.title + "\r\nSize: " + str((int(item.size) / 1024)/1024) + "MB" + "\r\nReleased: " + item.published, None, QtGui.QApplication.UnicodeUTF8))
            info.link = item.link
            self.ui.rssitemlist.addItem(info)
            return
        elif item.itype == "s":
            for i in range(0,item.childCount()):
                e = item.child(i)
                info = QtGui.QListWidgetItem()
                info.setText(QtGui.QApplication.translate("MainUi", "Title: " + e.title + " \r\nSize: " + str((int(e.size) / 1024)/1024) + "MB" + "\r\nReleased: " + e.published, None, QtGui.QApplication.UnicodeUTF8))
                info.link = e.link
                self.ui.rssitemlist.addItem(info)
            return
        elif item.itype == "f":
            for i in range(0,item.childCount()):
                citem = item.child(i)
                for i in range(0,citem.childCount()):
                    e = citem.child(i)
                    info = QtGui.QListWidgetItem()
                    info.setText(QtGui.QApplication.translate("MainUi", "Title: " + e.title + " \r\nSize: " + str((int(e.size) / 1024)/1024) + "MB" + "\r\nReleased: " + e.published, None, QtGui.QApplication.UnicodeUTF8))
                    info.link = e.link
                    self.ui.rssitemlist.addItem(info)
        elif item.itype == "u":
            items = item.findItems(QtCore.QString("*"),QtCore.Qt.MatchWrap|QtCore.Qt.MatchWildcard)
            for item in items:
                print item.itype
                if item.itype == "s":
                    for i in range(0,item.childCount()):
                        e = item.child(i)
                        print e
                        info = QtGui.QListWidgetItem()
                        info.setText(QtGui.QApplication.translate("MainUi", "Title: " + e.title + " \r\nSize: " + str((int(e.size) / 1024)/1024) + "MB" + "\r\nReleased: " + e.published, None, QtGui.QApplication.UnicodeUTF8))
                        info.link = e.link
                        self.ui.rssitemlist.addItem(info)
            return
    def DebugPrint(self, t):
        self.ui.debug_textedit.setPlainText(QtGui.QApplication.translate("MainUi", t, None, QtGui.QApplication.UnicodeUTF8))
    def setmanagers(self, managers):
        self.managers = managers
    def setgui(self, gui):
        self.ui = gui

class GuiRSSAddFeedDialog(QtGui.QDialog):
    def __init__(self, managers, tab):
        QtGui.QDialog.__init__(self)
        from gui.rssaddui import Ui_RSSAddFeedDialog
        self.ui=Ui_RSSAddFeedDialog()
        self.ui.setupUi(self)
        self.ui.tabs.setCurrentIndex(tab)
        self.managers = managers

        self.rsseasyaddurlstring = "http://invalideasyaddurl/%s"

    def RSSAddFeedByName(self):
        RSSUrlString = str(self.ui.functions_findrss_easy_input.text())
        RSSUrlItem = QtGui.QListWidgetItem()
        RSSUrlItem.setText(QtGui.QApplication.translate("RSSAddFeedDialog", self.rsseasyaddurlstring % RSSUrlString.lower().strip().replace(" ","-"), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.tab_easy_list.addItem(RSSUrlItem)
    def RSSAddFeedByURL(self):
        RSSUrlString = str(self.ui.functions_findrss_adv_input.text())
        RSSUrlItem = QtGui.QListWidgetItem()
        RSSUrlItem.setText(QtGui.QApplication.translate("RSSAddFeedDialog", RSSUrlString, None, QtGui.QApplication.UnicodeUTF8))
        self.ui.tab_adv_list.addItem(RSSUrlItem)
    def RSSAddFeedByURLBatch(self):
        return
    def RSSAddFeedGatherUiInfoList(self):
        index = self.ui.tabs.currentIndex()
        if index == 0:
            items = self.ui.tab_easy_list.findItems(QtCore.QString("*"),QtCore.Qt.MatchWrap|QtCore.Qt.MatchWildcard)
        elif index == 1:
            items = self.ui.tab_adv_list.findItems(QtCore.QString("*"),QtCore.Qt.MatchWrap|QtCore.Qt.MatchWildcard)
        else:
            raise NotImplementedError
        links = []
        for item in items:
            links.append(str(item.text()))
        #helper = guihelpers(self.managers)
        #helper.GuiInfoDialog(links)
        return links
    def RegisterEasyAddURLString(self, urlstring):
        self.rsseasyaddurlstring = urlstring
    def save(self):
        self.hide()
        self.managers.ThreadManagerInst.dispatch("RSSAddFeed", self.RSSAddFeedGatherUiInfoList())
        self.accept()

class GuiInfoErrorDialog(QtGui.QDialog):
    def __init__(self, managers, text):
        QtGui.QDialog.__init__(self)
        from gui.infoui import Ui_GuiInfoErrorDialog
        self.ui=Ui_GuiInfoErrorDialog()
        self.ui.setupUi(self)
        self.managers = managers
        import string
        self.ui.text_output.setText(QtCore.QString(string.join(text, "\r\n")))

class PrdTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent):
        self.objectName = ""
        QtGui.QTreeWidgetItem.__init__(self,  parent)
    def setObjectName(self, name):
        self.objectName = name
    def setObjectData(self, type="f", link=None, size=None, id=None, title=None, published=None):
        self.id = id
        self.title = title
        self.link = link
        self.size = size
        self.published = published
        self.itype = type
    def findChild(self, text):
        for i in range(0,self.childCount()):
            t = self.child(i)
            if self.child(i).objectName  == text:
                return self.child(i)
    def findChildById(self, text):
        for i in range(0,self.childCount()-1):
            t = self.child(i)
            if self.child(i).objectName  == text:
                return self.child(i)