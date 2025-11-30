#!/usr/bin/env python3
"""Quick verification script for the generated topology."""

from rdflib import Graph
from collections import Counter

# Load the topology graph
g = Graph()
print("Loading topology graph...")
g.parse("datav2/data_hanoi_topology.ttl", format="turtle")

# Count predicates
predicates = Counter()
for s, p, o in g:
    pred_name = str(p).split("/")[-1].split("#")[-1]
    predicates[pred_name] += 1

print(f"\n📊 Total triples: {len(g):,}")
print("\nPredicate Distribution:")
for pred, count in predicates.most_common():
    print(f"  • {pred}: {count:,}")

# Count unique entities
subjects = set(str(s) for s, p, o in g)
objects = set(str(o) for s, p, o in g)
all_entities = subjects | objects

print(f"\n🔗 Unique entities involved: {len(all_entities):,}")
print(f"  • As sources: {len(subjects):,}")
print(f"  • As targets: {len(objects):,}")
