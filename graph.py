# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt

class Generate_Graph(object):
    """ Class generating the datas for the graph by providing it
    the urls and tree dictionnaries """
    def __init__(self, root, urls, tree):
        # Initialisations
        self.root   = root
        self.urls   = [url for (url, prop) in urls.items()]
        self.tree   = tree
        self.graph  = nx.Graph()
        self.colors = ["red", "blue", "green", "orange", "violet", "purple", "black"]
        self._i     = 1
        self._dec   = False
        # Calling generate
        self._generate()
        
    def _generate(self):
        """ Generates internally the graph in the self.graph variable """
        # Adding root node
        self.graph.add_node(self.root, color=self.colors[0])
        # Adding all the nodes
        self.graph.add_nodes_from(self.urls)
        # Connecting the nodes
        self._add_edges(self.root, self.tree)
        # Colors for the nodes
        self._add_node_colors(self.tree)
        
    def _add_edges(self, root, tree):
        """ Recursive function : add all the edges to the graph """
        if tree != {}:
            for k in tree.keys():
                self.graph.add_edge(root, k)
                self._add_edges(k, tree[k])
                
    def _add_node_colors(self, tree):
        """ Recursive function : add colors for the nodes """
        if tree != {}:
            self._i += 1
            for k in tree.keys():
                self.graph.node[k]["color"] = self.colors[self._i]
                self._add_node_colors(tree[k])
            self._i -= 1
                
class Display_Graph(object):
    """ Class generating a PNG of the graph by providing it the graph datas """
    def __init__(self, root, graph):
        # Initialisations
        self.root  = root
        self.graph = graph
        # Calling display
        self._display()
        
    def _display(self):
        """ Generates the PNG of the graph by using the graph data
        previously calculated """
        # Calculating positions
        pos = nx.spring_layout(self.graph)
        # Adding colors for all the nodes
        for n in self.graph.nodes():
            if "color" in self.graph.node[n].keys():
                nx.draw_networkx_nodes(self.graph, pos, nodelist = [n], node_color=self.graph.node[n]["color"])
        # Adding edges
        nx.draw_networkx_edges(self.graph, pos)
        # Adding labels
        nx.draw_networkx_labels(self.graph, pos)
                
        # Putting a title (only if we have margins)
        plt.title("Crawling " + str(self.root))
        # Putting a window title
        plt.figure(1).canvas.set_window_title('Crawling ' + str(self.root)) 
        # Hidding x and y axes
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        # Adjusting margins
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0) # 0 < value < 1 (if we want margins, just put 0.1 and 0.9 for ex)
        # Showing the graph
        ## plt.show()
        
        # just saving a graph to disk, the way it is done should be
        # and we need a way to dynamically show the .png on the page 
        plt.savefig("html/graph.png")
