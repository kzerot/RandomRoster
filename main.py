import tornado.ioloop
import tornado.web
#import psycopg2
from psycopg2.extras import DictConnection
#DictCursor
from modules.user import User
from modules.world import World
from modules.character import Character
from modules.helpers import *
import os
#Base settings
dbname = 'rosters'
host = 'evillord.ru'
username = 'roster'
password = 'q1w2e3'

dburi = "dbname=%s host=%s user=%s password=%s" %\
    (dbname, host, username, password)


class BaseHandler(tornado.web.RequestHandler):
    connection = None

    def Connection(self):
        if not BaseHandler.connection or\
           BaseHandler.connection.closed:
            BaseHandler.connection = DictConnection(dburi)
        return BaseHandler.connection

    def get_current_user(self):
        login = self.get_secure_cookie("login")
        password = self.get_secure_cookie("password")
        if login and password:
            user = User.Create(self.Connection(),
                               login.decode('utf-8'),
                               password.decode('utf-8'))
            if user:
                return user.login
        return None

    def get_user(self):
        login = self.get_secure_cookie("login")
        password = self.get_secure_cookie("password")
        if login and password:
            user = User.Create(self.Connection(),
                               login.decode('utf-8'),
                               password.decode('utf-8'))
            if user:
                return user


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_user()
        items = menuItems[user.role]
        self.render("menu.html", menuitems=items)


class WorldsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, world_id=None):
        user = self.get_user()
        if not world_id:
            items = World.List(self.Connection(), user)
            self.render("worlds.html", worlds=items)
        else:
            w = World.Create(self.Connection(), world_id)
            if user.role == ADMIN:
                chars = World.CharactersByWorld(self.Connection(), w)
                self.render("world.html", world=w, characters=chars)
            else:
                chars = World.CharactersByWorld(self.Connection(), w, user)
                self.render("characters.html", world=w, user=user,
                            characters=chars)


class CharactersHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, character_id=None):
        user = self.get_user()
        if not character_id:
            self.write("NO CHARACTERS")
        else:
            char = Character.Create(self.Connection(), character_id)
            self.render("character.html", user=user,
                        character=char)


class CreateCharacterHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_user()
        worlds = World.List(self.Connection())
        self.render("createcharacter.html", worlds=worlds)

    @tornado.web.authenticated
    def post(self):
        print('Receive', self.request.body)
        user = self.get_user()
        data = tornado.escape.json_decode(self.request.body)
        self.content_type = 'application/json'
        if data and "name" in data:
            print ('New character\'s name', data["name"])
            w = World.Create(self.Connection(), data["world"])
            character = Character.New(self.Connection(), data["name"], w, user)
            if character and character.id >= 1:
                self.write({'result': True, 'char_id': character.id})
            else:
                self.write({'result': False})
        else:
            self.write({'result': False})


class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="login">'
                   'Password: <input type="text" name="password">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        print ('Try login with credits: %s, %s' % (login, password))
        user = User.Create(self.Connection(), login, password)
        if user:
            self.set_secure_cookie("login", login)
            self.set_secure_cookie("password", password)
            print ("Success")
        else:
            print ("Login failed with creditials: %s, %s" % (login, password))
        self.redirect("/")


settings = {
    "cookie_secret": "68468464648648684684684dfsgdsfgsdfg",
    "login_url": "/login",
    "debug": True
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/worlds", WorldsHandler),
    (r"/worlds/([0-9]+)", WorldsHandler),
    (r"/characters/([0-9]+)", CharactersHandler),
    (r"/createcharacter", CreateCharacterHandler),
    (r"/login", LoginHandler),
],
static_path=os.path.join(os.path.dirname(__file__), "static"),
template_path=os.path.join(os.path.dirname(__file__), "templates"),
**settings)

if __name__ == "__main__":
    application.listen(8888)

    def fn():
            print ("Hooked before reloading...")
    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
