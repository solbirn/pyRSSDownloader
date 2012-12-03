import sqlite3
class SettingsManager:
    def __init__(self):
        self.conn = None
        self.rssdbs = None
        self.load()
        #print self.rssdbs
        return
    def setmanagers(self, managers):
        self.managers = managers
    def load(self):
        #TODO Pull from db
        self.DLDir = "C:\\RSSFeedDownloads\\"
        try:
            self.conn = sqlite3.connect("settings", check_same_thread = False)
            getrssdbsql = "select * from connections"
            c = self.conn.cursor()
            c.execute(getrssdbsql)
            self.rssdbs = c.fetchall()
            self.conn.close()
        except sqlite3.OperationalError:
            print "in ex"
            self.create_settings_db()
            self.conn = sqlite3.connect("settings", check_same_thread = False)
            getrssdbsql = "select * from connections"
            c = self.conn.cursor()
            c.execute(getrssdbsql)
            self.rssdbs = c.fetchall()
            self.conn.close()
    def create_settings_db(self):
        sqlite3.connect("settings")
        c = self.conn.cursor()
        c.executescript("""
                    create table connections(
                        type,
                        hostname,
                        port,
                        user,
                        password,
                        database
                    );
                    """)
        self.conn.commit()
        defaultvals = ("sqlite", "", "", "", "", "rssfeedsdb")
        c.execute("insert into connections (type, hostname, port, user, password, database) values (?,?,?,?,?,?)", defaultvals)
        self.conn.commit()
    def get_default_storage(self):
        return self.rssdbs