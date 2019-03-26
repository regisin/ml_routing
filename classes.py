class Node():
    def __init__(self, _id=None, position=(.0,.0,.0)):
        self.id=_id
        self.x=position[0]
        self.y=position[1]
        self.z=position[2]
        self.remaining_energy=1.0
    def get_state(self):
        return self.id, (self.x, self.y, self.z), self.remaining_energy
        # position, energy, app data rate,num ifaces, num neighbors...

class Link():
    def __init__(self, _from=Node(), _to=Node(), error_probability=0.1, datarate=1.0):
        self._from=_from
        self._to=_to
        self.error_probability=error_probability
        self.datarate=datarate
    """
    Change this function to change the routing metric/link weight
    Ex.: return self._to.remaining_energy
    Ex.: return distance(self._from, self._to)
    """
    def get_metric(self):
        return self.metric
    def set_metric(self, metric):
        self.metric = metric

    def get_state(self):
        return self._from, self._to, self.error_probability, self.datarate
        # error, distance, throughput, delay...



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
        distances = {}
        for link in self.links:
            distances[(link._from.id, link._to.id)] = link.get_metric()
        return distances
    
    def _dijkstra(self, _from):
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
                weight = current_weight + distance[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node
        return visited, path

    """
    Main methods
    """
    def add_node(self, node=None):
        self.nodes.add(node)

    def get_node_by_id(self, _id):
        for node in self.nodes:
            if node.id == _id:
                return node
        return None

    def add_link(self, link=None):
        self.links.append(link)

    def get_link_by_ids(self, _from_id, _to_id):
        for link in self.links:
            if link._from.id == _from_id and link._to.id == _to_id:
                return link
        return None

    def shortest_path(self, source=Node(), destination=Node()):
        visited, paths = self._dijkstra(source.id)
        full_path = deque()
        _destination = paths[destination.id]
        while _destination != origin:
            full_path.appendleft(_destination)
            _destination = paths[_destination]
        full_path.appendleft(origin)
        full_path.append(destination)
        return visited[destination], list(full_path)
    
    def get_state(self):
        n_state = [n.get_state() for n in self.nodes]
        l_state = [l.get_state() for l in self.links]
        return n_state, l_state




