#-------------------------------------------------------------------------------
# Name:        dataBase
# Author:      Dud
#-------------------------------------------------------------------------------
# coding=utf-8

import pymongo

class DbObject(object):
    def __init__(self, coll):   
        self.collectionName = coll
    
    def connect(self):
        try:
            self.con = pymongo.Connection()
            self.db = self.con.test
            self.coll = self.db[self.collectionName]
            self.isConnected = True
        except pymongo.errors.PyMongoError:
            self.isConnected = False
            print("DB connection failed")

    def addURL(self, url):
        if (self.isConnected):
            self.coll.insert(url)
        else:
            print("DB not connected")
            
    def find(self):
        if (self.isConnected):
            return self.coll.find()
        else:
            print ("DB not connected")
            

