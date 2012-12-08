#-------------------------------------------------------------------------------
# Name:        dataBase
# Author:      Dud
#-------------------------------------------------------------------------------
# coding=utf-8

import pymongo

class DbObject(object):
    """ Class managing a simplified pymongo database object, 
    providing only two methods : addURL (to add and element)
    and find (to find an element) """
    def __init__(self, coll):   
        self.collectionName = coll
        self.con            = None
        self.db             = None
        self.coll           = None
        self.isConnected    = False 
    
    def connect(self):
        """ Connects to the pymongo collection in the database """
        try:
            self.con = pymongo.Connection()
            self.db = self.con.test
            self.coll = self.db[self.collectionName]
            self.isConnected = True
        except pymongo.errors.PyMongoError:
            self.isConnected = False
            print("DB connection failed")

    def addURL(self, url):
        """ Add an URL to the database """
        if (self.isConnected):
            self.coll.insert(url)
        else:
            print("DB not connected")
            
    def find(self):
        """ Find an object in the database and returns it """
        if (self.isConnected):
            return self.coll.find()
        else:
            print ("DB not connected")
            

