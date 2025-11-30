#!/usr/bin/env python3
"""
@File    : test_cafe_only.py
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

from clean_all_remaining import UniversalDataCleaner

cleaner = UniversalDataCleaner()
result = cleaner.process_file(
    'datav2/data_hanoi_cafe.ttl',
    'datav2/cleaned/data_hanoi_cafe_cleaned.ttl'
)
print(f"cafe: {result['processed']} entities processed")
