#!/usr/bin/env python3
"""
Example queries demonstrating the spatial topology capabilities.
"""

from rdflib import Graph, Namespace
from collections import Counter

# Load topology graph
print("Loading topology graph...")
g = Graph()
g.parse("datav2/data_hanoi_topology.ttl", format="turtle")

# Define namespaces
SCHEMA = Namespace("http://schema.org/")
EXT = Namespace("http://opendatafithou.org/def/extension/")
FIWARE = Namespace("https://smartdatamodels.org/dataModel.PointOfInterest/")

print(f"✓ Loaded {len(g):,} spatial relationships\n")
print("=" * 80)

# ============================================================================
# QUERY 1: Find all facilities within 50m (contained in place)
# ============================================================================
print("\n📍 QUERY 1: Facilities strictly contained within other facilities (≤50m)")
print("-" * 80)

query1 = """
PREFIX schema: <http://schema.org/>

SELECT ?source ?target
WHERE {
    ?source schema:containedInPlace ?target .
}
LIMIT 10
"""

results = g.query(query1)
for i, (source, target) in enumerate(results, 1):
    source_type = str(source).split(":")[-2]
    target_type = str(target).split(":")[-2]
    print(f"  {i}. {source_type} → {target_type}")

# Count by type
contained_pairs = [(str(s).split(":")[-2], str(t).split(":")[-2]) 
                   for s, t in g.query(query1.replace("LIMIT 10", ""))]
print(f"\nTotal: {len(contained_pairs)} containment relationships")
top_pairs = Counter(contained_pairs).most_common(5)
print("Top pairs:")
for (src, tgt), count in top_pairs:
    print(f"  • {src} → {tgt}: {count}")

# ============================================================================
# QUERY 2: Find bus-accessible schools
# ============================================================================
print("\n\n🚌 QUERY 2: Schools accessible by bus (via amenityFeature)")
print("-" * 80)

query2 = """
PREFIX schema: <http://schema.org/>
PREFIX fiware: <https://smartdatamodels.org/dataModel.PointOfInterest/>

SELECT ?bus_stop ?school
WHERE {
    ?bus_stop a schema:BusStop ;
              schema:amenityFeature ?school .
    ?school a schema:School .
}
LIMIT 15
"""

results = g.query(query2)
count = 0
for bus_stop, school in results:
    count += 1
    bus_id = str(bus_stop).split(":")[-1]
    school_id = str(school).split(":")[-1]
    print(f"  {count}. Bus stop {bus_id} serves school {school_id}")

total_query = query2.replace("LIMIT 15", "")
total_results = list(g.query(total_query))
print(f"\nTotal: {len(total_results)} bus-school connections")

# ============================================================================
# QUERY 3: Healthcare network (pharmacies near hospitals)
# ============================================================================
print("\n\n⚕️ QUERY 3: Pharmacies near hospitals/clinics")
print("-" * 80)

query3 = """
PREFIX schema: <http://schema.org/>

SELECT ?pharmacy ?healthcare
WHERE {
    ?pharmacy a schema:Pharmacy ;
              schema:isNextTo ?healthcare .
    { ?healthcare a schema:Hospital } UNION { ?healthcare a schema:Clinic }
}
LIMIT 10
"""

results = g.query(query3)
for i, (pharmacy, healthcare) in enumerate(results, 1):
    pharm_id = str(pharmacy).split(":")[-1]
    health_id = str(healthcare).split(":")[-1]
    health_type = "Hospital" if "hospital" in str(healthcare) else "Clinic"
    print(f"  {i}. Pharmacy {pharm_id} next to {health_type} {health_id}")

# ============================================================================
# QUERY 4: Find well-connected hubs (most outgoing links)
# ============================================================================
print("\n\n🌟 QUERY 4: Most connected amenities (top hubs)")
print("-" * 80)

query4 = """
PREFIX schema: <http://schema.org/>

SELECT ?entity (COUNT(?target) as ?connections)
WHERE {
    ?entity ?predicate ?target .
}
GROUP BY ?entity
ORDER BY DESC(?connections)
LIMIT 10
"""

results = g.query(query4)
for i, (entity, connections) in enumerate(results, 1):
    entity_type = str(entity).split(":")[-2]
    entity_id = str(entity).split(":")[-1]
    print(f"  {i}. {entity_type} {entity_id}: {connections} connections")

# ============================================================================
# QUERY 5: Emergency service network
# ============================================================================
print("\n\n🚨 QUERY 5: Emergency service network")
print("-" * 80)

query5 = """
PREFIX ext: <http://opendatafithou.org/def/extension/>
PREFIX schema: <http://schema.org/>

SELECT ?source ?target
WHERE {
    ?source ext:emergencyService ?target .
}
"""

results = g.query(query5)
emergency_pairs = []
for source, target in results:
    src_type = str(source).split(":")[-2].replace("_", " ").title()
    tgt_type = str(target).split(":")[-2].replace("_", " ").title()
    emergency_pairs.append((src_type, tgt_type))

if emergency_pairs:
    pair_counts = Counter(emergency_pairs)
    for (src, tgt), count in pair_counts.most_common():
        print(f"  • {src} ↔ {tgt}: {count} connections")
else:
    print("  No emergency service connections found")

# ============================================================================
# QUERY 6: Find parking with public access
# ============================================================================
print("\n\n🅿️ QUERY 6: Parking facilities with public access")
print("-" * 80)

query6 = """
PREFIX schema: <http://schema.org/>

SELECT ?parking ?destination
WHERE {
    ?parking schema:publicAccess ?destination .
}
LIMIT 10
"""

results = g.query(query6)
for i, (parking, destination) in enumerate(results, 1):
    park_id = str(parking).split(":")[-1]
    dest_type = str(destination).split(":")[-2].replace("_", " ").title()
    dest_id = str(destination).split(":")[-1]
    print(f"  {i}. Parking {park_id} serves {dest_type} {dest_id}")

print("\n" + "=" * 80)
print("✅ Example queries completed!")
print("\nFor more advanced queries, see SPARQL documentation at:")
print("https://www.w3.org/TR/sparql11-query/")
