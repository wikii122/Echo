#!/usr/bin/env python3
import cherrypy
import pymongo
import random


client = pymongo.MongoClient('mongo', 27017)
db = client["TTR"]

class Token:
    """
    Manages token authentication
    """
    def __init__(self):
        with open("./res/dict.txt") as wordlist:
            self.words = wordlist.readlines()

    @cherrypy.expose
    def index(self):
        idx = ' '.join(random.sample(self.words, 2))
        return idx


class Game:
    """
    Manages game state.
    """
    exposed = True

    def GET(self, id=None):
        pass

    def POST(self, id=None):
        pass

    def PUT(self, id=None):
        pass

    def DELETE(self, id=None):
        pass

if __name__ == '__main__':
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.tree.mount(
        Game(), '/game',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.tree.mount(Token(), '/token')

    cherrypy.engine.start()
    cherrypy.engine.block()
