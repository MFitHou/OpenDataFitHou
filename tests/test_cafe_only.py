#!/usr/bin/env python3
"""Test process single category."""

from clean_all_remaining import UniversalDataCleaner

cleaner = UniversalDataCleaner()
result = cleaner.process_file(
    'datav2/data_hanoi_cafe.ttl',
    'datav2/cleaned/data_hanoi_cafe_cleaned.ttl'
)
print(f"cafe: {result['processed']} entities processed")
