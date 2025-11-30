#!/usr/bin/env python3
"""Check cafes with ID-based names that have addresses."""

from rdflib import Graph, Namespace, Literal

# Load graph
g = Graph()
print("Loading cafe data...")
g.parse('datav2/data_hanoi_cafe.ttl', format='turtle')

SCHEMA = Namespace('http://schema.org/')
EXT = Namespace('http://opendatafithou.org/def/extension/')

count = 0
found = 0

for s in g.subjects():
    # Get names
    vi_names = [str(o) for o in g.objects(s, SCHEMA.name) if isinstance(o, Literal) and o.language == 'vi']
    
    if not vi_names:
        continue
    
    vi_name = vi_names[0]
    
    # Check if ID-based
    if '#' not in vi_name:
        continue
    
    # Check for address
    streets = list(g.objects(s, EXT.addr_street))
    districts = list(g.objects(s, EXT.addr_district))
    cities = list(g.objects(s, EXT.addr_city))
    
    if streets or districts or cities:
        found += 1
        print(f"\n{found}. {s}")
        print(f"   Current name: {vi_name}")
        if streets:
            print(f"   Street: {streets[0]}")
        if districts:
            print(f"   District: {districts[0]}")
        if cities:
            print(f"   City: {cities[0]}")
        
        if found >= 10:
            break

print(f"\nTotal found: {found} cafes with ID-based names that have addresses")
