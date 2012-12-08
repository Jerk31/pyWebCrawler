# coding=utf-8

import urllib2
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
        """ Add the headers to tell the website who we are """
        request.add_header("User-Agent", AGENT)

    def open(self):
        """ Opens the url with urllib2 """
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
        except IOError:
            return None
        return (request, handle)
        
    def fetch(self):
        """ Main function of the fetcher, will try to find the href 
        attributes inside the a tags and add them to the urls dictionnary """
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
        """ Main function of the crawler, will crawl a website and fill the
        urls dictionnary with the urls found in the website """
        # Number of urls we have crawled
        counter = 0
        # Looks at the links in the root page
        page = Fetcher(self.root, self.urls, self.end)
        page.fetch()
        
        print 'starting crawling'
        
        # Urls remaining to crawl
        to_crawl = [d for d in self.urls if self.urls[d]["toCrawl"] == True]
        while to_crawl != [] and (self.depth > 0 or self.depth == None):
            # For all the URLS remaining to crawl, we fetch it to take all the links
            for url in to_crawl:
                counter += 1
                print "\n"
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
            print "Remaining : ", self.remaining, " url(s) to crawl!", "\n"
            print "Depth = ", self.depth, "\n"
