#!/usr/bin/env python3
import cherrypy
import datetime
import pymongo
import random
import json


# Assume docker links from docker compose
client = pymongo.MongoClient('mongo', 27017)
db = client["echo"]
db.data.create_index("time", expireAfterSeconds=60*60*24)

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

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            raise cherrypy.HTTPError(404)

        collection = db["data"]
        json = collection.find_one({"token": id})
        if json is None:
            raise cherrypy.HTTPError(404)
        return json["data"]


    @cherrypy.tools.json_out()
    def POST(self, id=None):
        if id is None:
            raise cherrypy.HTTPError(404)

        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody.decode("utf-8"))
        d = {
                "data": body,
                "time": datetime.datetime.now(),
                "token": id
        }
        collection = db["data"]
        if collection.find({"token": id}).count() != 0:
            raise cherrypy.HTTPError(409)

        collection.insert_one(d)

        return {
            "token": id,
            "status": "created"
        }

    @cherrypy.tools.json_out()
    def PUT(self, id=None):
        if id is None:
            raise cherrypy.HTTPError(404)
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody.decode("utf-8"))
        collection = db["data"]
        if collection.find({"token": id}).count() == 0:
            raise cherrypy.HTTPError(404)
        collection.update_one({"token": id}, {"$set": {"data": body, "time": datetime.datetime.now()}})

        return {
            "token": id,
            "status": "updated"
        }


    @cherrypy.tools.json_out()
    def DELETE(self, id=None):
        if id is None:
            raise cherrypy.HTTPError(404)
        collection = db["data"]
        if collection.find({"token": id}).count() == 0:
            raise cherrypy.HTTPError(404)
        collection.remove({"token": id})
        return {
            "token": id,
            "status": "removed"
        }


if __name__ == '__main__':
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.tree.mount(
        Game(), '/data',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.tree.mount(Token(), '/token')

    cherrypy.engine.start()
    cherrypy.engine.block()
