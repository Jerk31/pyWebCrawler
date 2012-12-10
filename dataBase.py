import pymongo

class DbObject(object):
    def __init__(self):   
        self.collectionName = "pyWebCrawler"
    
    def connect(self):
        try:
            self.con = pymongo.Connection()
            self.db = self.con.test
            self.coll = self.db[self.collectionName]
            self.isConnected = True
        except pymongo.errors.PyMongoError:
            self.isConnected = False
            print("DB connection failed")

    def addURL(self, url, depth, stats, imgPath):
        if (self.isConnected):
            self.coll.insert({"url": url, "depth": depth, "stats": stats, "imgPath": imgPath})
        else:
            print("DB not connected")
            
    def findURL(self, url, depth):
        if (self.isConnected):
            return self.coll.find_one({"url": url, "depth":depth})
        else:
            print ("DB not connected")
            

