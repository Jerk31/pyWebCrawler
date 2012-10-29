# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt

class Generate_Graph(object):
    def __init__(self, root, urls, tree):
        # Initialisations
        self.root   = root
        self.urls   = [url for (url, prop) in urls.items()]
        self.tree   = tree
        self.graph  = nx.Graph()
        self.colors = ["red", "blue", "green", "black", "orange", "violet", "purple"]
        self._i     = -1
        # Calling generate
        self._generate()
        
    def _generate(self):
        # Adding root node
        self.graph.add_node(self.root, color='blue')
        # Adding all the nodes
        self.graph.add_nodes_from(self.urls)
        # Connecting the nodes
        self._add_edges(self.root, self.tree)
        
    def _add_edges(self, root, tree):
        # Recursive function : add all the edges
        if tree != {}:
            for k in tree.keys():
                self.graph.add_edge(root, k)
                self._add_edges(k, tree[k])
                
    def _add_node_colors(self, tree):
        # Recursive function : add colors for the nodes
        if tree != {}:
            self._i += 1
            for k in tree.keys():
                self.graph.node[k]["color"] = self.colors[self._i]
                self._add_node_colors(k, tree[k])
                self._i -= 1
                
class Display_Graph(object):
    def __init__(self, graph):
        # Initialisations
        self.graph = graph
        # Calling display
        self._display(self.graph)
        
    def _display(self, graph):
        # Colors for all the nodes : TODO : TO DEBUG
        for n in self.graph.nodes():
            if "color" in self.graph.node[n].keys():
                nx.draw_networkx_nodes(self.graph, nx.spring_layout(self.graph), nodelist = [n], node_color=self.graph.node[n]["color"])
        # Drawing the graph and displaying it
        nx.draw(self.graph)
        plt.show()
