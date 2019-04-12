class Node():
    """ 
    This class represents a node of a network and keeps its node state information.
      
    Attributes:
            id (int): The id of the node. Should be unique among nodes within the same network.
            position ((float, float, float)): The cartesian position of the node. Same as `(self.x, self.y, self.z)`.
            x, y, z (float): Position of the node relative to each axis. Same as self.position[0], [1], and [2] respectively.
            initial_charge (float): The initial state of charge of the battery, in Coulombs.
            current_charge (float): The current state of charge of the battery, in Coulombs. At first is the same as `initial_charge`.
            energy_fraction (float): The current remaining energy fraction of the battery [0, 1], calculated as `current_charge/initial_charge`.
            up (float): The draining current in Amps when `is_current_up` is True.
            down (float): The draining current in Amps when `is_current_up` is False.
            is_node_up (bool): The state of the node, i.e. active (True) or inactive (False).
            update_callback (pointer): Callback function called after `update` finished. Ex.: `self.update_callback(self)`.
    """
    def __init__(self, node_id=None, position=(.0,.0,.0), initial_charge=100.0, up=1.0, down=0.5, is_current_up=False, update_callback=None):
        """
        Creates a Node instance.

        Parameters:
            node_id (int): The id of the node. Should be unique among nodes within the same network.
            position ((float, float, float)): The cartesian position of the node. Same as `(self.x, self.y, self.z)`.
            initial_charge (float): The initial state of charge of the battery, in Coulombs.
            up (float): The draining current in Amps when `is_current_up` is True.
            down (float): The draining current in Amps when `is_current_up` is False.
            flow_counter (int): The number of flows going through this node.
            is_node_up (bool): The state of the node, i.e. active (True) or inactive (False).
            update_callback (pointer): Callback function called after `update` finished. Ex.: `self.update_callback(self)`.
        """
        self.id=node_id

        self.x=position[0]
        self.y=position[1]
        self.z=position[2]

        self.initial_charge = initial_charge
        self.current_charge = initial_charge
        self.up = up
        self.down = down

        self.flow_counter = 0

        # dictates which value of current will be drained
        self.is_current_up = is_current_up
        
        self.update_callback=update_callback

    @property
    def position(self):
        """
        Easy formatting for node's position
        """
        return (self.x, self.y, self.z)

    @property
    def energy_fraction(self):
        """
        The remaining energy fraction of the node.
        """
        return self.current_charge / self.initial_charge

    def update(self, packet, link):
        """
        Updates the state of charge (remaining energy fraction and remaining charge) based on size of packet.

        Parameters:
            packet (dict): From a call to `parse_trace_line(line)`.
            link (Link): The link which the packet is supposed to traverse.
                         Usually the link itself calls this method passim its own pointer.
                         Ex.: `self.to_node.update(packet, self)`.
        """

        current = self.down
        if self.is_current_up: current = self.up

        # current state of charge
        current_charge = self.current_charge

        # calculate delta time based on packet size and datarate
        datarate = link.datarate
        packet_size = packet['size']
        t = (packet_size * 8) / (datarate * 1000000) # seconds

        # amount of coulombs consumed
        amount_to_decrease = (t * current)

        # update state of charge
        self.current_charge = current_charge - amount_to_decrease

        # prevent charge to go negative.
        if self.current_charge <= 0.0: self.current_charge = 0.0

        # update position
        # notify callback function
        if self.update_callback: self.update_callback(self)