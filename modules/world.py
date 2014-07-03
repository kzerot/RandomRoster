from modules.dbobject import DBObject
from modules.helpers import *
from modules.character import Character


class World(DBObject):
    """docstring for World"""
    def __init__(self, id=None, name=None, structure=None):
        super(World, self).__init__()
        self.id = -1
        self.name = ''
        self.structure = {}
        if id:
            self.id = id
            self.name = name
            self.structure = structure

    def LoadRow(self, row):
        self.id = row['id']
        self.name = row['name']
        self.structure = row['structure']

    def Get(self, connection, id):
        print (connection)
        print (connection.closed)
        query = 'select * from worlds where id = %s'
        cur = connection.cursor()
        print ('Executing: ')
        print (cur.mogrify(query, (id)))
        cur.execute(query, (id))
        world = cur.fetchone()
        print ('Fetched: ', world)
        if world:
            self.id = world['id']
            self.name = world['name']
            self.structure = world['structure']
            return True
        print ('Fethed nothing')
        return False

    @staticmethod
    def FromRow(row):
        c = World()
        c.LoadRow(row)
        return c

    @staticmethod
    def Create(connection, id):
        world = World()
        if world.Get(connection, id):
            return world
        return None

    @staticmethod
    def List(connection, user=None):
        query = 'select worlds.* from worlds'
        params = []
        if user and user.role != ADMIN:
            query += ' join characters on characters.world_id = worlds.id '
            query += ' join users on users.id = characters.user_id'
            query += ' where users.id = %s'
            params.append(user.id)
        cur = connection.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        result = [World.FromRow(w) for w in result]
        return result

    @staticmethod
    def CharactersByWorld(connection, world, user=None):
        query = 'select characters.* from characters'
        query += ' where characters.world_id = %(world_id)s'
        if user and user.role != ADMIN:
            query += ' and user_id = %(user_id)s'
        cur = connection.cursor()
        params = {"world_id": world.id}
        if user:
            params["user_id"] = user.id
        cur.execute(query, params)
        result = cur.fetchall()
        if result:
            return [Character.FromRow(r) for r in result]
        return []
