import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from hypergraph.hypergraph import HyperGraph
from productions.p4.p4 import P4

class TestP4(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P4()

    def test_can_apply_single_edge(self):
        """Test P4 can be applied to a single boundary edge marked for refinement."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)

        e = self.graph.add_hyperedge([n1, n2], label="E")
        e.R = 1
        e.is_border = True

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched['hyperedge'], e)

    def test_cannot_apply_unmarked_edge(self):
        """Test P4 cannot be applied to a boundary edge with R=0."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)

        e = self.graph.add_hyperedge([n1, n2], label="E")
        e.R = 0
        e.is_border = True

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_non_border_edge(self):
        """Test P4 cannot be applied to a non-boundary edge even if R=1."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)

        e = self.graph.add_hyperedge([n1, n2], label="E")
        e.R = 1
        e.is_border = False  

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_wrong_label(self):
        """Test P4 ignores edges with wrong label (e.g. 'Q') even if R=1 and Border=True."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)

        e = self.graph.add_hyperedge([n1, n2], label="Q")
        e.R = 1
        e.is_border = True

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)

    def test_apply_breaks_edge(self):
        """Test that applying P4 removes the old edge and creates two new ones."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0) 
        e = self.graph.add_hyperedge([n1, n2], label="E")
        e.R = 1
        e.is_border = True

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        
        result = self.production.apply(self.graph, matched)
        new_node = result['new_node']
        new_edges = result['new_edges']

        self.assertAlmostEqual(new_node.x, 1.0)
        self.assertAlmostEqual(new_node.y, 0.0)


        self.assertNotIn(e, self.graph.edges)

        self.assertEqual(len(new_edges), 2)
        
        for ne in new_edges:
            self.assertIn(ne, self.graph.edges)
            self.assertEqual(ne.label, "E")
            self.assertEqual(ne.R, 0)
            self.assertTrue(ne.is_border) 
            self.assertIn(new_node, ne.nodes) 

    def test_complex_shape_with_diagonals(self):
        """Test P4 on a pentagon. Verifies it ignores internal diagonals even if R=1."""
     
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(3, 2)
        n4 = self.graph.add_node(1.5, 3)
        n5 = self.graph.add_node(0, 2)

        boundary_edges = [
            self.graph.add_hyperedge([n1, n2], label="E"), 
            self.graph.add_hyperedge([n2, n3], label="E"), 
            self.graph.add_hyperedge([n3, n4], label="E"), 
            self.graph.add_hyperedge([n4, n5], label="E"),
            self.graph.add_hyperedge([n5, n1], label="E")  
        ]

        edges_to_split = []
        for i, e in enumerate(boundary_edges):
            e.is_border = True
            if i % 2 == 0:
                e.R = 1
                edges_to_split.append(e)
            else:
                e.R = 0

        diag1 = self.graph.add_hyperedge([n1, n3], label="E")
        diag2 = self.graph.add_hyperedge([n2, n4], label="E")
        
        diag1.is_border = False
        diag1.R = 1 
        diag2.is_border = False
        diag2.R = 0

        applied_count = 0
        while True:
            can_apply, matched = self.production.can_apply(self.graph)
            if not can_apply:
                break
            self.production.apply(self.graph, matched)
            applied_count += 1

        self.assertEqual(applied_count, 3) 

        for old_edge in edges_to_split:
            self.assertNotIn(old_edge, self.graph.edges)

        self.assertIn(diag1, self.graph.edges)
        self.assertEqual(diag1.R, 1) 

        self.assertIn(boundary_edges[1], self.graph.edges)
        self.assertIn(boundary_edges[3], self.graph.edges)

if __name__ == '__main__':
    unittest.main(verbosity=2)