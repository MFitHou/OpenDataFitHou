#!/usr/bin/env python3
"""Test get_location_based_name for a specific cafe."""

from rdflib import Graph, Namespace, URIRef, Literal
import re

# Load graph
g = Graph()
print("Loading cafe data...")
g.parse('datav2/data_hanoi_cafe.ttl', format='turtle')

SCHEMA = Namespace('http://schema.org/')
EXT = Namespace('http://opendatafithou.org/def/extension/')
FIWARE = Namespace('https://smartdatamodels.org/dataModel.PointOfInterest/')

# Test entity
subject = URIRef('urn:ngsi-ld:PointOfInterest:Hanoi:cafe:12078122282')

print(f"\nTesting entity: {subject}")

# Get current names
vi_name = None
en_name = None
for o in g.objects(subject, SCHEMA.name):
    if isinstance(o, Literal):
        if o.language == 'vi':
            vi_name = str(o)
        elif o.language == 'en':
            en_name = str(o)

print(f"Current VI: {vi_name}")
print(f"Current EN: {en_name}")

# Get address
street = None
for o in g.objects(subject, EXT.addr_street):
    if isinstance(o, Literal):
        street = str(o)
        break

district = None
for o in g.objects(subject, EXT.addr_district):
    if isinstance(o, Literal):
        district = str(o)
        break

city = None
for o in g.objects(subject, EXT.addr_city):
    if isinstance(o, Literal):
        city = str(o)
        break

print(f"Street: {street}")
print(f"District: {district}")
print(f"City: {city}")

# Simulate get_location_based_name logic
category = 'cafe'
generic_vi = 'Quán cà phê'
generic_en = 'Cafe'

if street:
    new_vi = f"{generic_vi} tại {street}"
    new_en = f"{generic_en} at {street}"
elif district:
    new_vi = f"{generic_vi} tại {district}"
    new_en = f"{generic_en} at {district}"
elif city:
    new_vi = f"{generic_vi} tại {city}"
    new_en = f"{generic_en} at {city}"
else:
    new_vi = None
    new_en = None

print(f"\nGenerated VI: {new_vi}")
print(f"Generated EN: {new_en}")

# Check if generic
def is_generic(name):
    if not name:
        return True
    pattern = r'^[\w\s]+\s*#\d+$'
    return bool(re.match(pattern, name.lower()))

print(f"\nCurrent VI is generic: {is_generic(vi_name)}")
print(f"Current EN is generic: {is_generic(en_name)}")
print(f"New VI is generic: {is_generic(new_vi)}")
print(f"New EN is generic: {is_generic(new_en)}")

should_replace = False
if new_vi and new_en:
    if not is_generic(new_vi) or not is_generic(new_en):
        should_replace = True

print(f"\nShould replace: {should_replace}")
