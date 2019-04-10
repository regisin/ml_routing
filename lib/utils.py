def parse_trace_line(line):
    """
    Maps a line from a trace file into a dictionary for ease of use.
    
    Input
    line: str.
    """
    frame_index, frame_type, frame_time, frame_size = [x for x in line.rstrip("\n\r").split('\t') if x]
    return {
        'index': int(frame_index),
        'size': int(frame_size),
        'type': frame_type,
        'time': int(frame_time),
    }

def distance(a,b):
    """
    Calculates the Euclidean distance between points 'a' and 'b'.
    
    Input
    a: tuple of floats (x,y,z).
    b: tuple of floats (x,y,z).
    """
    return ( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )**0.5

def agg_energy_fraction(network, nodes):
    """
    Adds the energy_fraction attribute of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    re = 0
    for _id in nodes:
        node = network.get_node(_id)
        re += node.energy_fraction
    return re

def agg_initial_charge(network, nodes):
    """
    Adds the initial_charge attribute of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    ic = 0
    for _id in nodes:
        node = network.get_node(_id)
        ic += node.initial_charge
    return ic

def agg_current_charge(network, nodes):
    """
    Adds the remaining_charge attribute of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    rc = 0
    for _id in nodes:
        node = network.get_node(_id)
        rc += node.initial_charge * node.energy_fraction
    return rc

def agg_degree(network, nodes, out=True):
    """
    Adds the out_degree (number of outgoing edges) of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    d = 0
    for _id in nodes:
        d += degree(network, _id, out=out)
    return d

def sort_by_energy_fraction(network, nodes):
    """
    Returns a sorted list based on the energy_fraction attribute of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    nodes = []
    for _id in nodes:
        nodes.append(network.get_node_by_id(_id))
    return sorted(nodes, key=lambda x: x.energy_fraction)

def sort_by_initial_charge(network, nodes):
    """
    Returns a sorted list based on the initial_charge attribute of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    sorted_nodes = []
    for _id in nodes:
        sorted_nodes.append(network.get_node(_id))
    return sorted(sorted_nodes, key=lambda x: x.initial_charge)

def sort_by_remaining_charge(network, nodes):
    """
    Returns a sorted list based on the remaining_charge attribute of each node in the set.

    Input
    network: Network object.
    nodes: set() of ints representing the node's id.
    """
    nodes = []
    for _id in nodes:
        nodes.append(network.get_node_by_id(_id))
    return sorted(nodes, key=lambda x: x.remaining_charge)

def ordinal_label(sorted_list, item):
    """
    Computes the ordinal feature based on sorted list and index.

    Input
    sorted_list: list (agnostic of type of sorting performed)
    item: an item in the sorted_list (i.e. from which we extract the ordinal feature)
    """
    total = len(sorted_list)
    index = sorted_list.index(item)
    label = float(index)/float(total)
    return label

def dijkstra(graph, source, destination=None):
    """
    Runs Dijkstra's algorithm on a given graph.

    Input
    graph: dict of dicts (directed graph)
    source: int (the source node id)
    destination: int (the destination node id)

    Ex.:

    graph = {
        0: {1:10, 2:1},
        1: {},
        2: {1:1}
    }
    """
    dist = {}  #lengths of the shortest paths to each node
    pred = {}  #predecessor node in each shortest path

    # Store distance scores in a priority queue dictionary
    pq = minpq()
    for node in graph:
        if node == source:
            pq[node] = 0
        else:
            pq[node] = float('inf')
    
    # popitems always pops out the node with min score
    # Removing a node from pqdict is O(log n).
    for node, min_dist in pq.popitems():
        dist[node] = min_dist
        if node == destination:
            break

        for neighbor in graph[node]:
            if neighbor in pq:
                new_score = dist[node] + graph[node][neighbor]
                if new_score < pq[neighbor]:
                    # Updating the score of a node is O(log n) using pqdict.
                    pq[neighbor] = new_score
                    pred[neighbor] = node

    return dist, pred

def shortest_path(graph, source, destination):
    """
    Finds shortest path from source to destination.
    """
    dist, pred = dijkstra(graph, source, destination)
    end = destination
    path = [end]
    while end != source:
        end = pred[end]
        path.append(end)        
    path.reverse()
    return path

def neighborhood(network, from_id, hops=1, out=True):
    """
    Retrieves the nth neighborhood set (ids of nodes that are n hops away from from_id).

    Input
    network: Network object.
    from_id: int (id of the source node).
    hops: int (distance from the source in hops).
    out: if False will use incoming links to the source instead of outgoing from the source. Default True.
    """
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
        links = links_from_node_id(network, vertex, out=out)
        for link in links:
            nb = link._to.id
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                if level+1 == hops: nbh.add(nb)
                elif level+1 > hops: return nbh

def links_from_node_id(network, node_id, out=True):
    """
    Retrieves a list of Link objects from/to a Node with id equal to node_id.

    Input
    network: Network object.
    node_id: int representing the id of the source node.
    out: if False will use incoming links to the source instead of outgoing from the source. Default True.
    """
    links = []
    for link in network.links:
        _id = None
        if out:
            _id = link.from_node.id
        else:
            _id = link.to_node.id
        if _id == node_id:
            links.append(link)
    return links

def degree(network, node_id, out=True):
    """
    Returns the node degree. Being a directed graph, use argument `out` to use incoming or outgoing links.
    """
    return len(links_from_node_id(network, node_id, out=out))