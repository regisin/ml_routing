import unittest

from classes import Link, Node, Network

class TestNetworkMethods(unittest.TestCase):
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
        n.add_node(node=Node(_id=0, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=1, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=10, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=11, position=(0.0, 0.0, 0.0)))
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

        print('path:', path, 'reverse:', path_reverse)
        self.assertEqual(path[0], path_reverse[0])
        self.assertNotEqual(path[1], path_reverse[1])
        self.assertNotEqual(path[1], path_reverse[1].reverse())


    def test_neighborhood_set(self):
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
        n.add_node(node=Node(_id=0, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=1, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=10, position=(0.0, 0.0, 0.0)))
        n.add_node(node=Node(_id=11, position=(0.0, 0.0, 0.0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(0), _to=n.get_node_by_id(10)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(0)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(1), _to=n.get_node_by_id(11)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(1)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(10), _to=n.get_node_by_id(11)))
        n.add_link(link=Link(metric, _from=n.get_node_by_id(11), _to=n.get_node_by_id(10)))

        print('Out neighborhood test')
        _1hop_out_0 = set([nn.id for nn in n.get_out_nth_neighborhood_set(0)])
        _1hop_out_1 = set([nn.id for nn in n.get_out_nth_neighborhood_set(1)])
        _1hop_out_10 = set([nn.id for nn in n.get_out_nth_neighborhood_set(10)])
        _1hop_out_11 = set([nn.id for nn in n.get_out_nth_neighborhood_set(11)])
        print('1 hop:', {0:_1hop_out_0},
                        {1:_1hop_out_1},
                        {10:_1hop_out_10},
                        {11:_1hop_out_11})
        self.assertEqual(set([1,10]) , _1hop_out_0 )
        self.assertEqual(set([11,0]) , _1hop_out_1 )
        self.assertEqual(set([0,11]) , _1hop_out_10 )
        self.assertEqual(set([10,1]) , _1hop_out_11 )
        _2hop_out_0 = set([nn.id for nn in n.get_out_nth_neighborhood_set(0, hops=2)])
        _2hop_out_1 = set([nn.id for nn in n.get_out_nth_neighborhood_set(1, hops=2)])
        _2hop_out_10 = set([nn.id for nn in n.get_out_nth_neighborhood_set(10, hops=2)])
        _2hop_out_11 = set([nn.id for nn in n.get_out_nth_neighborhood_set(11, hops=2)])
        print('2 hop:', {0:_2hop_out_0},
                        {1:_2hop_out_1},
                        {10:_2hop_out_10},
                        {11:_2hop_out_11})
        self.assertEqual(set([11]) , _2hop_out_0 )
        self.assertEqual(set([10]) , _2hop_out_1 )
        self.assertEqual(set([1]) , _2hop_out_10 )
        self.assertEqual(set([0]) , _2hop_out_11 )

        print('In neighborhood test')
        _1hop_in_0 = set([nn.id for nn in n.get_in_nth_neighborhood_set(0)])
        _1hop_in_1 = set([nn.id for nn in n.get_in_nth_neighborhood_set(1)])
        _1hop_in_10 = set([nn.id for nn in n.get_in_nth_neighborhood_set(10)])
        _1hop_in_11 = set([nn.id for nn in n.get_in_nth_neighborhood_set(11)])
        self.assertEqual(set([1,10]) , _1hop_in_0 )
        self.assertEqual(set([11,0]) , _1hop_in_1 )
        self.assertEqual(set([0,11]) , _1hop_in_10 )
        self.assertEqual(set([10,1]) , _1hop_in_11 )
        print('1 hop:', {0:_1hop_in_0},
                        {1:_1hop_in_1},
                        {10:_1hop_in_10},
                        {11:_1hop_in_11})
        _2hop_in_0 = set([nn.id for nn in n.get_in_nth_neighborhood_set(0, hops=2)])
        _2hop_in_1 = set([nn.id for nn in n.get_in_nth_neighborhood_set(1, hops=2)])
        _2hop_in_10 = set([nn.id for nn in n.get_in_nth_neighborhood_set(10, hops=2)])
        _2hop_in_11 = set([nn.id for nn in n.get_in_nth_neighborhood_set(11, hops=2)])
        print('2 hop:', {0:_2hop_in_0},
                        {1:_2hop_in_1},
                        {10:_2hop_in_10},
                        {11:_2hop_in_11})
        self.assertEqual(set([11]) , _2hop_in_0 )
        self.assertEqual(set([10]) , _2hop_in_1 )
        self.assertEqual(set([1]) , _2hop_in_10 )
        self.assertEqual(set([0]) , _2hop_in_11 )



if __name__ == '__main__':
    unittest.main()