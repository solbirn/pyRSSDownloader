import Queue, os
from threading import Thread

from storage.manager import IORequestObject, IORequestThread, IORequestType

class RSSFeedManager:
    def __init__(self, maxrawthreads=5, maxnetthreads=5):
        self.RSS_PLUGIN_DIR = os.getcwd() + os.sep + "plugins"
        for plugin in os.listdir(self.RSS_PLUGIN_DIR):
            if os.path.isdir(os.path.join(self.RSS_PLUGIN_DIR, plugin)) and ("__init__" not in plugin):
                #For the time being only a single plugin is supported at a time. So to simplify things:
                exec ( "from plugins.%s.main import *" % plugin )
                exec ( "self.RSSFeedManagerIOThread = RSSFeedManagerIOThread" )
                exec ( "self.DBDPreExecutionThread = DBDPreExecutionThread" )
                exec ( "self.RSSFeedTypePlugin = RSSFeedTypePlugin" )
                exec ( "self.RSSFeedSource = RSSFeedSource" )
                exec ( "self.GuiAddFeedToTree = GuiAddFeedToTree" )
                break
                
                ##For future multi plugin implemetation
                #self.RSSFeedPlugins = []
                #exec ( "from plugins.%s.main import RSSFeedSource as plugin_%s_RSSFeedSource" % (plugin, plugin))
                #exec ( "from plugins.%s.main import RSSFeedTypePlugin as plugin_%s_RSSFeedType" % (plugin, plugin))
                #exec ( "self.RSSFeedPlugins.append({\"RSSFeedTypePluginName\": \"%s\", \"RSSFeedSource\": plugin_%s_RSSFeedSource, \"RSSFeedTypePlugin\": plugin_%s_RSSFeedType})" % (plugin, plugin, plugin))

        self.RFRawRequestQueue = Queue.Queue(0)
        self.RFNetRequestQueue = Queue.Queue(0)
        self.RFNetResponseQueue = Queue.Queue(0)
        self.RFIORequestQueue = Queue.Queue(0)
        self.RFRawWorkerThreadPool = []
        self.RFNetReqWorkerThreadPool = []
        self.RFNetResWorkerThreadPool = []
        self.RFIORequestWorkerThreadPool = []
        for i in range(0, maxrawthreads):
            tr = RSSFeedManagerRawIOThread(self.RFRawRequestQueue, self)
            self.RFRawWorkerThreadPool.append(tr)
            tr.start()
        for i in range(0, maxnetthreads):
            tnrq = RSSFeedManagerNetReqIOThread(self.RFNetRequestQueue, self)
            self.RFNetReqWorkerThreadPool.append(tnrq)
            tnrq.start()
        for i in range(0, maxnetthreads):
            tnrp = RSSFeedManagerNetResIOThread(self.RFNetResponseQueue, self)
            self.RFNetResWorkerThreadPool.append(tnrp)
            tnrp.start()
        for i in range(0, maxrawthreads):
            tio = RSSFeedManagerIOThread(self.RFIORequestQueue, self)
            self.RFIORequestWorkerThreadPool.append(tio)
            tio.start()
    def Request(self, IRO):
        self.RFRawRequestQueue.put(IRO)
    def ProcessNetResponse(self, IRO):
        self.RFNetResponseQueue.put(IRO)
    def ProcessIOResponse(self, IRO):
        self.RFIORequestQueue.put(IRO)
    def NotifyFileDownloaded(self, IRO):
        return
    def setmanagers(self, managers):
        self.managers = managers
        self.managers.GuiManagerInst.GuiAddFeedToTree = self.GuiAddFeedToTree

class RSSFeedManagerRawIOThread(Thread):
    def __init__(self, queue, FM):
        Thread.__init__(self)
        self.queue = queue
        self.FM = FM
        self.daemon = True
    def run(self):
        while 1:
            IRO = self.queue.get()
            if self.CheckForNet(IRO):
                self.FM.RFNetRequestQueue.put(IRO)
            else:
                self.ProcessIORequest(IRO)
            self.queue.task_done()
    def ProcessIORequest(self, IRO):
        self.FM.RFIORequestQueue.put(IRO)
    def CheckForNet(self, IRO):
        if IRO.RequestType == IORequestType.WriteFeed:
            return True
        else:
            return False

class RSSFeedManagerNetReqIOThread(Thread):
    def __init__(self, queue, FM):
        Thread.__init__(self)
        self.queue = queue
        self.FM = FM
        self.daemon = True
    def run(self):
        while 1:
            IRO = self.queue.get()
            self.ProcessNetRequest(IRO)
            self.queue.task_done()
    def ProcessNetRequest(self, IRO):        
        IRO.RequestProcessingTrash.append(IRO.RequestData)
        IRO.NetCallback = self.FM.ProcessNetResponse
        self.FM.managers.NetworkManagerInst.Request(IRO)

class RSSFeedManagerNetResIOThread(Thread):
    def __repr__(self):
        return super(RSSFeedManagerNetResIOThread, self).__repr__() + '  <%s.%s at %s>' % (self.__class__.__module__, self.__class__.__name__, hex(id(self)))
    def __init__(self, queue, FM):
        Thread.__init__(self)
        self.queue = queue
        self.FM = FM
        self.daemon = True
    def run(self):
        while 1:
            IRO = self.queue.get()
            self.ProcessNetResponse(IRO)
            self.FM.RFIORequestQueue.put(IRO)
            self.queue.task_done()
    def ProcessNetResponse(self, IRO):
        IRO.RequestData = self.FM.RSSFeedTypePlugin(IRO.NetResponse, IRO.NetRequest)
        return