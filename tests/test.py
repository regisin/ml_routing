import unittest

from lib.Node import Node
from lib.Link import Link
from lib.Network import Network

from lib.utils import parse_trace_line, distance,\
    agg_energy_fraction, agg_initial_charge, agg_current_charge, agg_degree,\
    sort_by_initial_charge

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
        Test update procedure of a Link object
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
    Test utility functions
    """
    def setUp(self):
        """
        Create sample networks
        """
        self.n0 = Network()
        self.node0=Node(node_id=0, initial_charge=1.0)
        self.node1=Node(node_id=1, initial_charge=2.0)
        self.node2=Node(node_id=2, initial_charge=3.0)

        self.node3=Node(node_id=3, initial_charge=3.0)

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
        Test line parser function
        """
        line = "13		B		440		1000"
        self.assertEqual(self.packet, parse_trace_line(line))
    
    def test_agg_functions(self):
        """
        Test aggregation functions: agg_energy_fraction, agg_initial_charge, agg_current_charge, agg_out_degree, agg_in_degree.
        """
        self.node0.is_current_up = True
        self.node0.update(self.packet, self.link0)

        ef = agg_energy_fraction(self.n0, [0,1,2])
        self.assertLess(ef, 3.0)
        ic = agg_initial_charge(self.n0, [0,1,2])
        self.assertEqual(ic, 6.0)
        ic = agg_initial_charge(self.n0, [0,1,2,3])
        self.assertEqual(ic, 9.0)
        cc = agg_current_charge(self.n0, [0,1,2])
        self.assertLess(cc, 6.0)
        cc = agg_current_charge(self.n0, [0,1,2,3])
        self.assertGreater(cc, 6.0)

        d = agg_degree(self.n0, [0,1,2,3])
        self.assertEqual(d, 1)
        d = agg_degree(self.n0, [0,1,2,3], out=False)
        self.assertEqual(d, 1)







    # def test_sort_functions(self):
    #     """
    #     Test sorting functions
    #     """
    #     self.assertEqual([self.node0, self.node1, self.node2], sort_by_initial_charge(self.n0, set([0,1,2])))
    #     self.assertNotEqual([self.node0, self.node2, self.node1], sort_by_initial_charge(self.n0, set([0,1,2])))
    #     self.assertNotEqual([self.node1, self.node0, self.node2], sort_by_initial_charge(self.n0, set([0,1,2])))
    #     self.assertNotEqual([self.node1, self.node2, self.node0], sort_by_initial_charge(self.n0, set([0,1,2])))
    #     self.assertNotEqual([self.node2, self.node0, self.node1], sort_by_initial_charge(self.n0, set([0,1,2])))
    #     self.assertNotEqual([self.node2, self.node1, self.node0], sort_by_initial_charge(self.n0, set([0,1,2])))

    # def test_directed_dijkstra(self):
    #     def metric(link):
    #         n0 = link._from.id
    #         n1 = link._to.id
    #         if n0 == 0 and n1 == 1: return 2
    #         if n0 == 0 and n1 == 10: return 3
    #         if n0 == 1 and n1 == 11: return 2
    #         if n0 == 1 and n1 == 0: return 3
    #         if n0 == 10 and n1 == 11: return 3
    #         if n0 == 10 and n1 == 0: return 2
    #         if n0 == 11 and n1 == 1: return 3
    #         if n0 == 11 and n1 == 10: return 2
    #         return 99
    #     n = Network()
    #     n.add_node(node=Node(_id=0))
    #     n.add_node(node=Node(_id=1))
    #     n.add_node(node=Node(_id=10))
    #     n.add_node(node=Node(_id=11))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(0)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(10)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(0)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(11)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(1)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(11)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(10)))

    #     path = n.shortest_path(source=n.get_node_by_id(0), destination=n.get_node_by_id(11))
    #     path_reverse = n.shortest_path(source=n.get_node_by_id(11), destination=n.get_node_by_id(0))

    #     self.assertEqual(path[0], path_reverse[0])
    #     self.assertNotEqual(path[1], path_reverse[1])
    #     self.assertNotEqual(path[1], path_reverse[1].reverse())
    
    # def test_disconected_graph(self):
    #     def metric(link):
    #         return 1
    #     n = Network()
    #     n.add_node(node=Node(_id=0))
    #     n.add_node(node=Node(_id=1))
    #     n.add_node(node=Node(_id=2))
    #     # n.add_node(node=Node(_id=3))
    #     # n.add_node(node=Node(_id=4))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(2)))
    #     # n.add_link(link=Link(metric, _from=n.get_node_by_id(3), _to=n.get_node_by_id(2)))

    #     path = n.shortest_path(source=n.get_node_by_id(0), destination=n.get_node_by_id(2))
    #     path_reverse = n.shortest_path(source=n.get_node_by_id(3), destination=n.get_node_by_id(2))
    #     print(path, path_reverse)

    #     # self.assertEqual(path[0], path_reverse[0])
    #     # self.assertNotEqual(path[1], path_reverse[1])
    #     # self.assertNotEqual(path[1], path_reverse[1].reverse())


    # def test_out_neighborhood_set(self):
    #     def metric(link):
    #         return 1
    #     n = Network()
    #     n.add_node(node=Node(_id=0))
    #     n.add_node(node=Node(_id=1))
    #     n.add_node(node=Node(_id=2))
    #     n.add_node(node=Node(_id=10))
    #     n.add_node(node=Node(_id=11))
    #     n.add_node(node=Node(_id=12))
    #     n.add_node(node=Node(_id=20))
    #     n.add_node(node=Node(_id=21))
    #     n.add_node(node=Node(_id=22))
        
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(2)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(11)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(12)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(20), _to=n.get_node_by_id(21)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(21), _to=n.get_node_by_id(22)))
        
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(10)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(20)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(11)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(21)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(2), _to=n.get_node_by_id(12)))
    #     n.add_link(link=Link(metric, _from=n.get_node_by_id(12), _to=n.get_node_by_id(22)))
        
    #     self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=1), set([1,10]))
    #     self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=2), set([2,11,20]))
    #     self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=3), set([12,21]))
    #     self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=4), set([22]))
    #     self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=5), set([]))

    # def test_in_neighborhood_set(self):
    #     def metric(link):
    #         n1 = link._from.id
    #         n0 = link._to.id
    #         if n0 == 0 and n1 == 1: return 1
    #         if n0 == 0 and n1 == 10: return 1
    #         if n0 == 1 and n1 == 11: return 1
    #         if n0 == 10 and n1 == 11: return 1
    #         if n0 == 11 and n1 == 2: return 1
    #         if n0 == 2 and n1 == 3: return 1
    #         if n0 == 10 and n1 == 4: return 99
    #         return 99
    #     n = Network()
    #     n.add_node(node=Node(_id=0))
    #     n.add_node(node=Node(_id=1))
    #     n.add_node(node=Node(_id=10))
    #     n.add_node(node=Node(_id=11))
    #     n.add_node(node=Node(_id=2))
    #     n.add_node(node=Node(_id=3))
    #     n.add_node(node=Node(_id=4))
    #     n.add_link(link=Link(metric, _to=n.get_node_by_id(0), _from=n.get_node_by_id(1)))
    #     n.add_link(link=Link(metric, _to=n.get_node_by_id(0), _from=n.get_node_by_id(10)))

    #     n.add_link(link=Link(metric, _to=n.get_node_by_id(1), _from=n.get_node_by_id(11)))

    #     n.add_link(link=Link(metric, _to=n.get_node_by_id(11), _from=n.get_node_by_id(2)))
    #     n.add_link(link=Link(metric, _to=n.get_node_by_id(2), _from=n.get_node_by_id(3)))

    #     n.add_link(link=Link(metric, _to=n.get_node_by_id(10), _from=n.get_node_by_id(4)))
        
    #     self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=1), set([1,10]))
    #     self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=2), set([11,4]))
    #     self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=3), set([2]))
    #     self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=4), set([3]))
    #     self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=5), set([]))
        

if __name__ == '__main__':
    unittest.main()