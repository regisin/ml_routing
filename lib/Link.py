from lib.utils import distance


class Link:
    """ 
    This is a class represents a link of a network and keeps its link state information.
      
    Attributes:
            from_node (Node): The source node of the link.
            to_node (Node): The destination node of the link.
            error_probability (float): Probability of error in the link [0, 1].
            datarate (float): Datarate of the link in Mbps.
            metric (float): Custom metric/weight for the given link, the return value from _metric(self) pointer.
            distance (float): Euclidean distance between `from_node.position` and `to_node.position`.
            _metric (pointer): Function that computes an arbitrary metric/weight for the given link.
    """
    def __init__(self, metric, from_node, to_node, error_probability=0.1, datarate=1.0):
        """
        Creates a link instance.

        Parameters:
            metric (pointer): Function that computes an arbitrary metric/weight for the given link.
            from_node (Node): The source node of the link.
            to_node (Node): The destination node of the link.
            error_probability (float): Probability of error in the link [0, 1].
            datarate (float): Datarate of the link in Mbps.
        """
        self.from_node = from_node
        self.to_node = to_node
        self.error_probability = error_probability
        self.datarate = datarate
        self.metric = float('inf')
        self._metric = metric
        self.update(None)
    
    @property        
    def distance(self):
        """
        The current distance between the nodes of this link.
        """
        return distance((self.from_node.x, self.from_node.y, self.from_node.z),
                        (self.to_node.x, self.to_node.y, self.to_node.z))

    def update_metric(self):
        """
        Updates the custom metric (used for computing shortest paths).
        """
        self.metric = self._metric(self)

    def update(self, packet):
        """
        Updates the state of itself and its aggregated nodes.
        
        Parameters:
            packet (dict): From a call to `parse_trace_line(line)`.
        """
        self.update_metric()
        if packet is not None:
            self.from_node.update(packet, self)
            self.to_node.update(packet, self)
