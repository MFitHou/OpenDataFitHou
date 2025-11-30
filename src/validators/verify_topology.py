#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    : verify_topology.py
@Project : OpenDataFitHou
@Date    : 2025-11-30 19:00:00
@Author  : MFitHou Team

Part of OpenDataFitHou - Ứng dụng dữ liệu mở liên kết phục vụ chuyển đổi số

Copyright (C) 2025 FITHOU

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

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
