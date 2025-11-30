#!/usr/bin/env python3
"""
@File    : test_housenumber.py
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

from rdflib import Graph, Namespace, URIRef, Literal
import re

def is_generic_or_unknown(name):
    if not name:
        return True
    name_str = str(name).strip().lower()
    if not name_str:
        return True
    generic_words = ['unknown', 'n/a', 'unnamed']
    if name_str in generic_words:
        return True
    id_pattern = r'^[\w\s]+\s*#\d+$'
    if re.match(id_pattern, name_str):
        return True
    return False

# Load graph
g = Graph()
print("Loading cafe data...")
g.parse('datav2/data_hanoi_cafe.ttl', format='turtle')

SCHEMA = Namespace('http://schema.org/')
EXT = Namespace('http://opendatafithou.org/def/extension/')

# Test entity with house number only
subject = URIRef('urn:ngsi-ld:PointOfInterest:Hanoi:cafe:10239384810')

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

print(f"Current names:")
print(f"  VI: {vi_name}")
print(f"  EN: {en_name}")

print(f"\nIs generic:")
print(f"  VI generic: {is_generic_or_unknown(vi_name)}")
print(f"  EN generic: {is_generic_or_unknown(en_name)}")

# Get address
housenumber = None
for o in g.objects(subject, EXT.addr_housenumber):
    if isinstance(o, Literal):
        housenumber = str(o)
        break

street = None
for o in g.objects(subject, EXT.addr_street):
    if isinstance(o, Literal):
        street = str(o)
        break

print(f"\nAddress info:")
print(f"  House number: {housenumber}")
print(f"  Street: {street}")

if housenumber and not street:
    new_vi = f"Quán cà phê số {housenumber}"
    new_en = f"Cafe No. {housenumber}"
    print(f"\nShould generate:")
    print(f"  New VI: {new_vi}")
    print(f"  New EN: {new_en}")
    print(f"  New VI generic: {is_generic_or_unknown(new_vi)}")
    print(f"  New EN generic: {is_generic_or_unknown(new_en)}")
