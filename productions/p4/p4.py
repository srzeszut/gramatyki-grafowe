from productions.production_base import Production

class P4(Production):
    """
    Production P4: Break boundary edges marked for refinement.
    It sets value of attribute R of each hyperedge with label E to 0.
    """

    def __init__(self):
        super().__init__(
            name="P4",
            description="Unmark boundary edges (E) previously marked for refinement (R:1 -> 0)"
        )

    def can_apply(self, graph, hyperedge=None):
        """Check if P4 can be applied to the graph.

        Args:
            hyperedge: Optional hyperedge to check; otherwise check all.
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            if not edge.is_border:
                continue

            if edge.label != "E":
                continue

            if edge.R != 1:
                continue

            return True, {'hyperedge': edge}


        return False, None

    def apply(self, graph, matched_elements):
        """Apply P4: break boundary edge marked for refinement into two edges with a new node in the middle."""
        edge = matched_elements['hyperedge']

        n1, n2 = edge.nodes

        x_mid = (n1.x + n2.x) / 2
        y_mid = (n1.y + n2.y) / 2
        new_node = graph.add_node(x_mid, y_mid)

        e1 = graph.add_hyperedge([n1, new_node], label="E")
        e1.R = 0
        e1.is_border = edge.is_border
        e2 = graph.add_hyperedge([new_node, n2], label="E")
        e2.R = 0
        e2.is_border = edge.is_border

        graph.remove_edge(edge)


        print(f"[{self.name}] Boundary edge broken into two edges with new node")
        print(f"[{self.name}] New node: {new_node}")
        print(f"[{self.name}] New edges: {e1}, {e2}")

        return {
            'new_node': new_node,
            'new_edges': [e1, e2]
        }