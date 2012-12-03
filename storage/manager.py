from threading import Thread
import Queue

class StorageManager():
    def __init__(self):
        from core import settings
        settings = settings.SettingsManager()
        self.connsettings = settings.get_default_storage()
        del settings

        self.IROID = 1
        self.IROActiveList = []
        self.IRONonActiveList = []

        self.db_type = self.connsettings[0][0]
        self.DBPreExecutionQueue = Queue.Queue(0)
        self.IORequestWorkerThreadPool = []

        self.driver = None
        if self.db_type == 'sqlite':
            from storage.drivers.SQLite import SQLiteConnector
            self.driver = SQLiteConnector(self.DBPreExecutionQueue)
        elif self.db_type == 'mysql':
            from storage.drivers.MySQL import MySQLConnector
            self.driver = MySQLConnector()

        if self.driver == None:
            raise IOError("Error initializing database driver")

        self.driver.DBDSetPreExecutionQ(self.DBPreExecutionQueue)

    def connect(self):
        return self.driver.connect()
    def execute(self, IRO):
        self.DBPreExecutionQueue.put(IRO)
    def create(self):
        return self.driver.create()
    def importdb(self, data):
        return self.driver.importdb(data)
    def exportdb(self):
        #returns a python object
        return self.driver.exportdb()
    def setmanagers(self, managers):
        self.managers = managers
        self.driver.setmanagers(managers)
    def transfer(self):
        if self.db_type == 'sqlite':
            from storage.drivers.MySQL import MySQLConnector
            self.newdriver = MySQLConnector
        elif self.db_type == 'mysql':
            from storage.drivers.SQLite import SQLiteConnector
            self.newdriver = SQLiteConnector
        success = self.newdriver.transferfrom(self.driver)
        if success:
            del self.driver
            self.driver = self.newdriver
            self.driver.setmanagers(self.managers)
            self.driver.DBDSetPreExecutionQ(self.DBPreExecutionQueue)
            self.db_type = self.driver.__db_type__
            self.driver.DBDStartWorkerThreads()
        else:
            raise IOError("Could not transfer database")
    def Request(self, IRO):
        IRT = IORequestThread(self.managers, IRO)
        self.IORequestWorkerThreadPool.append(IRT)
        IRT.start()
    def RegisterIROForDebug(self, IRO):
        self.IROActiveList.append(IRO)
        IRO.__id__ = self.IROID
        self.IROID = self.IROID + 1
    def UnregisterIROForDebug(self, IRO):
        self.IROActiveList.remove(IRO)
        self.IRONonActiveList.append(IRO)

class IORequestThread(Thread):
    def __init__(self, managers, IRO):
        Thread.__init__(self)
        self.managers = managers
        self.IRO = IRO
        self.daemon = True
    def run(self):
        self.IRO
        self.managers.StorageManagerInst.execute(self.IRO)
    def IOProcessResponse(self):
        self.IRO.RequestRealCallback(self.IRO)

class IORequestObject(object):
    def __init__(self, requesttype, callback, requestdata = None, SM = None):
        if (requestdata == None ) and (requesttype == IORequestType.EditFeed):
            raise IOError("Could not inialize RSSFeedRequest object. Cannot edit a non-existant feed.")
        self.__id__ = None
        self.RequestType = requesttype
        self.RequestData = requestdata
        self.RequestCallback = callback
        self.RequestRealCallback = callback #backup callback to allow for overriding primary callback to filer responses
        self.ResponseData = None
        self.RequestProcessingTrash = []
        self.NetRequest = None
        self.NetResponse = None
        self.NetCallback = callback
        self.SQLIO = None
        if SM != None:
            SM.RegisterIROForDebug(self)
    def __repr__(self):
        return '<%s.%s at %s>' % (self.__class__.__module__, self.__class__.__name__, hex(id(self))) + " \r\n{ \r\n\tID: " + str(self.__id__) + "\r\n\tRequestType: " + str(self.RequestType) + "\r\n\tRequestData: " + str(self.RequestData) + "\r\n\tResponseData: " + str(self.ResponseData) + "\r\n\tNetResponse: " + str(self.NetResponse) + "\r\n}"
        
class IORequestType:
    WriteFeed = 0
    ReadFeed = 1
    EditFeed = 2
    ReadFeedFromName = 3
    ReadAllFeeds = 4
