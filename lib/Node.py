class Node():
    def __init__(self, node_id=None, position=(.0,.0,.0), initial_charge=100.0, up_current=1.0, down_current=0.5, update_callback=None):
        """
        Creates a Node instance.

        Input
        node_id: int.
        position: tuple of floats (x,y,z).
        initial_charge: float (in units of charge - Coulombs)
        up_current: float (draining current in Amps when node UP state is True).
        down_current: float (draining current in Amps when node UP state is False).
        update_callback: pointer to a function called after update_state.
        """
        self.id=node_id
        self.x=position[0]
        self.y=position[1]
        self.z=position[2]
        self.initial_charge=initial_charge
        self.remaining_charge = initial_charge
        self.remaining_energy = 1.0
        self.up_current = up_current
        self.down_current = down_current
        self.current_up = False
        self._update_cb=update_callback


    def update(self, packet, link):
        """
        Updates the state of charge (remaining energy fraction and remaining charge) based on size of packet.
        """
        drain_current = self.down_current
        if self.current_up:
            drain_current = self.up_current
        datarate = link.datarate
        current_charge = self.initial_charge * self.remaining_energy
        packet_size = packet['size']
        t = (packet_size * 8) / (datarate * 1000000) # seconds
        deplete_charge = (t * drain_current)
        self.remaining_charge = current_charge - deplete_charge

        perc=0.0
        if self.initial_charge > 0.0:
            perc = (current_charge - deplete_charge) / self.initial_charge
        self.remaining_energy -= perc

        if self.initial_charge <= 0.0:
            self.initial_charge = 0.0
        if self._update_cb:
            self._update_cb(self)