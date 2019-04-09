from utils import distance as _distance
from collections import defaultdict, deque

class Node():
    def __init__(self, update_callback=None, _id=None, position=(.0,.0,.0), initial_charge=100.0, up_current=1.0, down_current=0.5):
        self.id=_id
        self.x=position[0]
        self.y=position[1]
        self.z=position[2]
        self.initial_charge=initial_charge
        self.remaining_charge = initial_charge
        self.remaining_energy = 1.0
        self.up_current = up_current
        self.down_current = down_current
        self.current_up = False # 0/false=down, 1/true=up
        self._update_cb=update_callback


    def update_state(self, frame, link):
        drain_current = self.down_current
        if self.current_up:
            drain_current = self.up_current
        datarate = link.datarate
        current_charge = self.initial_charge * self.remaining_energy
        frame_size = frame['frame_size']
        t = (frame_size * 8) / (datarate * 1000000) # seconds
        deplete_charge = current_charge - (t * drain_current)
        self.remaining_charge = current_charge - deplete_charge

        perc=0.0
        if self.initial_charge > 0.0:
            perc = (current_charge - deplete_charge) / self.initial_charge
        self.remaining_energy -= perc

        if self.initial_charge <= 0.0:
            self.initial_charge = 0.0
        if self._update_cb:
            self._update_cb(self)

class Link():
    def __init__(self, metric, _from=Node(), _to=Node(), error_probability=0.1, datarate=1.0):
        self._from=_from
        self._to=_to
        self.error_probability=error_probability
        self.datarate=datarate
        self.metric = float('inf')
        self._metric = metric
        self.update_state(None)
                
    # might be useful for mobile networks
    def update_distance(self):
        self.distance = _distance((self._from.x, self._from.y, self._from.z), (self._to.x, self._to.y, self._to.z))

    def update_metric(self):
        self.metric = self._metric(self)

    def update_state(self, frame):
        self.update_distance()
        self.update_metric()
        if frame != None:
            self._from.update_state(frame, self)
            self._to.update_state(frame, self)


class Network():
    def __init__(self):
        self.nodes=set()
        self.links=[]

    """
    Helper methods, used internally
    """
    def _get_nodes(self):
        return set([n.id for n in self.nodes])
    
    def _get_edges(self):
        edges = defaultdict(list)
        for link in self.links:
            edges[link._from.id].append(link._to.id)
            edges[link._to.id].append(link._from.id)
        return edges
    
    def _get_distances(self):
        distances = defaultdict(lambda: float('inf'))#{}
        for link in self.links:
            distances[(link._from.id, link._to.id)] = link.metric
        print(distances)
        return distances

    """
    Helper methods to create training samples
    """
    def get_out_nth_neighborhood_set(self, _from, hops=1):
        visited = set()
        queue = deque([_from, None])

        level = 0
        nbh=set([])
        
        while queue:
            vertex = queue.popleft()
            if vertex == None:
                queue.append(None)
                level += 1
                if queue[0] == None:
                    return nbh
                else:
                    continue
            
            for link in self.get_all_out_links_from_node_id(vertex):
                nb = link._to.id
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
                    if level+1 == hops: nbh.add(nb)
                    elif level+1 > hops: return nbh

    def get_in_nth_neighborhood_set(self, _from, hops=1):
        visited = set()
        queue = deque([_from, None])

        level = 0
        nbh=set([])
        
        while queue:
            vertex = queue.popleft()
            if vertex == None:
                queue.append(None)
                level += 1
                if queue[0] == None:
                    return nbh
                else:
                    continue
            for link in self.get_all_in_links_from_node_id(vertex):
                nb = link._from.id
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
                    if level+1 == hops: nbh.add(nb)
                    elif level+1 > hops: return nbh

    """
    Path finding methods
    """
    def dijkstra(self, _from):
        visited = {_from: 0}
        path = {}
        nodes = self._get_nodes()
        edges = self._get_edges()
        distances = self._get_distances()
        while nodes: 
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break
            nodes.remove(min_node)
            current_weight = visited[min_node]
            for edge in edges[min_node]:
                weight = current_weight + distances[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node
        return visited, path
    
    def shortest_path(self, source=Node(), destination=Node()):
        visited, paths = self.dijkstra(source.id)
        full_path = deque()
        _destination = paths[destination.id]
        while _destination != source.id:
            full_path.appendleft(_destination)
            _destination = paths[_destination]
        full_path.appendleft(source.id)
        full_path.append(destination.id)
        return visited[destination.id], list(full_path)

    """
    Manipulate network topology
    """
    def add_node(self, node=None):
        self.nodes.add(node)
    def remove_node_by_id(self, _id):
        self.nodes.discard(self.get_node_by_id(_id))

    def get_node_by_id(self, _id):
        for node in self.nodes:
            if node.id == _id:
                return node
        return None

    def add_link(self, link=None):
        self.links.append(link)
    def remove_link_by_ids(self, _from_id, _to_id):
        link = self.get_link_by_ids(_from_id, _to_id)
        if link in self.links:
            self.links.remove(link)
    


    def get_link_by_ids(self, _from_id, _to_id):
        for link in self.links:
            if link._from.id == _from_id and link._to.id == _to_id:
                return link
        return None

    """
    Node/Link State related methods
    """
    def get_all_out_links_from_node_id(self, _id):
        links = []
        for link in self.links:
            if link._from.id == _id:
                links.append(link)
        return links
    def get_all_in_links_from_node_id(self, _id):
        links = []
        for link in self.links:
            if link._to.id == _id:
                links.append(link)
        return links
    def get_node_out_degree(self, _id):
        return len(self.get_all_out_links_from_node_id(_id))
    def get_node_in_degree(self, _id):
        return len(self.get_all_in_links_from_node_id(_id))
    def get_node_degree(self, _id):
        return len(self.get_node_out_degree(_id)) + len(self.get_node_in_degree(_id))

    def update_state(self, frame):
        for link in self.links:
            link.update_state(frame)

    """
    Retrieve entire network state
    """
    def get_state(self):
        n_state = []
        for node in self.nodes:
            n_state.append({
                'id': node.id,
                'in_degree': self.get_node_in_degree(node.id),
                'out_degree': self.get_node_out_degree(node.id),
                'remaining_energy_fraction': node.remaining_energy,
                'current_state_up': node.current_up,
                'up_current': node.up_current,
                'down_current': node.down_current,
                'pos': (node.x, node.y, node.z),
                'frame_of_death': node.frame_of_death,
            })
        l_state = []
        for link in self.links:
            l_state.append({
                'from_id': link._from.id,
                'to_id': link._to.id,
                'distance': link.distance,
                'datarate': link.datarate,
                'error_probability': link.error_probability,
                'metric': link.metric
            })
        return n_state, l_state