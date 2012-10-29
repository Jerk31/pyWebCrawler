# coding=utf-8

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
