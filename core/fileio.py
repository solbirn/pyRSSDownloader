import Queue
from threading import Thread

class FileIOTypes:
    Read = 80
    Write = 81
    Append = 82
    Delete = 83
    NetworkToFile = 84

class FileManager:
    """description of class"""
    def __init__(self, maxthreads=2):
        self.FMIORequestQueue = Queue.Queue(0)
        self.FMIOWorkerThreadPool = []
        for i in range(0, maxthreads):
            tf = FileManagerIOThread(self.FMIORequestQueue, self)
            self.FMIOWorkerThreadPool.append(tf)
            tf.start()
    def FMConvertFromNetwork(self, IRO):
        IRO.RequestType = FileIOTypes.NetworkToFile
        self.FMIORequestQueue.put(IRO)
    def setmanagers(self, managers):
        self.managers = managers
        self.DLDir = self.managers.SettingsManagerInst.DLDir
    def Request(self, IRO):
        self.NMIORequestQueue.put(IRO)

class FileManagerIOThread(Thread):
    def __init__(self, queue, FM):
        Thread.__init__(self)
        self.queue = queue
        self.FM = FM
        self.daemon = True
    def run(self):
        while 1:
            IRO = self.queue.get()
            self.ProcessFileIORequest(IRO)
            IRO.RequestCallback(IRO)
            self.queue.task_done()
    def ProcessFileIORequest(self, IRO):
        if IRO.RequestType == FileIOTypes.Write:
            try:
                fhandle = open(IRO.RequestData[0], "wb")
                fhandle.write(IRO.RequestData[1])
                fhandle.close()
                IRO.ResponseData = True
            except Exception, e:
                IRO.ResponseData = e
        elif IRO.RequestType == FileIOTypes.NetworkToFile:
            IRO.RequestType = FileIOTypes.Write
            IRO.RequestProcessingTrash.append(IRO.RequestData)
            IRO.RequestCallback = self.FM.managers.RSSFeedManagerInst.NotifyFileDownloaded
            IRO.RequestData = [self.FM.DLDir + IRO.RequestData.split("/")[-1], IRO.NetResponse]
            self.FM.FMIORequestQueue.put(IRO)