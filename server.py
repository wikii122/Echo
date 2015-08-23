#!/usr/bin/env python3
import cherrypy


class Token:
    """
    Manages token authentication
    """
    def __init__(self):
        pass  # TODO load resources

    def index(self):
        return "OK"
    index.exposed = True


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

    cherrypy.tree.mount(
        Game(), '/game',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.tree.mount(Token(), '/token')

    cherrypy.engine.start()
    cherrypy.engine.block()
