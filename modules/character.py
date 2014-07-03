from modules.dbobject import DBObject
from modules.helpers import *
from modules.html_helper import *
from psycopg2.extras import Json


class Character(DBObject):
    """docstring for Character"""
    def __init__(self, id=-1, name=''):
        super(Character, self).__init__()
        self.id = int(id)
        self.data = {}
        self.user_id = -1
        self.world_id = -1
        self.name = name
        print('Created character: ', self.id, self.name)

    def LoadRow(self, row):
        self.id = row['id']
        self.data = row['data']
        self.user_id = row['user_id']
        self.world_id = row['world_id']
        self.name = row['name']

    def Get(self, connection, id=-1, name=''):
        print(type(id), id)
        if int(id) > -1:
            self.id = int(id)
        if name != '':
            self.name = name
        if self.name == '' and self.id == -1:
            return False

        cur = connection.cursor()
        print('Type id: ', type(self.id))
        if self.id > -1:
            query = 'select * from characters where id = %s'
            cur.execute(query, (self.id, ))
        else:
            query = 'select * from characters where name = %s'
            cur.execute(query, (self.name, ))

        character = cur.fetchone()
        if character:
            self.LoadRow(character)
            return True
        return False

    def Save(self, connection):
        query = 'update characters set data = %s where id = %s'
        cur = connection.cursor()
        cur.execute(query, (self.data, self.id))
        connection.commit()

    def GenerateHtml(self, is_admin=False):
        print ('Generating personal')
        html = '<div class="character">'
        html += in_p(self.name, cls='name')
        for item_id in self.data:
            if item_id == 'stats':
                #level stats
                d = self.data[item_id]
                for stat_id, stat_val in\
                        sorted(d.items(),
                               key=lambda v: (Character._get_order(v[1]))):
                    #level group - variable, editable
                    item = stat_val
                    #self.data[item_id][stat_id]
                    print (item)

                    if 'name' in item:
                        item_name = str(item['name'])
                        html += in_div(item_name, 'item')
                    if 'value' in item:
                        item_value = str(item['value'])
                        html += in_div(item_value, 'value', item_id)
                    #item_editable = item['editable']
                    #item_is_inventory = item['is_inventory']
                    #item_type = item['item_type']

        html += '</div>'
        return html

    @staticmethod
    def _get_order(item):
        if item and 'order' in item:
            return item['order']
        return 999

    @staticmethod
    def New(connection, name, world, user):
        query = '''insert into characters(name, data, user_id, world_id) values
                (%s, %s, %s, %s)'''
        cur = connection.cursor()
        cur.execute(query, (name, Json(world.structure['character']), user.id, world.id))
        connection.commit()
        char = Character(name=name)
        char.Get(connection)
        return char

    @staticmethod
    def Create(connection, id):
        character = Character()
        if character.Get(connection, id):
            return character
        return None

    @staticmethod
    def FromRow(row):
        c = Character()
        print ("Char from row", row)
        c.LoadRow(row)
        return c
