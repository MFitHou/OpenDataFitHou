#!/usr/bin/env python3
"""Debug: Test why cafes are not being processed."""

from rdflib import Graph, Namespace, URIRef, Literal
import re

def is_generic_or_unknown(name):
    if not name:
        return True
    name_str = str(name).strip().lower()
    generic_patterns = [
        'unknown', 'n/a', '', 'unnamed',
        r'^[\w\s]+\s*#\d+$',
    ]
    for pattern in generic_patterns:
        if re.match(pattern, name_str):
            return True
    return False

# Load graph
g = Graph()
print("Loading cafe data...")
g.parse('datav2/data_hanoi_cafe.ttl', format='turtle')

SCHEMA = Namespace('http://schema.org/')
EXT = Namespace('http://opendatafithou.org/def/extension/')

# Test specific entity
subject = URIRef('urn:ngsi-ld:PointOfInterest:Hanoi:cafe:12078122282')

print(f"\n=== Testing entity: {subject} ===\n")

# Get names
vi_name = None
en_name = None
for o in g.objects(subject, SCHEMA.name):
    if isinstance(o, Literal):
        if o.language == 'vi':
            vi_name = str(o)
        elif o.language == 'en':
            en_name = str(o)

print(f"Step 1: Get current names")
print(f"  vi_name = '{vi_name}'")
print(f"  en_name = '{en_name}'")

# Check if good
vi_is_good = vi_name and not is_generic_or_unknown(vi_name)
en_is_good = en_name and not is_generic_or_unknown(en_name)

print(f"\nStep 2: Check if names are good")
print(f"  vi_is_good = {vi_is_good}")
print(f"  en_is_good = {en_is_good}")

if vi_is_good:
    print("\n  -> VI name is good, would try semantic translation")
    print("  -> This entity won't get location-based name")
else:
    print("\n  -> VI name is generic, will try location-based")
    
    # Get address
    street = None
    district = None
    city = None
    for o in g.objects(subject, EXT.addr_street):
        street = str(o) if isinstance(o, Literal) else None
        break
    for o in g.objects(subject, EXT.addr_district):
        district = str(o) if isinstance(o, Literal) else None
        break
    for o in g.objects(subject, EXT.addr_city):
        city = str(o) if isinstance(o, Literal) else None
        break
    
    print(f"\nStep 3: Get address info")
    print(f"  street = {street}")
    print(f"  district = {district}")
    print(f"  city = {city}")
    
    # Generate location name
    generic_vi = 'Quán cà phê'
    generic_en = 'Cafe'
    
    if street:
        vi_fallback = f"{generic_vi} tại {street}"
        en_fallback = f"{generic_en} at {street}"
    elif district:
        vi_fallback = f"{generic_vi} tại {district}"
        en_fallback = f"{generic_en} at {district}"
    elif city:
        vi_fallback = f"{generic_vi} tại {city}"
        en_fallback = f"{generic_en} at {city}"
    else:
        vi_fallback = None
        en_fallback = None
    
    print(f"\nStep 4: Generate location-based names")
    print(f"  vi_fallback = '{vi_fallback}'")
    print(f"  en_fallback = '{en_fallback}'")
    
    if vi_fallback and en_fallback:
        new_vi_is_generic = is_generic_or_unknown(vi_fallback)
        new_en_is_generic = is_generic_or_unknown(en_fallback)
        
        print(f"\nStep 5: Check if new names are generic")
        print(f"  new_vi_is_generic = {new_vi_is_generic}")
        print(f"  new_en_is_generic = {new_en_is_generic}")
        
        should_replace = False
        
        if not new_vi_is_generic and not new_en_is_generic:
            should_replace = True
            print(f"\n  -> Both new names are good (not generic)")
        elif (not new_vi_is_generic or not new_en_is_generic):
            if vi_fallback != vi_name or en_fallback != en_name:
                should_replace = True
                print(f"\n  -> At least one new name is better and different")
        
        print(f"\nStep 6: Final decision")
        print(f"  should_replace = {should_replace}")
        
        if should_replace:
            print(f"\n  ✓ WOULD REPLACE:")
            print(f"    Old VI: '{vi_name}' -> New VI: '{vi_fallback}'")
            print(f"    Old EN: '{en_name}' -> New EN: '{en_fallback}'")
        else:
            print(f"\n  ✗ WOULD NOT REPLACE (no improvement)")
    else:
        print(f"\n  ✗ No location-based names generated")
