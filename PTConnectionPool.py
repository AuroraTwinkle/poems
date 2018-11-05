import pymysql
from DBUtils.PooledDB import PooledDB
import config as Config

class PTConnectionPool(object):
    __pool = None

    def __enter__(self):
        self.conn = self.getConn()
        self.cursor = self.conn.cursor()
        return self

    def getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=Config.DB_MIN_CACHED, maxcached=Config.DB_MAX_CACHED,
                                   maxshared=Config.DB_MAX_SHARED, maxconnections=Config.DB_MAX_CONNECYIONS,
                                   blocking=Config.DB_BLOCKING, maxusage=Config.DB_MAX_USAGE,
                                   setsession=Config.DB_SET_SESSION,
                                   host=Config.HOST, port=Config.PORT,
                                   user=Config.USERNAME, passwd=Config.PASSWORD,
                                   db=Config.DATABASENAME, use_unicode=True)

        return self.__pool.connection()

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


def getPTConnection():
    return PTConnectionPool()
