# create network
# load trace
# compute dijkstra+update network state for each packet

from classes import Node, Link, Network

"""
Topology: 7x7 evenly spaced grid
Why? 7+7+5+5 = 24 edge nodes (x); 5x5=25 inner nodes (o)

z = 0 for all

(x,y)
(0,600) ----> (600,600)
x---x---x---x---x---x---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---x---x---x---x---x---x
(0,0) ----> (600,0)

84x2=168 links
"""
#
# Params
#
trace_file='trace.dat'
mtu=1500
z = 0.0
n = Network()
square_size = 7

#
# Create network/graph
#
for i in range(square_size):
    for j in range(square_size):
        n.add_node(node=Node(_id=int(str(i) + str(j)), position=(i*100.0, j*100.0, z)))

for i in range(square_size):
    for j in range(square_size):
        node = n.get_node_by_id(int(str(i) + str(j)))
        if i-1 >= 0:
            n.add_link(link=Link(_from=node, _to=n.get_node_by_id(int(str(i-1) + str(j)))))
        if j-1 >= 0:
            n.add_link(link=Link(_from=node, _to=n.get_node_by_id(int(str(i) + str(j-1)))))
        if i+1 < square_size:
            n.add_link(link=Link(_from=node, _to=n.get_node_by_id(int(str(i+1) + str(j)))))
        if j+1 < square_size:
            n.add_link(link=Link(_from=node, _to=n.get_node_by_id(int(str(i) + str(j+1)))))

from utils import parse_trace_line

with open(trace_file) as f:
    for line in f:
        frame = parse_trace_line(line)
        # "transmit the frame"
        # - calculate shortest path
        # - save network state (topology, node state, link state, frame)
        # - update state of network
        # - - update link metric
        # - - update node energy
        # next

        

















