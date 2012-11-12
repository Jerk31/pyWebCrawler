#-------------------------------------------------------------------------------
# Name:        dataBase
# Purpose:
#
# Author:      Dud
#
# Created:     11-11-2012
# Copyright:   (c) Dud 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pymongo

def main():
    pass

if __name__ == '__main__':
    main()

class DbObject(object):
    def connect(self):
        try:
            self.con = pymongo.Connection()
            self.db = self.con.test
            self.coll = self.db.test2
            self.isConnected = True
        except pymongo.errors.PyMongoError:
            self.isConnected = False
            print("DB connection failed")


    def addURL(self, url):
        if (self.isConnected):
            self.coll.insert(url)
        else:
            print("DB not connected")

