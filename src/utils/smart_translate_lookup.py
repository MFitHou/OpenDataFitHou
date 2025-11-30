"""
@File    : smart_translate_lookup.py
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

import re
import json
import os
import time
import requests
from typing import Optional, Dict, Tuple
import unicodedata

class SmartTranslator:
    """
    Intelligent translator using Wikidata API with caching and pattern-based fallback.
    """
    
    def __init__(self, cache_file: str = "translation_cache.json"):
        """
        Initialize the translator with cache support.
        
        Args:
            cache_file: Path to JSON cache file
        """
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.api_call_count = 0
        self.cache_hit_count = 0
        
        # Wikidata API endpoint
        self.wikidata_api = "https://www.wikidata.org/w/api.php"
        
        # Generic prefixes to remove (often found in OSM but not official names)
        self.prefixes_to_remove = [
            r'^Địa\s+chỉ:\s*',
            r'^Số\s+\d+\s*',
            r'^Trụ\s+sở\s+',
            r'^Văn\s+phòng\s+',
            r'^Chi\s+nhánh\s+',
        ]
        
        # Abbreviation standardization
        self.abbreviations = {
            r'\bĐH\b': 'Đại học',
            r'\bTHPT\b': 'Trường Trung học phổ thông',
            r'\bTHCS\b': 'Trường Trung học cơ sở',
            r'\bTH\b': 'Trường Tiểu học',
            r'\bMN\b': 'Trường Mầm non',
            r'\bBV\b': 'Bệnh viện',
            r'\bTT\b': 'Trung tâm',
            r'\bCty\b': 'Công ty',
            r'\bUBND\b': 'Ủy ban Nhân dân',
            r'\bTP\b': 'Thành phố',
            r'\bQ\.\s*': 'Quận ',
            r'\bP\.\s*': 'Phường ',
            r'\bPGD\b': 'Phòng Giáo dục',
        }
        
        # Pattern-based translation rules for common structures
        self.pattern_translations = [
            # Administrative units
            (r'^Ủy\s+ban\s+Nhân\s+dân\s+(.+)$', r'People\'s Committee of \1'),
            (r'^UBND\s+(.+)$', r'People\'s Committee of \1'),
            (r'^Nhà\s+văn\s+hóa\s+(.+)$', r'Cultural House of \1'),
            (r'^Tổ\s+dân\s+phố\s+(\d+)$', r'Residential Group \1'),
            (r'^Khu\s+dân\s+cư\s+(.+)$', r'Residential Area \1'),
            
            # Education patterns
            (r'^Trường\s+Đại\s+học\s+(.+)$', r'\1 University'),
            (r'^Đại\s+học\s+(.+)$', r'\1 University'),
            (r'^Trường\s+Trung\s+học\s+phổ\s+thông\s+(.+)$', r'\1 High School'),
            (r'^Trường\s+THPT\s+(.+)$', r'\1 High School'),
            (r'^Trường\s+Trung\s+học\s+cơ\s+sở\s+(.+)$', r'\1 Secondary School'),
            (r'^Trường\s+THCS\s+(.+)$', r'\1 Secondary School'),
            (r'^Trường\s+Tiểu\s+học\s+(.+)$', r'\1 Primary School'),
            (r'^Trường\s+Mầm\s+non\s+(.+)$', r'\1 Kindergarten'),
            (r'^Thư\s+viện\s+(.+)$', r'\1 Library'),
            
            # Medical patterns
            (r'^Bệnh\s+viện\s+(.+)$', r'\1 Hospital'),
            (r'^Phòng\s+khám\s+(.+)$', r'\1 Clinic'),
            (r'^Nhà\s+thuốc\s+(.+)$', r'\1 Pharmacy'),
            (r'^Trung\s+tâm\s+Y\s+tế\s+(.+)$', r'\1 Medical Center'),
            
            # Emergency services
            (r'^Đồn\s+Công\s+an\s+(.+)$', r'\1 Police Station'),
            (r'^Công\s+an\s+(.+)$', r'\1 Police'),
            (r'^Trạm\s+Cứu\s+hỏa\s+(.+)$', r'\1 Fire Station'),
            
            # Commercial patterns
            (r'^Ngân\s+hàng\s+(.+)$', r'\1 Bank'),
            (r'^Siêu\s+thị\s+(.+)$', r'\1 Supermarket'),
            (r'^Cửa\s+hàng\s+(.+)$', r'\1 Store'),
            (r'^Nhà\s+hàng\s+(.+)$', r'\1 Restaurant'),
            (r'^Quán\s+(.+)$', r'\1 Shop'),
            (r'^Chợ\s+(.+)$', r'\1 Market'),
            (r'^Bưu\s+điện\s+(.+)$', r'\1 Post Office'),
            
            # Infrastructure
            (r'^Công\s+viên\s+(.+)$', r'\1 Park'),
            (r'^Bãi\s+đỗ\s+xe\s+(.+)$', r'\1 Parking'),
            (r'^Trạm\s+xe\s+buýt\s+(.+)$', r'\1 Bus Stop'),
            (r'^Trạm\s+xăng\s+(.+)$', r'\1 Gas Station'),
        ]
        
        # Special cases dictionary (for well-known entities)
        self.special_cases = {
            'Đại học Quốc gia Hà Nội': 'Vietnam National University, Hanoi',
            'Đại học Bách khoa Hà Nội': 'Hanoi University of Science and Technology',
            'Đại học Kiểm sát Hà Nội': 'Hanoi Procuratorate University',
            'Bệnh viện Bạch Mai': 'Bach Mai Hospital',
            'Bệnh viện Việt Đức': 'Viet Duc Hospital',
            'Bệnh viện K': 'K Hospital',
            'Bệnh viện Nhi Trung ương': 'National Children\'s Hospital',
            'Hồ Hoàn Kiếm': 'Hoan Kiem Lake',
            'Chợ Đồng Xuân': 'Dong Xuan Market',
        }
    
    def _load_cache(self) -> Dict[str, str]:
        """Load translation cache from JSON file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Save translation cache to JSON file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _normalize_vietnamese_name(self, name: str) -> str:
        """
        Normalize Vietnamese name before searching.
        
        Args:
            name: Original Vietnamese name
            
        Returns:
            Normalized name
        """
        if not name:
            return name
        
        # Remove generic prefixes
        for prefix_pattern in self.prefixes_to_remove:
            name = re.sub(prefix_pattern, '', name, flags=re.IGNORECASE)
        
        # Expand abbreviations
        for abbr, full in self.abbreviations.items():
            name = re.sub(abbr, full, name, flags=re.IGNORECASE)
        
        # Clean up whitespace
        name = ' '.join(name.split())
        
        return name.strip()
    
    def _search_wikidata(self, vi_name: str) -> Optional[str]:
        """
        Search Wikidata for English translation.
        
        Args:
            vi_name: Vietnamese name to search
            
        Returns:
            English name if found, None otherwise
        """
        try:
            # Wikidata search parameters
            params = {
                'action': 'wbsearchentities',
                'format': 'json',
                'language': 'vi',
                'search': vi_name,
                'limit': 5
            }
            
            # Rate limiting: max 1 request per second
            time.sleep(1)
            
            response = requests.get(self.wikidata_api, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.api_call_count += 1
            
            # Check if we have results
            if 'search' in data and len(data['search']) > 0:
                # Get the first result (most relevant)
                entity_id = data['search'][0]['id']
                
                # Fetch entity details to get English label
                entity_params = {
                    'action': 'wbgetentities',
                    'format': 'json',
                    'ids': entity_id,
                    'props': 'labels',
                    'languages': 'en'
                }
                
                time.sleep(1)
                entity_response = requests.get(self.wikidata_api, params=entity_params, timeout=10)
                entity_response.raise_for_status()
                
                entity_data = entity_response.json()
                
                # Extract English label
                if 'entities' in entity_data and entity_id in entity_data['entities']:
                    entity = entity_data['entities'][entity_id]
                    if 'labels' in entity and 'en' in entity['labels']:
                        return entity['labels']['en']['value']
            
            return None
            
        except Exception as e:
            print(f"  Wikidata search failed for '{vi_name}': {e}")
            return None
    
    def _pattern_based_translation(self, vi_name: str) -> Optional[str]:
        """
        Apply pattern-based translation rules.
        
        Args:
            vi_name: Vietnamese name
            
        Returns:
            English translation if pattern matches, None otherwise
        """
        for pattern, replacement in self.pattern_translations:
            match = re.match(pattern, vi_name, flags=re.IGNORECASE)
            if match:
                # Apply the translation pattern
                result = re.sub(pattern, replacement, vi_name, flags=re.IGNORECASE)
                # Remove Vietnamese accents from the remaining parts
                result = self._transliterate_vietnamese(result)
                return result
        
        return None
    
    def _transliterate_vietnamese(self, text: str) -> str:
        """
        Transliterate Vietnamese text to ASCII (remove accents).
        
        Args:
            text: Vietnamese text
            
        Returns:
            Text without accents
        """
        # Normalize and remove accents
        nfd = unicodedata.normalize('NFD', text)
        result = ''.join([c for c in nfd if not unicodedata.combining(c)])
        
        # Handle special Vietnamese characters
        replacements = {
            'đ': 'd', 'Đ': 'D',
            'ð': 'd', 'Ð': 'D'
        }
        
        for viet_char, eng_char in replacements.items():
            result = result.replace(viet_char, eng_char)
        
        return result
    
    def get_official_english_name(self, vi_name: str) -> Tuple[str, str]:
        """
        Get official English name for a Vietnamese POI name.
        
        Strategy:
        1. Check special cases dictionary
        2. Check cache
        3. Normalize Vietnamese name
        4. Search Wikidata API
        5. Apply pattern-based translation
        6. Fallback to transliteration
        
        Args:
            vi_name: Vietnamese name to translate
            
        Returns:
            Tuple of (english_name, source) where source is one of:
            'special', 'cache', 'wikidata', 'pattern', 'transliterate'
        """
        if not vi_name:
            return (vi_name, 'empty')
        
        original_name = vi_name.strip()
        
        # Strategy 1: Check special cases
        if original_name in self.special_cases:
            return (self.special_cases[original_name], 'special')
        
        # Strategy 2: Check cache
        if original_name in self.cache:
            self.cache_hit_count += 1
            return (self.cache[original_name], 'cache')
        
        # Strategy 3: Normalize name
        normalized_name = self._normalize_vietnamese_name(original_name)
        
        # Strategy 4: Search Wikidata
        wikidata_result = self._search_wikidata(normalized_name)
        if wikidata_result:
            # Cache the result
            self.cache[original_name] = wikidata_result
            self._save_cache()
            return (wikidata_result, 'wikidata')
        
        # Strategy 5: Pattern-based translation
        pattern_result = self._pattern_based_translation(normalized_name)
        if pattern_result:
            # Cache the result
            self.cache[original_name] = pattern_result
            self._save_cache()
            return (pattern_result, 'pattern')
        
        # Strategy 6: Fallback to transliteration
        transliterated = self._transliterate_vietnamese(normalized_name)
        self.cache[original_name] = transliterated
        self._save_cache()
        return (transliterated, 'transliterate')
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get translation statistics.
        
        Returns:
            Dictionary with stats
        """
        return {
            'cache_size': len(self.cache),
            'cache_hits': self.cache_hit_count,
            'api_calls': self.api_call_count,
            'cache_file': self.cache_file
        }


# Convenience function for quick usage
def translate_to_english(vi_name: str, translator: Optional[SmartTranslator] = None) -> str:
    """
    Quick translation function.
    
    Args:
        vi_name: Vietnamese name to translate
        translator: Existing translator instance (optional)
        
    Returns:
        English translation
    """
    if translator is None:
        translator = SmartTranslator()
    
    result, source = translator.get_official_english_name(vi_name)
    return result


# Test function
def test_translator():
    """Test the translator with sample names."""
    print("="*80)
    print("Smart Translator - Test Suite")
    print("="*80)
    
    translator = SmartTranslator()
    
    test_cases = [
        "Trường Đại học Kiểm sát Hà Nội",
        "Bệnh viện Bạch Mai",
        "UBND Phường Hoàn Kiếm",
        "Nhà văn hóa Tổ 5",
        "Tổ dân phố 12",
        "Trường THPT Chu Văn An",
        "Siêu thị Vinmart",
        "Chợ Đồng Xuân",
    ]
    
    for test_name in test_cases:
        english_name, source = translator.get_official_english_name(test_name)
        print(f"\n📍 Vietnamese: {test_name}")
        print(f"   English: {english_name}")
        print(f"   Source: {source}")
    
    print("\n" + "="*80)
    print("Translation Statistics:")
    stats = translator.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print("="*80)


if __name__ == "__main__":
    test_translator()
