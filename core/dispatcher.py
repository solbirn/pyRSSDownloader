import gui
from threading import Thread
from PyQt4 import QtCore, QtGui

from gui.manager import GuiRSSAddFeedDialog, GuiInfoErrorDialog
from storage.manager import IORequestObject, IORequestType
from core.fileio import FileIOTypes

class PrdMethods(object):
    def __init__(self, managers, args=None):
        self.managers = managers
        self.ui = managers.GuiManagerInst.ui
        self.args = args
        return
    def setArgs(self):
        self.args = args
    def DLForceUpdate(self):
        self.ui.label_4.setText(QtGui.QApplication.translate("RSSDownloaderMainUi", "Now", None, QtGui.QApplication.UnicodeUTF8))
        return
    def DLSetHoldStatus(self):
        self.ui.label_4.setText(QtGui.QApplication.translate("RSSDownloaderMainUi", "Never", None, QtGui.QApplication.UnicodeUTF8))
        return
    def DLStartChanged(self):
        return
    def DLUpdateIntChanged(self):
        return
    def DLPrefQualityChanged(self):
        return
    def DLPullDLSettings(self):
        return
    def DLDLItems(self, IRO=12):
        if IRO == 12:
            items = self.ui.rssitemlist.selectedItems()
            for item in items:
                request = IORequestObject(IORequestType.ReadFeed, self.managers.FileManagerInst.FMConvertFromNetwork, item.link, self.managers.StorageManagerInst)
                self.managers.NetworkManagerInst.NMIORequestQueue.put(request)
        elif type(IRO) != type(Exception):
            IRO.RequestType = FileIOTypes.Write
            IRO.RequestProcessingTrash.append(IRO.RequestData)
            IRO.RequestCallback = self.managers.RSSFeedManagerInst.NotifyFileDownloaded
            IRO.RequestData = [self.managers.SettingsManagerInst.DLDir + IRO.RequestData.split("/")[-1], IRO.NetResponse]
            self.managers.FileManagerInst.FMIORequestQueue.put(IRO)
        else:
            #add logging
            return
    def RSSAddFeed(self, IRO=12):
        if IRO == 12:
            feedrequesttype = IORequestType.WriteFeed
            feedrequest = IORequestObject(feedrequesttype, self.RSSAddFeed, self.args[0], self.managers.StorageManagerInst)
            self.managers.RSSFeedManagerInst.Request(feedrequest)
        elif type(IRO) != type(Exception):
            IRO.RequestProcessingTrash.append(IRO.ResponseData)
            IRO.ResponseData = IRO.RequestData
            self.managers.GuiManagerInst.GuiAddFeedToTree(IRO, self.ui)
        else:
            #add logging
            return
        return
    def RSSRemoveFeed(self):
        return
    def RSSReadAllFeeds(self, IRO=12):
        #print "In dispatcher.TreadManager().RSSReadAllFeeds(data)"
        if IRO == 12:
            feedrequesttype = IORequestType.ReadAllFeeds
            feedrequest = IORequestObject(feedrequesttype, self.RSSReadAllFeeds, None, self.managers.StorageManagerInst)
            self.managers.RSSFeedManagerInst.Request(feedrequest)
        elif type(IRO) != type(Exception):
            self.managers.GuiManagerInst.GuiClearFeedList()
            self.managers.GuiManagerInst.GuiAddFeedToTree(IRO, self.ui)
        else:
            print "Error!"
            #add logging
            return
        return
    def RSSActivateDetails(self):
        self.managers.GuiManagerInst.GuiSetRSSFeedItemsList(self.args[0])
    def SettingsDBChanged(self):
        return
    def SettingsDBReload(self):
        return
    def SettingsBasicChanged(self):
        return
    def DebugPrintIROs(self):
        IRO_STR_LIST = ""
        for IRO in self.managers.StorageManagerInst.IROActiveList:
            IRO_STR_LIST = IRO_STR_LIST + IRO.__repr__() + "\r\n\r\n"
        for IRO in self.managers.StorageManagerInst.IRONonActiveList:
            IRO_STR_LIST = IRO_STR_LIST + IRO.__repr__() + "\r\n\r\n"
        self.managers.GuiManagerInst.DebugPrint(IRO_STR_LIST)
    def DebugPrintThreads(self):
        raise NotImplementedError

class PrdCreateThread(Thread):
    """Universal ui background threading subsystem"""
    def __init__(self, method, managers, args):
        Thread.__init__(self)
        self.method = method
        self.managers = managers
        self.args = args
        return
    def run(self):
        self.m = PrdMethods(self.managers, self.args)
        self.PrdThreadFindEntryPoint()
        del self.m
        return
    def PrdThreadFindEntryPoint(self):
        try:
            if (self.method == "DLForceUpdate"):
                self.m.DLForceUpdate()
                return
            elif (self.method == "RSSReadAllFeeds"):
                self.m.RSSReadAllFeeds()
                return
            elif (self.method == "DLSetHoldStatus"):
                self.m.DLSetHoldStatus()
                return
            elif (self.method == "DLStartChanged"):
                self.m.DLStartChanged()
                return
            elif (self.method == "DLUpdateIntChanged"):
                self.m.DLUpdateIntChanged()
                return
            elif (self.method == "DLPrefQualityChanged"):
                self.m.DLPrefQualityChanged()
                return
            elif (self.method == "DLPullDLSettings"):
                self.m.DLPullDLSettings()
                return
            elif (self.method == "DLDLItems"):
                self.m.DLDLItems()
                return
            elif (self.method == "RSSAddFeed"):
                self.m.RSSAddFeed()
                return
            elif (self.method == "RSSRemoveFeed"):
                self.m.RSSRemoveFeed()
                return
            elif (self.method == "RSSActivateDetails"):
                self.m.RSSActivateDetails()
                return
            elif (self.method == "SettingsDBChanged"):
                self.m.SettingsDBChanged()
                return
            elif (self.method == "SettingsDBReload"):
                self.m.SettingsDBReload()
                return
            elif (self.method == "SettingsBasicChanged"):
                self.m.SettingsBasicChanged()
                return
            elif (self.method == "DebugPrintIROs"):
                self.m.DebugPrintIROs()
                return
            elif (self.method == "DebugPrintThreads"):
                self.m.DebugPrintThreads()
                return
        except Exception, e:
            print e

class ThreadManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.queue = []
        self.ThreadCollections = None
        self.ui = None
        self.start()
    def dispatch(self,  method, args=None):
        prdthreadinst = PrdCreateThread(method, self.managers, args)
        prdthreadinst.start()
        self.queue.append(prdthreadinst)
    def setmanagers(self, managers):
        self.managers = managers
        self.ThreadCollections = {
                                 'NMIO' : self.managers.NetworkManagerInst.NMIOWorkerThreadPool,
                                 'RFNetReq' : self.managers.RSSFeedManagerInst.RFNetReqWorkerThreadPool,
                                 'RFNetRes' : self.managers.RSSFeedManagerInst.RFNetResWorkerThreadPool,
                                 'RFRaw' : self.managers.RSSFeedManagerInst.RFRawWorkerThreadPool,
                                 'DBDPreExec' : self.managers.StorageManagerInst.driver.DBDPreExecutionWorkerThreadPool,
                                 'DBDExec' : self.managers.StorageManagerInst.driver.DBDExecutionWorkerThreadPool,
                                 }
    def clean(self):
        raise NotImplementedError