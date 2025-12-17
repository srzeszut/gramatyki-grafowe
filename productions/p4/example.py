import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p4.p4 import P4  

output_dir = "./productions/p4/outputs"
os.makedirs(output_dir, exist_ok=True)

graph1 = HyperGraph()
production = P4()

n1 = graph1.add_node(0, 0)
n2 = graph1.add_node(1, 0)

e1 = graph1.add_hyperedge([n1, n2], label="E")
e1.R = 1
e1.B = True  # Mark as boundary edge 
graph1.visualize(os.path.join(output_dir, "example_p4_before.png"))

can_apply, matched = production.can_apply(graph1,e1)
if can_apply:
    production.apply(graph1, matched)

graph1.visualize(os.path.join(output_dir, "example_p4_after.png"))
