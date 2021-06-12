import psycopg2


class DBReader:
    def __init__(self, login_info):
        self.__login_info = login_info
        self.db = None
        self.cursor = None
        self._db_connect()

    def _db_connect(self):
        self.db = psycopg2.connect(host=self.__login_info['Host'],
                                   user=self.__login_info['User'],
                                   password=self.__login_info['Password'],
                                   dbname=self.__login_info["Database"])
        self.cursor = self.db.cursor()

    def db_search(self, sql, values=None):
        if values is None:
            values = {}
        self.cursor.execute(sql, values)
        result = self.cursor.fetchall()
        return result

    def db_close(self):
        self.db_close()
