from lib.utils import parse_trace_line

from random import randint, choice


class Flow:
    """
    Template class that represents a data flow in the network.
    """
    def __init__(self, from_node, to_node):
        raise NotImplementedError

    @property
    def current_packet(self):
        """
        Returns the current packet in the pipeline.
        """
        raise NotImplementedError

    @property
    def packets_left(self):
        """
        The number of packets left (including the `current_frame`).
        """
        raise NotImplementedError

    @property
    def has_packets_left(self):
        """
        Returns True if there are more packets left, False otherwise.
        """
        raise NotImplementedError

    def next(self):
        """
        Increases the `current_index` by 1 and return the next frame in the list.
        """
        raise NotImplementedError


class RandomFlow(Flow):
    """
    Represents an infinite data flow.
    """
    def __init__(self, from_node, to_node, min_size=500, max_size=3000, time_interval=100, type_list=None):
        self.from_node = from_node
        self.to_node = to_node
        self.max_size = max_size
        self.min_size = min_size
        self.type_list = type_list
        self.time_interval = time_interval
        self.type_list = ['I', 'P', 'B']
        if type_list is not None:
            self.type_list = type_list
        self.current_index = -1
        self.next()

    @property
    def packets_left(self):
        """
        Always has another packet to generate. Returns always >= 1.
        """
        return 1

    @property
    def has_packets_left(self):
        """
        Always has another packet to generate.
        """
        return True

    def next(self):
        """
        Generates a new random packet.
        """
        self.current_index += 1
        self.current_packet = {
            'index': int(self.current_index),
            'size': int(randint(self.min_size, self.max_size)),
            'type': choice(self.type_list),
            'time': int(self.current_index * self.time_interval),
        }
        return self.current_packet


class TraceFlow(Flow):
    """ 
    This class represents a data flow in the network.

    Attributes:
            from_node (Node): The source node of the link.
            to_node (Node): The destination node of the link.
            trace_file (string): File path of the trace file this flow will read from.
            start_index (int): The starting point of the flow, i.e. the line in the trace file to start reading from.
    """
    def __init__(self, from_node, to_node, trace_file, start_index=0):
        """
        Creates a flow instance from a given trace file. Parses file and stores values into memory, careful with big files.

        Parameters:
            from_node (Node): The source node of the link.
            to_node (Node): The destination node of the link.
            trace_file (string): File path of the trace file this flow will read from.
            start_index (int): The starting point of the flow, i.e. the line in the trace file to start reading from.
        """
        self.from_node = from_node
        self.to_node = to_node
        self.trace_file = trace_file
        self.start_index = start_index
        self.current_index = start_index
        
        self._packets = []
        with open(trace_file) as f:
            for i, line in enumerate(f):
                if i >= start_index:
                    packet = parse_trace_line(line)
                    self._packets.append(packet)
    
    @property        
    def current_packet(self):
        """
        The current packet being read.
        """
        return self._packets[self.current_index]

    @property
    def packets_left(self):
        """
        The number of packets left (including the `current_frame`).
        """
        return len(self._packets) - self.current_index

    @property
    def has_packets_left(self):
        """
        Returns True if there are more packets left, False otherwise.
        """
        return self.packets_left > 0

    def next(self):
        """
        Increases the `current_index` by 1 and return the next frame in the list.
        """
        if self.has_packets_left:
            self.current_index += 1
            return self.current_packet
        return None
