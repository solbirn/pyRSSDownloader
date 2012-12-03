import sqlite3, Queue, types
from storage.manager import IORequestObject, IORequestType
from threading import Thread

class SQLiteConnector:
    def __init__(self, PEQ):
        self.PEQ = PEQ
    def realinit(self):
        self.__db_type__ = "sqlite"
        self.DBDPreExecutionThread = self.managers.RSSFeedManagerInst.DBDPreExecutionThread
        self.DBDSetPreExecutionQ(self.PEQ)
        self.DBDExecutionQueue = Queue.Queue(0)
        self.DBDPreExecutionWorkerThreadPool = []
        for i in range(1, 2):
            tpe = self.DBDPreExecutionThread(self)
            self.DBDPreExecutionWorkerThreadPool.append(tpe)
            tpe.start()
        self.DBDExecutionWorkerThreadPool = []
        for i in range(1, 2):
            te = DBDExecutionThread(self)
            self.DBDExecutionWorkerThreadPool.append(te)
            te.start()
    def connect(self, db="pyrssdl"):
        try:
            conn = sqlite3.connect(db, check_same_thread = False)
            c = conn.cursor()
            c.execute("select * from settings")
            return conn
        except sqlite3.OperationalError, e:
            print e
            conn.close()
            self.create()
            return sqlite3.connect(db, check_same_thread = False)

    def create(self):
        conn = sqlite3.connect("pyrssdl", check_same_thread = False)
        c = conn.cursor()
        try:
            c.execute("select * from settings")
        except sqlite3.OperationalError, e:
            c.executescript(self.managers.RSSFeedManagerInst.RSSFeedSource.SQLScripts["create"])
            conn.commit()
    def execute(self, action, data, callback):
        
        return
    def importdb(self, data):
        return
    def exportdb(self):
        #returns a python object
        return
    def setmanagers(self, managers):
        self.managers = managers
        self.realinit()
    def DBDSetPreExecutionQ(self, Q):
        self.DBDPreExecutionQueue = Q
    def transferfrom(self, olddriver):
        return

class DBDExecutionThread(Thread):
    def __init__(self, parentconnector):
        Thread.__init__(self)
        self.driver = parentconnector
        self.conn = self.driver.connect()
        self.daemon = True
    def run(self):
        while 1:
            IRO = self.driver.DBDExecutionQueue.get()
            IRO.ResponseData = self.executesql(IRO.SQLIO)
            IRO.RequestCallback(IRO)
            self.driver.DBDExecutionQueue.task_done()
    def executesql(self, sql):
        c = self.conn.cursor()
        responses = []
        for query in sql:
            #print "Query: ", query
            try:
                c.execute(query)
                self.conn.commit()
                responses.append(c.fetchall())
            except Exception, e:
                responses.append({query:e})
                pass
        return responses