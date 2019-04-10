import unittest

from lib.Node import Node
from lib.Link import Link
from lib.Network import Network

from lib.utils import parse_trace_line, distance,\
        agg_energy_fraction, agg_initial_charge, agg_current_charge, agg_degree,\
        sort_by_energy_fraction, sort_by_initial_charge, sort_by_current_charge,\
        ordinal_label, neighborhood,\
        dijkstra, shortest_path

class TestClasses(unittest.TestCase):
    """
    Tests classes Node, Link, and Network related functions.
    """
    def setUp(self):
        """
        Initialize test objects.
        """
        self.node0 = Node(node_id=0, position=(.0,.0,.0), initial_charge=100.0, up_current=1.0, down_current=0.5, update_callback=None)
        self.node1 = Node(node_id=1, position=(.0,.0,100.0), initial_charge=100.0, up_current=1.0, down_current=0.5, update_callback=None)
        self.link0 = Link(lambda x:1.0, self.node0, self.node1, error_probability=0.1, datarate=1.0)
        self.link1 = Link(lambda x:0.5, self.node1, self.node0, error_probability=0.1, datarate=2.0)
        self.n0 = Network()
        self.n0.add_node(self.node0)
        self.n0.add_node(self.node1)
        self.n0.add_link(self.link0)
        self.n0.add_link(self.link1)

    def test_distance(self):
        """
        Tests `distance` function.
        """
        d0 = distance(self.node0.position, self.node1.position)
        d1 = distance(self.node0.position, self.node1.position)
        self.assertEqual(d0, 100.0)
        self.assertEqual(d1, 100.0)
        self.assertEqual(d0, d1)

    def test_update(self):
        """
        Test update procedure of a Link object.
        """
        packet={
            'index': 0,
            'size': 1000,
            'type': 'I',
            'time': 0
        }
        self.node1.is_current_up = True
        self.link0.update(packet)
        self.assertEqual(self.node0.current_charge, 99.996)
        self.assertEqual(self.node1.current_charge, 99.992)

        self.node0.is_current_up = True
        self.node1.is_current_up = False
        self.link1.update(packet)
        self.assertAlmostEqual(self.node0.current_charge, 99.99199999999999)
        self.assertAlmostEqual(self.node1.current_charge, 99.99000000000001)

        self.node0.is_current_up = False
        self.node1.is_current_up = True
        self.n0.update(packet)
        self.assertAlmostEqual(self.node0.current_charge, 99.98599999999999)
        self.assertAlmostEqual(self.node1.current_charge, 99.97800000000001)

        self.assertEqual(self.link0.distance, 100.0)
        self.assertEqual(self.link1.distance, 100.0)


