from lib.utils import links_from_node_id
class Network():
    def __init__(self):
        """
        Instantiates an empty Network object.
        """
        self.nodes=set()
        self.links=[]

    @property
    def node_list(self):
        """
        List of all nodes' ids.
        """
        return [n.id for n in self.nodes]
    
    @property
    def edge_list(self):
        """
        Network representation as an edge list in the format [(from_node_id, to_node_id, weight), ...].
        """
        return [(link.from_node.id, link.to_node.id, link.metric) for link in self.links]

    @property
    def graph(self):
        """
        Directed graph representation of the network as a dictionary.

        Ex.:
        graph = {
            0: {1:10, 2:9, 3:1},
            1: {},
            2: {4:2},
            3: {0:1}
        }
        graph[from][to] = link_cost if it exists.
        """
        graph = {}
        for node in self.nodes:
            graph[node.id]={}
            for link in links_from_node_id(self, node.id):
                graph[node.id][link.to_node.id] = link.metric
        return graph

    def add_node(self, node):
        """
        Adds a Node object to the node set. Does not check for duplicate ids, uses set() instead.
        """
        self.nodes.add(node)
    
    def remove_node(self, node_id):
        """
        Removes a node from the network using the node_id to find it.
        """
        self.nodes.discard(self.get_node(node_id))

    def get_node(self, node_id):
        """
        Retrieves and returns a Node object based on the node id.
        """
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def add_link(self, link):
        """
        Adds a link to the list. Does not check for duplicates (in the future this will allow multiple links from same pair of nodes).
        """
        self.links.append(link)

    def remove_link(self, from_id, to_id):
        """
        Remodes a link from the edge list.
        
        Needs improvement to allow multiple links between same nodes.
        """
        link = self.get_link(from_id, to_id)
        if link in self.links:
            self.links.remove(link)
    
    def get_link(self, from_id, to_id):
        """
        Retrieves a link based on its from/to id pair.

        Needs improvement to allow multiple links between same nodes.
        """
        for link in self.links:
            if link.from_node.id == from_id and link.to_node.id == to_id:
                return link
        return None

    def update(self, packet):
        """
        Updates the state of the network by updating each individual link.
        """
        for link in self.links:
            link.update(packet)