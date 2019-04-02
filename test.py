import unittest

from classes import Link, Node, Network


def metric(link):
    n0 = link._from.id
    n1 = link._to.id
    if n0 == 0 and n1 == 1: return 2
    if n0 == 0 and n1 == 2: return 3
    if n0 == 1 and n1 == 3: return 2
    if n0 == 1 and n1 == 0: return 3
    if n0 == 2 and n1 == 3: return 3
    if n0 == 2 and n1 == 0: return 2
    if n0 == 3 and n1 == 1: return 3
    if n0 == 3 and n1 == 2: return 2
    return 99

class TestNetworkMethods(unittest.TestCase):
    def test_directed_dijkstra(self):
        n = Network()
        n.add_node(node=Node(_id=0, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=1, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=2, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=3, position=(0.0, 0.0, 0.0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(2)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(2), _to=n.get_node_by_id(0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(3)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(3), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(2), _to=n.get_node_by_id(3)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(3), _to=n.get_node_by_id(2)))

        path = n.shortest_path(source=n.get_node_by_id(0), destination=n.get_node_by_id(3))
        path_reverse = n.shortest_path(source=n.get_node_by_id(3), destination=n.get_node_by_id(0))

        self.assertEqual(path[0], path_reverse[0])
        self.assertNotEqual(path[1], path_reverse[1])
        self.assertNotEqual(path[1], path_reverse[1].reverse())

if __name__ == '__main__':
    unittest.main()