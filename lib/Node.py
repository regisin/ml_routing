class Node():
    def __init__(self, node_id=None, position=(.0,.0,.0), initial_charge=100.0, up_current=1.0, down_current=0.5, update_callback=None):
        """
        Creates a Node instance.

        Input
        node_id: int.
        position: tuple of floats (x,y,z).
        initial_charge: float (in units of charge - Coulombs)
        up: float (draining current in Amps when node UP state is True).
        down: float (draining current in Amps when node UP state is False).
        update_callback: pointer to a function called after update_state.
        """
        self.id=node_id

        self.x=position[0]
        self.y=position[1]
        self.z=position[2]

        self.initial_charge = initial_charge
        self.current_charge = initial_charge
        self.up = up_current
        self.down = down_current
        # defines which value of current will be drained
        self.is_current_up = False
        self._update_cb=update_callback

    @property
    def position(self):
        """
        Easy formatting for node's position
        """
        return (self.x, self.y, self.z)

    @property
    def energy_fraction(self):
        return self.current_charge/self.initial_charge

    def update(self, packet, link):
        """
        Updates the state of charge (remaining energy fraction and remaining charge) based on size of packet.
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
        if self._update_cb: self._update_cb(self)