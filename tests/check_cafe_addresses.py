#!/usr/bin/env python3
"""
@File    : check_cafe_addresses.py
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
