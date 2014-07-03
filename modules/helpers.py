ADMIN = 0
USER = 1

roles = {ADMIN: 'admin', USER: 'user'}


class MenuItem(object):
    def __init__(self, url, name):
        self.url = url
        self.name = name

menuItems = {ADMIN: [
    MenuItem('worlds', 'Enter world'),
    MenuItem('addplayer', 'Add new player'),
], USER: [
    MenuItem('worlds', 'Присоединиться к игре'),
    MenuItem('createcharacter', 'Создать нового персонажа'),
]}