class TestUtils(unittest.TestCase):
    """
    Test utility functions.
    """
    def setUp(self):
        """
        Create sample networks.
        """
        self.n0 = Network()
        self.node0=Node(node_id=0, initial_charge=1.0)
        self.node1=Node(node_id=1, initial_charge=2.0)
        self.node2=Node(node_id=2, initial_charge=3.0)

        self.node3=Node(node_id=3, initial_charge=3.1)

        self.link0 = Link(lambda x:1.0, self.node0, self.node1, error_probability=0.1, datarate=1.0)

        self.n0.add_node(self.node0)
        self.n0.add_node(self.node1)
        self.n0.add_node(self.node2)
        self.n0.add_node(self.node3)

        self.n0.add_link(self.link0)

        self.packet={
            'index': 13,
            'size': 1000,
            'type': 'B',
            'time': 440
        }

    def test_parse(self):
        """
        Test line parser function.
        """
        line = "13		B		440		1000"
        self.assertEqual(self.packet, parse_trace_line(line))
    
    def test_agg_functions(self):
        """
        Test aggregation functions: agg_energy_fraction, agg_initial_charge, agg_current_charge, agg_degree.
        """
        self.node0.is_current_up = True
        self.node0.update(self.packet, self.link0)

        ef = agg_energy_fraction(self.n0, [0,1,2])
        self.assertLess(ef, 3.0)
        ic = agg_initial_charge(self.n0, [0,1,2])
        self.assertEqual(ic, 6.0)
        ic = agg_initial_charge(self.n0, [0,1,2,3])
        self.assertEqual(ic, 9.1)
        cc = agg_current_charge(self.n0, [0,1,2])
        self.assertLess(cc, 6.0)
        cc = agg_current_charge(self.n0, [0,1,2,3])
        self.assertGreater(cc, 6.1)

        d = agg_degree(self.n0, [0,1,2,3])
        self.assertEqual(d, 1)
        d = agg_degree(self.n0, [0,1,2,3], out=False)
        self.assertEqual(d, 1)

    def test_sort_functions(self):
        """
        Test sort functions: sort_by_energy_fraction, sort_by_initial_charge, sort_by_current_charge.
        """
        self.assertEqual([self.node0, self.node1, self.node2, self.node3], sort_by_initial_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node0, self.node3, self.node2, self.node1], sort_by_initial_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node1, self.node0, self.node3, self.node2], sort_by_initial_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node1, self.node2, self.node0], sort_by_initial_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node3, self.node2, self.node0, self.node1], sort_by_initial_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node2, self.node1, self.node0, self.node3], sort_by_initial_charge(self.n0, set([0,1,2,3])))

        self.assertEqual([self.node3, self.node2, self.node1, self.node0], sort_by_current_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node0, self.node2, self.node1, self.node3], sort_by_current_charge(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node1, self.node0, self.node2, self.node3], sort_by_current_charge(self.n0, set([0,3,1,2])))
        self.assertNotEqual([self.node1, self.node3, self.node2, self.node0], sort_by_current_charge(self.n0, set([0,1,3,2])))
        self.assertNotEqual([self.node2, self.node0, self.node3, self.node1], sort_by_current_charge(self.n0, set([0,1,3,2])))
        self.assertNotEqual([self.node3, self.node1, self.node2, self.node0], sort_by_current_charge(self.n0, set([3,0,1,2])))

        self.node0.is_current_up = True
        self.node0.update(self.packet, self.link0)
        self.node1.is_current_up = True
        self.node1.update(self.packet, self.link0)
        self.node2.is_current_up = True
        self.node2.update(self.packet, self.link0)
        self.node3.is_current_up = True
        self.node3.update(self.packet, self.link0)
        self.assertEqual([self.node0, self.node1, self.node2, self.node3], sort_by_energy_fraction(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node0, self.node2, self.node1, self.node3], sort_by_energy_fraction(self.n0, set([0,1,2,3])))
        self.assertNotEqual([self.node1, self.node0, self.node2, self.node3], sort_by_energy_fraction(self.n0, set([0,3,1,2])))
        self.assertNotEqual([self.node1, self.node3, self.node2, self.node0], sort_by_energy_fraction(self.n0, set([0,1,3,2])))
        self.assertNotEqual([self.node2, self.node0, self.node3, self.node1], sort_by_energy_fraction(self.n0, set([0,1,3,2])))
        self.assertNotEqual([self.node3, self.node2, self.node1, self.node0], sort_by_energy_fraction(self.n0, set([3,0,1,2])))

    def test_label(self):
        """
        Test ordinal label function.
        """
        label = ordinal_label(sort_by_energy_fraction(self.n0, set([0,1,2,3])), self.node3)
        self.assertEqual(label, .75)
        label = ordinal_label(sort_by_energy_fraction(self.n0, set([0,1,2,3])), self.node2)
        self.assertEqual(label, .5)
        label = ordinal_label(sort_by_energy_fraction(self.n0, set([0,1,2,3])), self.node1)
        self.assertEqual(label, .25)
        label = ordinal_label(sort_by_energy_fraction(self.n0, set([0,1,2,3])), self.node0)
        self.assertEqual(label, .0)

        label = ordinal_label(sort_by_initial_charge(self.n0, set([0,1,2,3])), self.node3)
        self.assertEqual(label, .75)
        label = ordinal_label(sort_by_initial_charge(self.n0, set([0,1,2,3])), self.node2)
        self.assertEqual(label, .5)
        label = ordinal_label(sort_by_initial_charge(self.n0, set([0,1,2,3])), self.node1)
        self.assertEqual(label, .25)
        label = ordinal_label(sort_by_initial_charge(self.n0, set([0,1,2,3])), self.node0)
        self.assertEqual(label, .0)

        label = ordinal_label(sort_by_current_charge(self.n0, set([0,1,2,3])), self.node3)
        self.assertEqual(label, .0)
        label = ordinal_label(sort_by_current_charge(self.n0, set([0,1,2,3])), self.node2)
        self.assertEqual(label, .25)
        label = ordinal_label(sort_by_current_charge(self.n0, set([0,1,2,3])), self.node1)
        self.assertEqual(label, .5)
        label = ordinal_label(sort_by_current_charge(self.n0, set([0,1,2,3])), self.node0)
        self.assertEqual(label, .75)

    def test_neighborhood(self):
        """
        Test neighborhood function.
        """
        from random import random

        n = Network()
        for i in range(7):
            for j in range(7):
                n.add_node(Node(node_id=int(str(i) + str(j)), position=(i*100.0, j*100.0, 0.0), initial_charge=100.0, up_current=1.5, down_current=0.5))
        for i in range(7):
            for j in range(7):
                node = n.get_node(int(str(i) + str(j)))
                if i-1 >= 0:
                    n.add_link(Link(lambda x: random(), from_node=node, to_node=n.get_node(int(str(i-1) + str(j)))))
                if j-1 >= 0:
                    n.add_link(Link(lambda x: random(), from_node=node, to_node=n.get_node(int(str(i) + str(j-1)))))
                if i+1 < 7:
                    n.add_link(Link(lambda x: random(), from_node=node, to_node=n.get_node(int(str(i+1) + str(j)))))
                if j+1 < 7:
                    n.add_link(Link(lambda x: random(), from_node=node, to_node=n.get_node(int(str(i) + str(j+1)))))
        
        nbh_1_out = neighborhood(n, 0, hops=1)
        nbh_2_out = neighborhood(n, 0, hops=2)
        nbh_3_out = neighborhood(n, 0, hops=3)
        self.assertEqual(nbh_1_out, set([1, 10]))
        self.assertEqual(nbh_2_out, set([2, 20, 11]))
        self.assertEqual(nbh_3_out, set([30, 21, 12, 3]))

        nbh_1_out = neighborhood(n, 0, hops=1, out=False)
        nbh_2_out = neighborhood(n, 0, hops=2, out=False)
        nbh_3_out = neighborhood(n, 0, hops=3, out=False)
        self.assertEqual(nbh_1_out, set([1, 10]))
        self.assertEqual(nbh_2_out, set([2, 20, 11]))
        self.assertEqual(nbh_3_out, set([30, 21, 12, 3]))


