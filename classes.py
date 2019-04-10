from utils import distance as _distance
from collections import defaultdict, deque
from pqdict import minpq

# class Node():
#     def __init__(self, update_callback=None, _id=None, position=(.0,.0,.0), initial_charge=100.0, up_current=1.0, down_current=0.5):
#         self.id=_id
#         self.x=position[0]
#         self.y=position[1]
#         self.z=position[2]
#         self.initial_charge=initial_charge
#         self.remaining_charge = initial_charge
#         self.remaining_energy = 1.0
#         self.up_current = up_current
#         self.down_current = down_current
#         self.current_up = False # 0/false=down, 1/true=up
#         self._update_cb=update_callback


#     def update_state(self, frame, link):
#         drain_current = self.down_current
#         if self.current_up:
#             drain_current = self.up_current
#         datarate = link.datarate
#         current_charge = self.initial_charge * self.remaining_energy
#         frame_size = frame['frame_size']
#         t = (frame_size * 8) / (datarate * 1000000) # seconds
#         deplete_charge = current_charge - (t * drain_current)
#         self.remaining_charge = current_charge - deplete_charge

#         perc=0.0
#         if self.initial_charge > 0.0:
#             perc = (current_charge - deplete_charge) / self.initial_charge
#         self.remaining_energy -= perc

#         if self.initial_charge <= 0.0:
#             self.initial_charge = 0.0
#         if self._update_cb:
#             self._update_cb(self)

# class Link():
#     def __init__(self, metric, _from=Node(), _to=Node(), error_probability=0.1, datarate=1.0):
#         self._from=_from
#         self._to=_to
#         self.error_probability=error_probability
#         self.datarate=datarate
#         self.metric = float('inf')
#         self._metric = metric
#         self.update_state(None)
                
#     # might be useful for mobile networks
#     def update_distance(self):
#         self.distance = _distance((self._from.x, self._from.y, self._from.z), (self._to.x, self._to.y, self._to.z))

#     def update_metric(self):
#         self.metric = self._metric(self)

#     def update_state(self, frame):
#         self.update_distance()
#         self.update_metric()
#         if frame != None:
#             self._from.update_state(frame, self)
#             self._to.update_state(frame, self)


# class Network():
#     def __init__(self):
#         self.nodes=set()
#         self.links=[]
#         self.as_graph={}

#     """
#     Helper methods, used internally
#     """
#     def _get_nodes(self):
#         return set([n.id for n in self.nodes])
    
#     def _get_edges(self):
#         edges = defaultdict(list)
#         for link in self.links:
#             edges[link._from.id].append(link._to.id)
#             edges[link._to.id].append(link._from.id)
#         return edges
    
#     def _get_distances(self):
#         distances = defaultdict(lambda: float('inf'))
#         for link in self.links:
#             distances[(link._from.id, link._to.id)] = link.metric
#         return distances

#     def _set_graph(self):
#         graph = {}
#         for node in self.nodes:
#             graph[node.id]={}
#             for link in self.get_all_out_links_from_node_id(node.id):
#                 graph[node.id][link._to.id]=link.metric
#         self.as_graph = graph


#     def dijkstra(self, source, destination=None):
#         """
#         Dijkstra
#         """
#         graph = self.as_graph

#         dist = {}  #lengths of the shortest paths to each node
#         pred = {}  #predecessor node in each shortest path

#         # Store distance scores in a priority queue dictionary
#         pq = minpq()
#         for node in graph:
#             if node == source:
#                 pq[node] = 0
#             else:
#                 pq[node] = float('inf')
        
#         # popitems always pops out the node with min score
#         # Removing a node from pqdict is O(log n).
#         for node, min_dist in pq.popitems():
#             dist[node] = min_dist
#             if node == destination:
#                 break

#             for neighbor in graph[node]:
#                 if neighbor in pq:
#                     new_score = dist[node] + graph[node][neighbor]
#                     if new_score < pq[neighbor]:
#                         # Updating the score of a node is O(log n) using pqdict.
#                         pq[neighbor] = new_score
#                         pred[neighbor] = node

#         return dist, pred

#     def shortest_path(self, source, destination):
#         """Finds shortest path from source to destination"""
#         graph = self.as_graph
#         dist, pred = dijkstra(graph, source, destination)
#         end = destination
#         path = [end]
#         while end != source:
#             end = pred[end]
#             path.append(end)        
#         path.reverse()
#         return path
#     """
#     Helper methods to create training samples
#     """
#     def get_out_nth_neighborhood_set(self, _from, hops=1):
#         visited = set()
#         queue = deque([_from, None])

#         level = 0
#         nbh=set([])
        
#         while queue:
#             vertex = queue.popleft()
#             if vertex == None:
#                 queue.append(None)
#                 level += 1
#                 if queue[0] == None:
#                     return nbh
#                 else:
#                     continue
            
#             for link in self.get_all_out_links_from_node_id(vertex):
#                 nb = link._to.id
#                 if nb not in visited:
#                     visited.add(nb)
#                     queue.append(nb)
#                     if level+1 == hops: nbh.add(nb)
#                     elif level+1 > hops: return nbh

#     def get_in_nth_neighborhood_set(self, _from, hops=1):
#         visited = set()
#         queue = deque([_from, None])

#         level = 0
#         nbh=set([])
        
#         while queue:
#             vertex = queue.popleft()
#             if vertex == None:
#                 queue.append(None)
#                 level += 1
#                 if queue[0] == None:
#                     return nbh
#                 else:
#                     continue
#             for link in self.get_all_in_links_from_node_id(vertex):
#                 nb = link._from.id
#                 if nb not in visited:
#                     visited.add(nb)
#                     queue.append(nb)
#                     if level+1 == hops: nbh.add(nb)
#                     elif level+1 > hops: return nbh

#     """
#     Manipulate network topology
#     """
#     def add_node(self, node=None):
#         self.nodes.add(node)
#     def remove_node_by_id(self, _id):
#         self.nodes.discard(self.get_node_by_id(_id))

#     def get_node_by_id(self, _id):
#         for node in self.nodes:
#             if node.id == _id:
#                 return node
#         return None

#     def add_link(self, link=None):
#         self.links.append(link)
#     def remove_link_by_ids(self, _from_id, _to_id):
#         link = self.get_link_by_ids(_from_id, _to_id)
#         if link in self.links:
#             self.links.remove(link)
    


#     def get_link_by_ids(self, _from_id, _to_id):
#         for link in self.links:
#             if link._from.id == _from_id and link._to.id == _to_id:
#                 return link
#         return None

#     """
#     Node/Link State related methods
#     """
#     def get_all_out_links_from_node_id(self, _id):
#         links = []
#         for link in self.links:
#             if link._from.id == _id:
#                 links.append(link)
#         return links
#     def get_all_in_links_from_node_id(self, _id):
#         links = []
#         for link in self.links:
#             if link._to.id == _id:
#                 links.append(link)
#         return links
#     def get_node_out_degree(self, _id):
#         return len(self.get_all_out_links_from_node_id(_id))
#     def get_node_in_degree(self, _id):
#         return len(self.get_all_in_links_from_node_id(_id))
#     def get_node_degree(self, _id):
#         return len(self.get_node_out_degree(_id)) + len(self.get_node_in_degree(_id))

#     def update_state(self, frame):
#         for link in self.links:
#             link.update_state(frame)
#         self._set_graph()