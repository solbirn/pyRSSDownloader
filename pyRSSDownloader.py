from gui.manager import GuiManager
from rss.manager import RSSFeedManager
from core.settings import SettingsManager
from core.fileio import FileManager
from core.dispatcher import ThreadManager, PrdMethods
from network.manager import NetworkManager
from storage.manager import StorageManager

from gui.mainui import *
import sys

class Managers:
    def __init__(self):
        self.SettingsManagerInst = SettingsManager()
        self.StorageManagerInst = StorageManager()
        self.RSSFeedManagerInst = RSSFeedManager()
        self.NetworkManagerInst = NetworkManager()
        self.FileManagerInst = FileManager()
        self.GuiManagerInst = GuiManager()
        self.ThreadManagerInst =  ThreadManager()

        self.setmanagers()

    def setmanagers(self):
        self.SettingsManagerInst.setmanagers(self)
        self.StorageManagerInst.setmanagers(self)
        self.RSSFeedManagerInst.setmanagers(self)
        self.NetworkManagerInst.setmanagers(self)
        self.FileManagerInst.setmanagers(self)
        self.GuiManagerInst.setmanagers(self)
        self.ThreadManagerInst.setmanagers(self)

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui=Ui_MainUi()
        self.ui.setupUi(self)

        self.managers = Managers()
        self.managers.GuiManagerInst.setgui(self.ui)
        self.managers.GuiManagerInst.main = self

        self.GuiModeThreadManager = PrdMethods(self.managers)
        self.GuiModeThreadManager.RSSReadAllFeeds()
        
            
    #GUI Functions - runs in main thread
    def RSSContextMenu(self, i):
        menu = QtGui.QMenu()
        menu.addAction(self.ui.actionRSSAddFeed)
        menu.addAction(self.ui.actionRSSRemoveFeed)
        menu.addAction(self.ui.actionRSSUpdateFeed)
        menu.addAction(self.ui.actionRSSUpdateAllFeeds)
        menu.addAction(self.ui.actionListDLItems)
        menu.exec_(self.ui.feedlist.mapToGlobal(i))  
    def RSSFeedItemContextMenu(self, i):
        menu = QtGui.QMenu()
        menu.addAction(self.ui.actionDLItem)
        menu.exec_(self.ui.rssitemlist.mapToGlobal(i))
    def RSSAddFeedE(self):
        helper = self.managers.GuiManagerInst
        helper.GuiAddFeedDialog(0)
    def RSSAddFeedM(self):
        helper = self.managers.GuiManagerInst
        helper.GuiAddFeedDialog(1)

    #NonGUI Functions - needs threading
    def DLForceUpdate(self):
        self.managers.ThreadManagerInst.dispatch("DLForceUpdate")
    def DLSetHoldStatus(self):
        self.managers.ThreadManagerInst.dispatch("DLSetHoldStatus")
    def DLStartChanged(self):
        self.managers.ThreadManagerInst.dispatch("DLStartChanged")
    def DLUpdateIntChanged(self):
        self.managers.ThreadManagerInst.dispatch("DLUpdateIntChanged")
    def DLPrefQualityChanged(self):
        self.managers.ThreadManagerInst.dispatch("DLPrefQualityChanged")
    def DLPullDLSettings(self):
        self.managers.ThreadManagerInst.dispatch("DLPullDLSettings")
    def DLDLItems(self):
        self.managers.ThreadManagerInst.dispatch("DLDLItems")
    def RSSUpdateAllFeeds(self):
        self.managers.ThreadManagerInst.dispatch("RSSReadAllFeeds")
    def RSSRefreshAllFeeds(self):
        self.managers.ThreadManagerInst.dispatch("RSSReadAllFeeds")
    def RSSRemoveFeed(self):
        self.managers.ThreadManagerInst.dispatch("RSSRemoveFeed")
    def RSSActivateDetails(self, rssitem, column):
        self.managers.ThreadManagerInst.dispatch("RSSActivateDetails", (rssitem, column))
    def SettingsDBChanged(self):
        self.managers.ThreadManagerInst.dispatch("SettingsDBChanged")
    def SettingsDBReload(self):
        self.managers.ThreadManagerInst.dispatch("SettingsDBReload")
    def SettingsBasicChanged(self):
        self.managers.ThreadManagerInst.dispatch("SettingsBasicChanged")
    def DebugPrintIROs(self):
        self.managers.ThreadManagerInst.dispatch("DebugPrintIROs")
    def DebugPrintThreads(self):
        self.managers.ThreadManagerInst.dispatch("DebugPrintThreads")
    
    #PyQt Event Handlers
    def closeEvent(self, event):
        #TODO: Verfiy all saved
        event.isAccepted()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())