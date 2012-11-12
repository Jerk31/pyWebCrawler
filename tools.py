# coding=utf-8
urls_found = list()

def search_parent(parent, url, tree):
    """ Recrusive function to add the url as a child of the parent """
    if tree != {}:
        for k in tree.keys():
            if parent == k:
                if url not in urls_found:
                    tree[k][url] = {}
                    urls_found.append(url)
                return True
            else:
                search_parent(parent, url, tree[k])
    else:
        return False                          
            
def urls_to_tree(root, urls, tree):
    """ Takes the URLS structure and creates a tree structure as parent -> children """          
    urls_found.append(root)
    for (url, prop) in urls.items():
        if prop["parent"] == url:
            if url not in urls_found:
                tree[url] = dict()
                urls_found.append(url)
        else:
            if not search_parent(prop["parent"], url, tree):
                if (url not in urls_found) and (prop["parent"] not in urls_found):
                    tree[prop["parent"]] = {url:{}}
                    urls_found.append(prop["parent"])
                    urls_found.append(url)
                    
def insert_database(urls, db):
    """ Insert the urls into the database we're currently working with """
    for (url, prop) in urls.items():
        db.addURL({"url" : url, "parent" : prop["parent"]})
        
def read_database(urls, db):
    """ Reads the database we're currently working with and re-creates the urls tree """
    for e in db.find():
        del e['_id']
        urls[e["url"]] = {"parent" : e["parent"]}
