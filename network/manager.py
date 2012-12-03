import urllib2, Queue
from threading import Thread

class NetworkManager:
    """description of class"""
    def __init__(self, maxrawthreads=10):
        self.NMIORequestQueue = Queue.Queue(0)
        self.NMIOWorkerThreadPool = []
        for i in range(0, maxrawthreads):
            tn = NetworkManagerIOThread(self.NMIORequestQueue)
            self.NMIOWorkerThreadPool.append(tn)
            tn.start()
    def setmanagers(self, managers):
        self.managers = managers
    def Request(self, IRO):
        self.NMIORequestQueue.put(IRO)

class NetworkManagerIOThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.daemon = True
    def run(self):
        while 1:
            IRO = self.queue.get()
            self.ProcessNetRequest(IRO)
            IRO.NetCallback(IRO)
            self.queue.task_done()
    def ProcessNetRequest(self, IRO):
        IRO.NetRequest = IRO.RequestData
        req = urllib2.Request(url=IRO.RequestData)
        res = urllib2.urlopen(req)
        IRO.NetResponse = res.read()