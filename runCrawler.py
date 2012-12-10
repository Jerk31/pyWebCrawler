import sys
from pyWebCrawler import Fetcher, Crawler
from tools import *
from graph import Generate_Graph, Display_Graph

import dataBase as dB
import pymongo

def main(url, stopVal, depth):
	if len(sys.argv) != 4:
		print len(sys.argv)
		print ("ERROR: wrong argument number! \n")
		print EOF
	# Global variable containing all the URLS following this scheme of node
	# { "http_url", {"toCrawl" : bool, "parent" : "http_parent"} }
	urls = dict()
	# Global variable containing the final tree of all the urls following this scheme
	# { "parent" : { "child1" : {}, "child2" : { "subchild1" : {} } }
	tree = dict()
	### Verifying data
	if depth == "":
		depth = None
	if stopVal == "":
		stopVal = None
	if not (url.startswith("http") or url.startswith("https")):
		print "Invalid webpage"
		sys.exit(42)
	try:
		depth = int(depth)
	except:
		if depth != None:
			print "Invalid depth"
			sys.exit(42)
	if depth == 0:
		depth = None
	# Connecting to the db
	db0 = dB.DbObject()
	db0.connect()
	
	item = db0.findURL(url, depth)
	if item:
		print "======= Url found in the database ======="
		path = item["imgPath"]
		stats = item["stats"]
	else:
		c = Crawler(url, urls, stopVal, depth)
		c.crawl()
		urls_to_tree(url, urls, tree)
		print "======= Displaying the tree =========\n"
		print len(tree)
		for i in tree.items():
			print i
		print "======= Number of urls found : ", len(urls), " ========\n"
		graph = Generate_Graph(url, urls, tree).graph
		path = Display_Graph(url, graph).path
		db0.addURL(url, depth, [], path)
		
	print EOF
	
if __name__ == '__main__':
	# Map command line arguments to function arguments.
	main(*sys.argv[1:])
