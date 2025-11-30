#!/usr/bin/env python3
"""
@File    : check_address_coverage.py
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

from rdflib import Graph, Namespace

categories = [
    'bus_stop', 'waste_basket', 'warehouse', 'parking', 
    'public_toilet', 'fuel_station', 'charging_station'
]

EXT = Namespace('http://opendatafithou.org/def/extension/')
SCHEMA = Namespace('http://schema.org/')

for cat in categories:
    g = Graph()
    g.parse(f'datav2/data_hanoi_{cat}.ttl', format='turtle')
    
    id_names = 0
    with_street = 0
    with_district = 0
    with_housenumber = 0
    with_any_addr = 0
    
    for s in g.subjects():
        # Check if has ID name
        name = None
        for o in g.objects(s, SCHEMA.name):
            name = str(o)
            break
        
        if name and '#' in name:
            id_names += 1
        
        # Check address components
        has_street = bool(list(g.objects(s, EXT.addr_street)))
        has_district = bool(list(g.objects(s, EXT.addr_district)))
        has_housenumber = bool(list(g.objects(s, EXT.addr_housenumber)))
        
        if has_street:
            with_street += 1
        if has_district:
            with_district += 1
        if has_housenumber:
            with_housenumber += 1
        if has_street or has_district or has_housenumber:
            with_any_addr += 1
    
    total = len(list(g.subjects()))
    print(f"\n{cat}:")
    print(f"  Total: {total}")
    print(f"  ID names: {id_names}")
    print(f"  With street: {with_street}")
    print(f"  With district: {with_district}")
    print(f"  With housenumber: {with_housenumber}")
    print(f"  With any address: {with_any_addr}")
    print(f"  No address: {total - with_any_addr}")
