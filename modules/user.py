from modules.dbobject import DBObject
from modules.helpers import *


class User(DBObject):
    """docstring for User"""
    def __init__(self):
        super(User, self).__init__()
        self.id = -1
        self.login = ''
        self.password = ''
        self.role = ''

    def Get(self, connection, login, password):
        query = 'select * from users where login = %s and password = %s'
        cur = connection.cursor()
        cur.execute(query, (login, password))
        user = cur.fetchone()
        if user:
            self.id = user['id']
            self.login = user['login']
            self.password = user['password']
            self.role = user['role']
            return True
        return False

    @staticmethod
    def Create(connection, login, password):
        user = User()
        if user.Get(connection, login, password):
            return user
        return None