class TestDijkstra(unittest.TestCase):
    """
    Test various Dijkstra situations
    """
    def test_directed(self):
        """
        Test Dijkstra for directed cyclic graph
        """
        n = Network()
        for i in range(3): n.add_node(Node(node_id=i))
        n.add_link(Link(lambda x: 10, from_node=n.get_node(0), to_node=n.get_node(1)))
        n.add_link(Link(lambda x: 1, from_node=n.get_node(1), to_node=n.get_node(2)))
        n.add_link(Link(lambda x: 3, from_node=n.get_node(2), to_node=n.get_node(0)))

        cost, path = shortest_path(n.graph, 0, 1)
        self.assertEqual(cost, 10)
        self.assertEqual(path, [0,1])
        cost, path = shortest_path(n.graph, 0, 2)
        self.assertEqual(cost, 11)
        self.assertEqual(path, [0,1,2])

        cost, path = shortest_path(n.graph, 1, 0)
        self.assertEqual(cost, 4)
        self.assertEqual(path, [1,2,0])
        cost, path = shortest_path(n.graph, 1, 2)
        self.assertEqual(cost, 1)
        self.assertEqual(path, [1,2])

        cost, path = shortest_path(n.graph, 2, 0)
        self.assertEqual(cost, 3)
        self.assertEqual(path, [2,0])
        cost, path = shortest_path(n.graph, 2, 1)
        self.assertEqual(cost, 13)
        self.assertEqual(path, [2,0,1])

    def test_acyclic_disconected(self):
        """
        Test Dijkstra for directed acyclic graph
        """
        n = Network()
        for i in range(6): n.add_node(Node(node_id=i))
        n.add_link(Link(lambda x: 10, from_node=n.get_node(0), to_node=n.get_node(1)))
        n.add_link(Link(lambda x: 3, from_node=n.get_node(0), to_node=n.get_node(2)))
        n.add_link(Link(lambda x: 1, from_node=n.get_node(1), to_node=n.get_node(2)))
        n.add_link(Link(lambda x: 1, from_node=n.get_node(3), to_node=n.get_node(2)))
        n.add_link(Link(lambda x: 1.5, from_node=n.get_node(4), to_node=n.get_node(5)))

        cost, path = shortest_path(n.graph, 0, 1)
        self.assertEqual(cost, 10)
        self.assertEqual(path, [0,1])
        cost, path = shortest_path(n.graph, 0, 2)
        self.assertEqual(cost, 3)
        self.assertEqual(path, [0,2])
        cost, path = shortest_path(n.graph, 0, 3)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 0, 4)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 0, 5)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])

        cost, path = shortest_path(n.graph, 1, 2)
        self.assertEqual(cost, 1)
        self.assertEqual(path, [1,2])
        cost, path = shortest_path(n.graph, 1, 0)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 1, 3)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 1, 4)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 1, 5)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])

        cost, path = shortest_path(n.graph, 2, 0)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 2, 1)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 2, 3)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 2, 4)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 2, 5)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])

        cost, path = shortest_path(n.graph, 3, 0)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 3, 1)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 3, 2)
        self.assertEqual(cost, 1)
        self.assertEqual(path, [3,2])
        cost, path = shortest_path(n.graph, 3, 4)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 3, 5)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])

        cost, path = shortest_path(n.graph, 4, 0)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 4, 1)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 4, 2)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 4, 3)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 4, 5)
        self.assertEqual(cost, 1.5)
        self.assertEqual(path, [4,5])

        cost, path = shortest_path(n.graph, 5, 0)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 5, 1)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 5, 2)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 5, 3)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])
        cost, path = shortest_path(n.graph, 5, 4)
        self.assertEqual(cost, float('inf'))
        self.assertEqual(path, [])

if __name__ == '__main__':
    unittest.main()