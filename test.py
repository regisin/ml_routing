import unittest

from classes import Node, Link, Network
from utils import sort_by_initial_charge, sort_by_remaining_charge, sort_by_remaining_energy

# _id=None, position=(.0,.0,.0), initial_charge=1000.0, up_current=1.0, down_current=0.5):
class TestNetworkMethods(unittest.TestCase):
    def test_sort_by_initial_charge(self):
        n = Network()
        
        n0=Node(_id=0, initial_charge=1.0)
        n1=Node(_id=1, initial_charge=2.0)
        n2=Node(_id=2, initial_charge=3.0)
        
        n.add_node(node=n0)
        n.add_node(node=n1)
        n.add_node(node=n2)

        self.assertEqual([n0, n1, n2], sort_by_initial_charge(n, set([0,1,2])))
        self.assertNotEqual([n0, n2, n1], sort_by_initial_charge(n, set([0,1,2])))
        self.assertNotEqual([n1, n0, n2], sort_by_initial_charge(n, set([0,1,2])))
        self.assertNotEqual([n1, n2, n0], sort_by_initial_charge(n, set([0,1,2])))
        self.assertNotEqual([n2, n0, n1], sort_by_initial_charge(n, set([0,1,2])))
        self.assertNotEqual([n2, n1, n0], sort_by_initial_charge(n, set([0,1,2])))

    def test_directed_dijkstra(self):
        def metric(link):
            n0 = link._from.id
            n1 = link._to.id
            if n0 == 0 and n1 == 1: return 2
            if n0 == 0 and n1 == 10: return 3
            if n0 == 1 and n1 == 11: return 2
            if n0 == 1 and n1 == 0: return 3
            if n0 == 10 and n1 == 11: return 3
            if n0 == 10 and n1 == 0: return 2
            if n0 == 11 and n1 == 1: return 3
            if n0 == 11 and n1 == 10: return 2
            return 99
        n = Network()
        n.add_node(node=Node(_id=0))
        n.add_node(node=Node(_id=1))
        n.add_node(node=Node(_id=10))
        n.add_node(node=Node(_id=11))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(10)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(11)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(11)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(10)))

        path = n.shortest_path(source=n.get_node_by_id(0), destination=n.get_node_by_id(11))
        path_reverse = n.shortest_path(source=n.get_node_by_id(11), destination=n.get_node_by_id(0))

        self.assertEqual(path[0], path_reverse[0])
        self.assertNotEqual(path[1], path_reverse[1])
        self.assertNotEqual(path[1], path_reverse[1].reverse())
    
    def test_disconected_graph(self):
        def metric(link):
            return 1
        n = Network()
        n.add_node(node=Node(_id=0))
        n.add_node(node=Node(_id=1))
        n.add_node(node=Node(_id=2))
        # n.add_node(node=Node(_id=3))
        # n.add_node(node=Node(_id=4))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(2)))
        # n.add_link(link=Link(metric, _from=n.get_node_by_id(3), _to=n.get_node_by_id(2)))

        path = n.shortest_path(source=n.get_node_by_id(0), destination=n.get_node_by_id(2))
        path_reverse = n.shortest_path(source=n.get_node_by_id(3), destination=n.get_node_by_id(2))
        print(path, path_reverse)

        # self.assertEqual(path[0], path_reverse[0])
        # self.assertNotEqual(path[1], path_reverse[1])
        # self.assertNotEqual(path[1], path_reverse[1].reverse())


    def test_out_neighborhood_set(self):
        def metric(link):
            return 1
        n = Network()
        n.add_node(node=Node(_id=0))
        n.add_node(node=Node(_id=1))
        n.add_node(node=Node(_id=2))
        n.add_node(node=Node(_id=10))
        n.add_node(node=Node(_id=11))
        n.add_node(node=Node(_id=12))
        n.add_node(node=Node(_id=20))
        n.add_node(node=Node(_id=21))
        n.add_node(node=Node(_id=22))
        
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(2)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(11)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(12)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(20), _to=n.get_node_by_id(21)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(21), _to=n.get_node_by_id(22)))
        
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(10)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(20)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(11)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(21)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(2), _to=n.get_node_by_id(12)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(12), _to=n.get_node_by_id(22)))
        
        self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=1), set([1,10]))
        self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=2), set([2,11,20]))
        self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=3), set([12,21]))
        self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=4), set([22]))
        self.assertEqual(n.get_out_nth_neighborhood_set(0, hops=5), set([]))

    def test_in_neighborhood_set(self):
        def metric(link):
            n1 = link._from.id
            n0 = link._to.id
            if n0 == 0 and n1 == 1: return 1
            if n0 == 0 and n1 == 10: return 1
            if n0 == 1 and n1 == 11: return 1
            if n0 == 10 and n1 == 11: return 1
            if n0 == 11 and n1 == 2: return 1
            if n0 == 2 and n1 == 3: return 1
            if n0 == 10 and n1 == 4: return 99
            return 99
        n = Network()
        n.add_node(node=Node(_id=0))
        n.add_node(node=Node(_id=1))
        n.add_node(node=Node(_id=10))
        n.add_node(node=Node(_id=11))
        n.add_node(node=Node(_id=2))
        n.add_node(node=Node(_id=3))
        n.add_node(node=Node(_id=4))
        n.add_link(link=Link(metric, _to=n.get_node_by_id(0), _from=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _to=n.get_node_by_id(0), _from=n.get_node_by_id(10)))

        n.add_link(link=Link(metric, _to=n.get_node_by_id(1), _from=n.get_node_by_id(11)))

        n.add_link(link=Link(metric, _to=n.get_node_by_id(11), _from=n.get_node_by_id(2)))
        n.add_link(link=Link(metric, _to=n.get_node_by_id(2), _from=n.get_node_by_id(3)))

        n.add_link(link=Link(metric, _to=n.get_node_by_id(10), _from=n.get_node_by_id(4)))
        
        self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=1), set([1,10]))
        self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=2), set([11,4]))
        self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=3), set([2]))
        self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=4), set([3]))
        self.assertEqual(n.get_in_nth_neighborhood_set(0, hops=5), set([]))
        

if __name__ == '__main__':
    unittest.main()