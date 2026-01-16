import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p4.p4 import P4  

output_dir = "./productions/p4/outputs"
os.makedirs(output_dir, exist_ok=True)


print("\n--- Test 1: Single boundary edge with R=1 ---")
graph1 = HyperGraph()
production = P4()

n1 = graph1.add_node(0, 0)
n2 = graph1.add_node(1, 0)

e = graph1.add_hyperedge([n1, n2], label="E")
e.R = 1
e.is_border = True

graph1.visualize(os.path.join(output_dir, "p4_test1_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)

graph1.visualize(os.path.join(output_dir, "p4_test1_after.png"))


print("\n--- Test 2: Boundary edge but R=0 (should not apply) ---")
graph2 = HyperGraph()
production2 = P4()

n1 = graph2.add_node(0, 0)
n2 = graph2.add_node(1, 0)

e = graph2.add_hyperedge([n1, n2], label="E")
e.R = 0
e.is_border = True

graph2.visualize(os.path.join(output_dir, "p4_test2_before.png"))

can_apply, matched = production2.can_apply(graph2)
print("Can apply:", can_apply) 

graph2.visualize(os.path.join(output_dir, "p4_test2_after.png"))


print("\n--- Test 3: Non-boundary edge with R=1 (should not apply) ---")
graph3 = HyperGraph()
production3 = P4()

n1 = graph3.add_node(0, 0)
n2 = graph3.add_node(1, 0)

e = graph3.add_hyperedge([n1, n2], label="E")
e.R = 1
e.is_border = False

graph3.visualize(os.path.join(output_dir, "p4_test3_before.png"))

can_apply, matched = production3.can_apply(graph3)
print("Can apply:", can_apply) 

graph3.visualize(os.path.join(output_dir, "p4_test3_after.png"))


print("\n--- Test 4: Multiple boundary edges, only one marked ---")
graph4 = HyperGraph()
production4 = P4()

n1 = graph4.add_node(0, 0)
n2 = graph4.add_node(1, 0)
n3 = graph4.add_node(2, 0)

e1 = graph4.add_hyperedge([n1, n2], label="E")
e1.R = 1
e1.is_border = True

e2 = graph4.add_hyperedge([n2, n3], label="E")
e2.R = 0
e2.is_border = True

graph4.visualize(os.path.join(output_dir, "p4_test4_before.png"))

can_apply, matched = production4.can_apply(graph4)
if can_apply:
    production4.apply(graph4, matched)

graph4.visualize(os.path.join(output_dir, "p4_test4_after.png"))


print("\n--- Test 5: Pentagon with selective boundary refinement ---")
graph5 = HyperGraph()
production_p4 = P4()

n1 = graph5.add_node(2.0, 4.0) 
n2 = graph5.add_node(4.0, 2.5)  
n3 = graph5.add_node(3.2, 0.0)  
n4 = graph5.add_node(0.8, 0.0)  
n5 = graph5.add_node(0.0, 2.5)  

edges = [
    graph5.add_hyperedge([n1, n2], label="E"), 
    graph5.add_hyperedge([n2, n3], label="E"), 
    graph5.add_hyperedge([n3, n4], label="E"), 
    graph5.add_hyperedge([n4, n5], label="E"), 
    graph5.add_hyperedge([n5, n1], label="E") 
]

for e in edges:
    e.is_border = True 
    e.R = 0           

edges[0].R = 1 
edges[2].R = 1 
edges[4].R = 1 

diag1 = graph5.add_hyperedge([n1, n3], label="E")
diag1.is_border = False
diag1.R = 1 

graph5.visualize(os.path.join(output_dir, "p4_test5_before.png"))

iteration = 0
while True:
    can_apply, matched = production_p4.can_apply(graph5)
    
    if not can_apply:
        break
    
    iteration += 1
    
    production_p4.apply(graph5, matched)

graph5.visualize(os.path.join(output_dir, "p4_test5_after.png"))