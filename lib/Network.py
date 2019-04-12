from lib.utils import links_from_node_id, reset_flow_counter
class Network():
    """
    Container class that represents the network.

    Attributes:
        node_list (list): The list of unique node ids in the network.
        edge_list (list): The list of all links in the network in the form of `(from_id, to_id)`.
        graph (dict): Representation of the network as a `dict` format.
    """
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

        Parameters:
            node (Node): Node object to be added to the network.
        """
        self.nodes.add(node)
    
    def remove_node(self, node_id):
        """
        Removes a node from the network using the node_id to find it.

        Parameters:
            node_id (int): The unique id of a node in the network.
        """
        self.nodes.discard(self.get_node(node_id))

    def get_node(self, node_id):
        """
        Retrieves and returns a Node object based on the node id.

        Parameters:
            node_id (int): The unique id of a node in the network.
        """
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def add_link(self, link):
        """
        Adds a link to the list. Does not check for duplicates (in the future this will allow multiple links from same pair of nodes).

        Parameters:
            link (Link): Link object to be added to the network.
        """
        self.links.append(link)

    def remove_link(self, from_id, to_id):
        """
        Remodes a link from the edge list.
        
        Needs improvement to allow multiple links between same nodes.

        Parameters:
            from_id (int): The unique id of a node in the network.
            to_id (int): The unique id of a node in the network.
        """
        link = self.get_link(from_id, to_id)
        if link in self.links:
            self.links.remove(link)
    
    def get_link(self, from_id, to_id):
        """
        Retrieves a link based on its from/to id pair.

        Needs improvement to allow multiple links between same nodes.

        Parameters:
            from_id (int): The unique id of a node in the network.
            to_id (int): The unique id of a node in the network.
        """
        for link in self.links:
            if link.from_node.id == from_id and link.to_node.id == to_id:
                return link
        return None

    def update_with_packets(self, packets):
        """
        Updates the state of the network by updating each individual link for each packet in the list. Useful for multi-flow scenarios.

        Parameters:
            packets (list): List of packets from calls to `parse_trace_line(line)`.
        """
        for p in packets:
            self.update(p)

    def update(self, packet):
        """
        Updates the state of the network by updating each individual link.

        Parameters:
            packet (dict): From a call to `parse_trace_line(line)`.
        """
        for link in self.links:
            link.update(packet)
        reset_flow_counter(self)