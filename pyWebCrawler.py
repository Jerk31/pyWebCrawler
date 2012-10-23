# coding=utf-8
# http://code.activestate.com/recipes/576551-simple-web-crawler/
# https://bitbucket.org/kuytu/crawlpy/src/5383922384ba7150c5bd4017009bf53810b7dfbb/crawlPy.py?at=default

import urllib2
import urlparse
import sys
from cgi import escape
from BeautifulSoup import BeautifulSoup

__version__ = "0.1"
AGENT = "%s/%s" % (__name__, __version__)

class Fetcher(object):
    """ This class is designed to Fetch an URL and take all the links on the distant-page.
        It will add the new urls to the URLS variable """
        
    def __init__(self, url, urls, end):
        self.url = url
        self.urls = urls
        self.end = end
        
    def _addHeaders(self, request):
        # Add the headers to tell the website who we are
        request.add_header("User-Agent", AGENT)

    def open(self):
        # Opens the url with urllib2
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
        except IOError:
            return None
        return (request, handle)
        
    def fetch(self):
        tags = []
        request, handle = self.open()
        self._addHeaders(request)
        if handle:
            try:
                # Reads the page and pass it to BS
                content = unicode(handle.open(request).read(), "utf-8", errors="replace")
                soup = BeautifulSoup(content)
                # Searchs all the 'a' tags in the page
                tags = soup('a')
            except urllib2.HTTPError, error:
                if error.code == 404:
                    print "ERROR: %s -> %s" % (error, error.url)
                else:
                    print "ERROR: %s" % error
            except urllib2.URLError, error:
                print "ERROR: %s" % error
                
            # Iterate over all the 'a' tags to find the 'href' attributes
            for tag in tags:
                href = tag.get("href")
                # We dont need pdfs and no "false-links" and no url we have already
                if (href is not None) and (href not in self.urls) and ("pdf" not in href):
                    # We only need http or https urls
                    if href.startswith("http://") or href.startswith("https://"):
                        url = urlparse.urljoin(self.url, escape(href))
                        self.urls[href] = dict()
                        self.urls[href]["parent"] = self.url
                        # If the URL in INSIDE our website, we keep it for the crawling
                        # Else it's here but we will not crawl it
                        # Self.end given by the user
                        if self.end in href:
                            self.urls[href]["toCrawl"] = True
                        else:
                            self.urls[href]["toCrawl"] = False
                                        
    
class Crawler(object):
    """ This class is designed to crawl a website, starting at the root point and deeping until the depth.
        If the depth is None, it will crawl all the website.
        The default ending condition is the root point, we don't want to crawl all the web..."""
        
    def __init__(self, root, urls, ending_condition=None, depth=None):
        self.root = root
        self.urls = urls
        self.depth = depth
        self.remaining = -1
        if ending_condition is None:
            self.end = self.root
        else:
            self.end = ending_condition
        
    def crawl(self):
        # Number of urls we have crawled
        counter = 0
        # Looks at the links in the root page
        page = Fetcher(self.root, self.urls, self.end)
        page.fetch()
        
        # Urls remaining to crawl
        to_crawl = [d for d in self.urls if self.urls[d]["toCrawl"] == True]
        while to_crawl != [] and (self.depth > 0 or self.depth == None):
            # For all the URLS remaining to crawl, we fetch it to take all the links
            for url in to_crawl:
                counter += 1
                print "Fetching url : ", url, " (", counter, "/", self.remaining, ")"
                page = Fetcher(url, self.urls, self.end)
                self.urls[url]["toCrawl"] = False
                page.fetch()
            
            # At the end we decrease the depth : if it's equal to 0, it stops the crawling
            if self.depth is not None:
                self.depth -= 1
            # Updating the urls to crawl
            to_crawl = [d for d in self.urls if self.urls[d]["toCrawl"] == True]
            self.remaining = len(to_crawl)
            counter = 0
            print "Remaining : ", self.remaining, " url(s) to crawl!"
            print "Depth = ", self.depth
            
            
def search_parent(parent, url, tree):
    """ Recrusive function to add the url as a child of the parent """
    if tree != {}:
        for k in tree.keys():
            if parent == k:
                tree[k][url] = {}
                return True
            else:
                search_parent(parent, url, tree[k])
    else:
        return False                          
            
def urls_to_tree(urls, tree):
    """ Takes the URLS structure and creates a tree structure as parent -> children """          
    for (url, prop) in urls.items():
        if prop["parent"] == url:
            tree[url] = dict()
        else:
            if not search_parent(prop["parent"], url, tree):
                tree[prop["parent"]] = {url:{}}
                

# Global variable containing all the URLS following this scheme of node
# { "http_url", {"toCrawl" : bool, "parent" : "http_parent"} }
urls = dict()
# Global variable containing the final tree of all the urls following this scheme
# { "parent" : { "child1" : {}, "child2" : { "subchild1" : {} } }
tree = dict()

#######################################################################
# Starting point of the crawler : ask the user what he wants to crawl
http = raw_input("What webpage do you want to crawl [http(s) page]? ")
ending = raw_input("What is the ending condition [str]? ")
deep = raw_input("How deeper [int] do you want to go (None = infinite)? ")

# Verifying datas
if deep == "":
    deep = None
if ending == "":
    ending = None
if not (http.startswith("http") or http.startswith("https")):
    print "Invalid webpage"
    sys.exit(42)
try:
    deep = int(deep)
except:
    if deep != None:
        print "Invalid deep"
        sys.exit(42)
    
# Starts the crawler    
c = Crawler(http, urls, ending, deep)
c.crawl()
             
# Creates the tree structure using the URLS found previously
urls_to_tree(urls, tree)

# To debug : prints the tree at the end and the number of urls found
print "\n======= Finished, displaying the tree ========="
for i in tree.items():
    print i     
print "\n======= Number of urls found : ", len(urls), " ========"
