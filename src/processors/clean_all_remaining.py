"""
@File    : clean_all_remaining.py
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

import os
import re
import unicodedata
import time
import requests
from urllib.parse import quote
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, GEO
import logging
from typing import Tuple, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UniversalDataCleaner:
    """
    Universal cleaner for all remaining Hanoi POI data files.
    Implements smart category-based naming strategies.
    """
    
    # Category definitions
    MEDICAL_EMERGENCY = ['hospital', 'pharmacy', 'police', 'fire_station']
    EDUCATION = ['school', 'university', 'kindergarten', 'library']
    INFRASTRUCTURE = ['parking', 'public_toilet', 'waste_basket', 'warehouse', 
                     'fuel_station', 'charging_station', 'drinking_water']
    COMMUNITY_LEISURE = ['park', 'playground', 'community_centre']
    COMMERCE = ['restaurant', 'cafe', 'supermarket', 'convenience_store', 
               'marketplace', 'post_office']
    TRANSPORT = ['bus_stop']
    
    # Generic names for infrastructure (Logic B)
    GENERIC_NAMES = {
        # Infrastructure (Logic B)
        "parking": {"vi": "Bãi đỗ xe", "en": "Parking Lot"},
        "public_toilet": {"vi": "Nhà vệ sinh", "en": "Public Toilet"},
        "waste_basket": {"vi": "Thùng rác", "en": "Waste Basket"},
        "warehouse": {"vi": "Nhà kho", "en": "Warehouse"},
        "fuel_station": {"vi": "Trạm xăng", "en": "Gas Station"},
        "charging_station": {"vi": "Trạm sạc", "en": "Charging Station"},
        "drinking_water": {"vi": "Nguồn nước uống", "en": "Drinking Water"},
        "bus_stop": {"vi": "Trạm xe buýt", "en": "Bus Stop"},
        
        # Semantic (Logic A) - needed for location-based fallback
        "hospital": {"vi": "Bệnh viện", "en": "Hospital"},
        "pharmacy": {"vi": "Nhà thuốc", "en": "Pharmacy"},
        "clinic": {"vi": "Phòng khám", "en": "Clinic"},
        "police": {"vi": "Đồn công an", "en": "Police Station"},
        "fire_station": {"vi": "Trạm cứu hỏa", "en": "Fire Station"},
        "school": {"vi": "Trường học", "en": "School"},
        "university": {"vi": "Đại học", "en": "University"},
        "kindergarten": {"vi": "Trường mầm non", "en": "Kindergarten"},
        "library": {"vi": "Thư viện", "en": "Library"},
        "park": {"vi": "Công viên", "en": "Park"},
        "playground": {"vi": "Sân chơi", "en": "Playground"},
        "community_centre": {"vi": "Trung tâm cộng đồng", "en": "Community Centre"},
        "restaurant": {"vi": "Nhà hàng", "en": "Restaurant"},
        "cafe": {"vi": "Quán cà phê", "en": "Cafe"},
        "supermarket": {"vi": "Siêu thị", "en": "Supermarket"},
        "convenience_store": {"vi": "Cửa hàng tiện lợi", "en": "Convenience Store"},
        "marketplace": {"vi": "Chợ", "en": "Market"},
        "post_office": {"vi": "Bưu điện", "en": "Post Office"},
        "atm": {"vi": "Máy ATM", "en": "ATM"},
        "bank": {"vi": "Ngân hàng", "en": "Bank"},
    }
    
    # Translation dictionary for Logic A (Semantic Translation)
    SEMANTIC_TRANSLATIONS = {
        # Education
        r'\b(Truong\s+)?Tieu\s+hoc\b': 'Primary School',
        r'\bTiểu\s+học\b': 'Primary School',
        r'\b(THCS|Trung\s+hoc\s+co\s+so)\b': 'Secondary School',
        r'\bTrung\s+học\s+cơ\s+sở\b': 'Secondary School',
        r'\b(THPT|Trung\s+hoc\s+pho\s+thong)\b': 'High School',
        r'\bTrung\s+học\s+phổ\s+thông\b': 'High School',
        r'\b(Dai\s+hoc|Đại\s+học)\b': 'University',
        r'\bMam\s+non\b': 'Kindergarten',
        r'\bMầm\s+non\b': 'Kindergarten',
        r'\bNha\s+tre\b': 'Preschool',
        r'\bNhà\s+trẻ\b': 'Preschool',
        r'\bThu\s+vien\b': 'Library',
        r'\bThư\s+viện\b': 'Library',
        
        # Medical/Emergency
        r'\bBenh\s+vien\b': 'Hospital',
        r'\bBệnh\s+viện\b': 'Hospital',
        r'\b(Nha\s+thuoc|Quay\s+thuoc)\b': 'Pharmacy',
        r'\b(Nhà\s+thuốc|Quầy\s+thuốc)\b': 'Pharmacy',
        r'\b(Cong\s+an|Don\s+cong\s+an)\b': 'Police Station',
        r'\b(Công\s+an|Đồn\s+công\s+an)\b': 'Police Station',
        r'\b(Tram\s+cuu\s+hoa|PCCC)\b': 'Fire Station',
        r'\b(Trạm\s+cứu\s+hỏa)\b': 'Fire Station',
        r'\bPhong\s+kham\b': 'Clinic',
        r'\bPhòng\s+khám\b': 'Clinic',
        
        # Commercial
        r'\bSieu\s+thi\b': 'Supermarket',
        r'\bSiêu\s+thị\b': 'Supermarket',
        r'\bCho\b(?!\w)': 'Market',
        r'\bChợ\b': 'Market',
        r'\bNha\s+hang\b': 'Restaurant',
        r'\bNhà\s+hàng\b': 'Restaurant',
        r'\bQuan\s+(an|com)\b': 'Restaurant',
        r'\bQuán\s+(ăn|cơm)\b': 'Restaurant',
        r'\bCua\s+hang\b': 'Store',
        r'\bCửa\s+hàng\b': 'Store',
        r'\bBuu\s+dien\b': 'Post Office',
        r'\bBưu\s+điện\b': 'Post Office',
        r'\bCafe\b': 'Cafe',
        r'\bCà\s+phê\b': 'Cafe',
        
        # Community/Leisure
        r'\bCong\s+vien\b': 'Park',
        r'\bCông\s+viên\b': 'Park',
        r'\bSan\s+choi\b': 'Playground',
        r'\bSân\s+chơi\b': 'Playground',
        r'\bTrung\s+tam\s+cong\s+dong\b': 'Community Centre',
        r'\bTrung\s+tâm\s+cộng\s+đồng\b': 'Community Centre',
    }
    
    def __init__(self):
        """Initialize the universal cleaner."""
        # Define namespaces
        self.SCHEMA = Namespace("http://schema.org/")
        self.FIWARE = Namespace("https://smartdatamodels.org/dataModel.PointOfInterest/")
        self.EXT = Namespace("http://opendatafithou.org/def/extension/")
        self.GEO = Namespace("http://www.opengis.net/ont/geosparql#")
        self.XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
        
        # Reverse geocoding cache to avoid repeated API calls
        self.geocode_cache = {}
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """
        Get location name from coordinates using Nominatim reverse geocoding.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Location name (road, suburb, or district) or None if failed
        """
        # Create cache key (round to ~11m precision)
        cache_key = f"{round(lat, 4)}_{round(lon, 4)}"
        
        # Check cache first
        if cache_key in self.geocode_cache:
            return self.geocode_cache[cache_key]
        
        # Retry logic: up to 3 attempts
        for attempt in range(3):
            try:
                # Call Nominatim API
                url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=vi"
                headers = {
                    'User-Agent': 'OpenDataFitHou/1.0 (educational project)'
                }
                
                # Rate limiting: 1 request per second (1.5s on retries)
                time.sleep(1.5 if attempt > 0 else 1)
                
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract location name from response
                address = data.get('address', {})
                
                # Priority: road > suburb > district > city
                location_name = (
                    address.get('road') or
                    address.get('suburb') or
                    address.get('district') or
                    address.get('city') or
                    address.get('town') or
                    address.get('village')
                )
                
                # Cache the result
                self.geocode_cache[cache_key] = location_name
                
                return location_name
                
            except requests.exceptions.Timeout:
                if attempt < 2:
                    print(f"  ⚠ Timeout for ({lat}, {lon}), retrying ({attempt + 1}/3)...")
                    continue
                else:
                    print(f"  ⚠ Reverse geocoding failed after 3 attempts for ({lat}, {lon}): Timeout")
                    self.geocode_cache[cache_key] = None
                    return None
            except Exception as e:
                print(f"  ⚠ Reverse geocoding failed for ({lat}, {lon}): {e}")
                # Cache None to avoid retrying failed locations
                self.geocode_cache[cache_key] = None
                return None
        
        return None
    
    def remove_vietnamese_accents(self, text: str) -> str:
        """
        Remove Vietnamese accents from text.
        
        Args:
            text: Vietnamese text with accents
            
        Returns:
            Text without accents
        """
        if not text:
            return text
        
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
    
    def capitalize_properly(self, text: str) -> str:
        """
        Capitalize words properly for English names.
        
        Args:
            text: Input text
            
        Returns:
            Properly capitalized text
        """
        # Words that should remain lowercase (unless at start)
        lowercase_words = {'and', 'of', 'the', 'in', 'at', 'for', 'on', 'to', 'a', 'an'}
        
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            # First word is always capitalized
            if i == 0:
                result.append(word.capitalize())
            # Keep lowercase words lowercase (unless they're the first word)
            elif word.lower() in lowercase_words:
                result.append(word.lower())
            # Capitalize other words
            else:
                result.append(word.capitalize())
        
        return ' '.join(result)
    
    def apply_semantic_translation(self, vi_name: str, category: str) -> str:
        """
        Apply semantic translation using regex patterns (Logic A).
        
        Args:
            vi_name: Vietnamese name
            category: Category of the entity
            
        Returns:
            Translated English name
        """
        if not vi_name:
            return vi_name
        
        # Start with removing accents
        result = self.remove_vietnamese_accents(vi_name)
        
        # Apply all translation patterns
        for pattern, replacement in self.SEMANTIC_TRANSLATIONS.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result).strip()
        
        # Capitalize properly
        result = self.capitalize_properly(result)
        
        return result
    
    def get_location_based_name(self, graph: Graph, subject: URIRef, 
                                category: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate location-based name using address (Logic B).
        
        Args:
            graph: RDF graph
            subject: Subject URI
            category: Category of the entity
            
        Returns:
            Tuple of (vietnamese_name, english_name) or (None, None)
        """
        # Get generic names for this category
        if category not in self.GENERIC_NAMES:
            return (None, None)
        
        generic_vi = self.GENERIC_NAMES[category]["vi"]
        generic_en = self.GENERIC_NAMES[category]["en"]
        
        # Get address components
        street = None
        for obj in graph.objects(subject=subject, predicate=self.EXT.addr_street):
            if isinstance(obj, Literal):
                street = str(obj)
                break
        
        district = None
        for obj in graph.objects(subject=subject, predicate=self.EXT.addr_district):
            if isinstance(obj, Literal):
                district = str(obj)
                break
        
        city = None
        for obj in graph.objects(subject=subject, predicate=self.EXT.addr_city):
            if isinstance(obj, Literal):
                city = str(obj)
                break
        
        housenumber = None
        for obj in graph.objects(subject=subject, predicate=self.EXT.addr_housenumber):
            if isinstance(obj, Literal):
                housenumber = str(obj)
                break
        
        # Priority 1: Street with optional house number
        if street:
            if housenumber:
                vi_name = f"{generic_vi} {housenumber} {street}"
                street_no_accents = self.remove_vietnamese_accents(street)
                en_name = self.capitalize_properly(f"{generic_en} {housenumber} {street_no_accents}")
            else:
                vi_name = f"{generic_vi} tại {street}"
                street_no_accents = self.remove_vietnamese_accents(street)
                en_name = self.capitalize_properly(f"{generic_en} at {street_no_accents}")
            return (vi_name, en_name)
        
        # Priority 2: House number only (without street)
        if housenumber:
            vi_name = f"{generic_vi} số {housenumber}"
            en_name = f"{generic_en} No. {housenumber}"
            logging.debug(f"Generated house number name: {vi_name} / {en_name}")
            return (vi_name, en_name)
        
        # Priority 3: District
        if district:
            vi_name = f"{generic_vi} tại {district}"
            district_no_accents = self.remove_vietnamese_accents(district)
            en_name = self.capitalize_properly(f"{generic_en} at {district_no_accents}")
            return (vi_name, en_name)
        
        # Priority 4: City
        if city:
            vi_name = f"{generic_vi} tại {city}"
            city_no_accents = self.remove_vietnamese_accents(city)
            en_name = self.capitalize_properly(f"{generic_en} at {city_no_accents}")
            return (vi_name, en_name)
        
        # Priority 5: Use reverse geocoding from coordinates (instead of ID)
        # Get WKT geometry to extract coordinates
        coords_text = None
        for obj in graph.objects(subject=subject, predicate=self.GEO.asWKT):
            if isinstance(obj, Literal):
                coords_text = str(obj)
                break
        
        if coords_text:
            # Extract lat/lon from "POINT(lon lat)"
            match = re.search(r'POINT\(([\d.]+)\s+([\d.]+)\)', coords_text)
            if match:
                lon = float(match.group(1))
                lat = float(match.group(2))
                
                # Try to get location name from coordinates using Nominatim
                location_name = self.reverse_geocode(lat, lon)
                
                if location_name:
                    vi_name = f"{generic_vi} tại {location_name}"
                    location_no_accents = self.remove_vietnamese_accents(location_name)
                    en_name = self.capitalize_properly(f"{generic_en} at {location_no_accents}")
                    return (vi_name, en_name)
        
        # Absolute last resort: Use ID from URI (if no coordinates available)
        uri_str = str(subject)
        match = re.search(r':(\d+)>?$', uri_str)
        if match:
            entity_id = match.group(1)
            vi_name = f"{generic_vi} #{entity_id}"
            en_name = f"{generic_en} #{entity_id}"
            return (vi_name, en_name)
        
        return (None, None)
    
    def is_generic_or_unknown(self, name: str) -> bool:
        """
        Check if a name is generic/placeholder/unknown.
        
        Args:
            name: Name to check
            
        Returns:
            True if generic, False otherwise
        """
        if not name:
            return True
        
        name_str = str(name).strip().lower()
        
        # Check for empty or whitespace-only
        if not name_str:
            return True
        
        # Check for specific generic words
        generic_words = ['unknown', 'n/a', 'unnamed']
        if name_str in generic_words:
            return True
        
        # Check for ID-based pattern "Type #123"
        id_pattern = r'^[\w\s]+\s*#\d+$'
        if re.match(id_pattern, name_str):
            return True
        
        return False
    
    def determine_category(self, filename: str) -> str:
        """
        Determine which category a file belongs to.
        
        Args:
            filename: Name of the file
            
        Returns:
            Category name
        """
        # Extract category from filename (e.g., data_hanoi_school.ttl -> school)
        match = re.search(r'data_hanoi_(\w+)\.ttl', filename)
        if match:
            return match.group(1)
        return 'unknown'
    
    def get_naming_strategy(self, category: str) -> str:
        """
        Determine which naming strategy to use for a category.
        
        Args:
            category: Category name
            
        Returns:
            'semantic' for Logic A, 'location' for Logic B
        """
        if category in self.MEDICAL_EMERGENCY:
            return 'semantic'
        elif category in self.EDUCATION:
            return 'semantic'
        elif category in self.COMMERCE:
            return 'semantic'
        elif category in self.COMMUNITY_LEISURE:
            return 'semantic'
        elif category in self.INFRASTRUCTURE:
            return 'location'
        elif category in self.TRANSPORT:
            return 'location'
        else:
            return 'semantic'  # Default to semantic
    
    def fix_invalid_uris(self, graph: Graph) -> int:
        """
        Fix invalid URIs in the graph (e.g., Wikipedia links with spaces).
        
        Args:
            graph: RDF graph
            
        Returns:
            Number of URIs fixed
        """
        fixed_count = 0
        
        # Find all Wikipedia URIs that need fixing
        for s, p, o in list(graph):
            if isinstance(o, URIRef):
                uri_str = str(o)
                # Check if it's a Wikipedia URI with spaces or special characters
                if 'wikipedia.org/wiki/' in uri_str and (' ' in uri_str or 'Đ' in uri_str or 'ả' in uri_str or 'ô' in uri_str):
                    # Split into base and path
                    if '/wiki/' in uri_str:
                        base, path = uri_str.rsplit('/wiki/', 1)
                        # URL encode the path part only
                        encoded_path = quote(path, safe='')
                        new_uri = f"{base}/wiki/{encoded_path}"
                        new_uri_ref = URIRef(new_uri)
                        
                        # Replace in graph
                        graph.remove((s, p, o))
                        graph.add((s, p, new_uri_ref))
                        fixed_count += 1
        
        return fixed_count
    
    def process_entity(self, graph: Graph, subject: URIRef, category: str) -> Dict[str, any]:
        """
        Process a single entity with category-specific logic.
        
        Args:
            graph: RDF graph
            subject: Subject URI
            category: Category of the entity
            
        Returns:
            Dictionary with processing stats
        """
        stats = {
            'processed': False,
            'had_name': False,
            'used_semantic': False,
            'used_location': False,
            'unchanged': False
        }
        
        # Get naming strategy for this category
        strategy = self.get_naming_strategy(category)
        
        # Get existing Vietnamese name
        vi_name = None
        en_name = None
        
        for obj in graph.objects(subject=subject, predicate=self.SCHEMA.name):
            if isinstance(obj, Literal):
                if obj.language == 'vi':
                    vi_name = str(obj)
                elif obj.language == 'en':
                    en_name = str(obj)
        
        # Determine if we need to process
        needs_processing = False
        
        if strategy == 'semantic':
            # Logic A: Semantic Translation with Location Fallback
            # Preserve meaningful names, improve translations, use location when available
            
            vi_is_good = vi_name and not self.is_generic_or_unknown(vi_name)
            en_is_good = en_name and not self.is_generic_or_unknown(en_name)
            
            if vi_is_good:
                # Good Vietnamese name exists, try to improve English translation
                stats['had_name'] = True
                new_en_name = self.apply_semantic_translation(vi_name, category)
                
                # Update English name if translation improved it
                if new_en_name and new_en_name != en_name and not self.is_generic_or_unknown(new_en_name):
                    if en_name:
                        graph.remove((subject, self.SCHEMA.name, Literal(en_name, lang='en')))
                    graph.add((subject, self.SCHEMA.name, Literal(new_en_name, lang='en')))
                    stats['processed'] = True
                    stats['used_semantic'] = True
                else:
                    stats['unchanged'] = True
            else:
                # Vietnamese name is generic/missing, try location-based improvement
                logging.debug(f"Vietnamese name is generic/missing, trying location-based for: {subject}")
                vi_fallback, en_fallback = self.get_location_based_name(graph, subject, category)
                logging.debug(f"Location-based result: {vi_fallback} / {en_fallback}")
                
                if vi_fallback and en_fallback:
                    # Check if generated names are better than what we have
                    new_vi_is_generic = self.is_generic_or_unknown(vi_fallback)
                    new_en_is_generic = self.is_generic_or_unknown(en_fallback)
                    
                    # Only replace if new names are ACTUALLY better (not just different IDs)
                    # Compare: if old is "Cafe #123" and new is "Cafe #123", don't replace
                    # But if old is "Cafe #123" and new is "Cafe tại District", DO replace
                    should_replace = False
                    
                    if not new_vi_is_generic and not new_en_is_generic:
                        # Both new names are location-based (good), replace them
                        should_replace = True
                    elif (not new_vi_is_generic or not new_en_is_generic):
                        # At least one new name is better, check if it's different from current
                        if vi_fallback != vi_name or en_fallback != en_name:
                            should_replace = True
                    
                    if should_replace:
                        # Remove old names
                        if vi_name:
                            graph.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                        if en_name:
                            graph.remove((subject, self.SCHEMA.name, Literal(en_name, lang='en')))
                        # Add new names
                        graph.add((subject, self.SCHEMA.name, Literal(vi_fallback, lang='vi')))
                        graph.add((subject, self.SCHEMA.name, Literal(en_fallback, lang='en')))
                        stats['processed'] = True
                        stats['used_location'] = True
                    else:
                        # Keep existing names as they are (even if ID-based, no better option)
                        stats['unchanged'] = True
                else:
                    # No location fallback available, keep existing
                    stats['unchanged'] = True
        
        elif strategy == 'location':
            # Logic B: Location-Based Fallback for Infrastructure
            # Strategy: Only generate location-based names for entities that lack meaningful names
            # Preserve all existing meaningful names from source data
            
            # Check if existing names are meaningful
            vi_is_good = vi_name and not self.is_generic_or_unknown(vi_name)
            en_is_good = en_name and not self.is_generic_or_unknown(en_name)
            
            # If BOTH names are already good, keep them
            if vi_is_good and en_is_good:
                stats['unchanged'] = True
            else:
                # At least one name is missing or generic, try to improve
                vi_fallback, en_fallback = self.get_location_based_name(graph, subject, category)
                
                if vi_fallback and en_fallback:
                    # Check if generated names are better than what we have
                    new_vi_is_generic = self.is_generic_or_unknown(vi_fallback)
                    new_en_is_generic = self.is_generic_or_unknown(en_fallback)
                    
                    should_replace_vi = False
                    should_replace_en = False
                    
                    # Replace VI name only if:
                    # - Current VI is bad AND (new VI is good OR current is empty/generic)
                    if not vi_is_good:
                        if not new_vi_is_generic or not vi_name:
                            should_replace_vi = True
                    
                    # Replace EN name only if:
                    # - Current EN is bad AND (new EN is good OR current is empty/generic)
                    if not en_is_good:
                        if not new_en_is_generic or not en_name:
                            should_replace_en = True
                    
                    # Apply replacements
                    if should_replace_vi:
                        if vi_name:
                            graph.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                        graph.add((subject, self.SCHEMA.name, Literal(vi_fallback, lang='vi')))
                        stats['processed'] = True
                        stats['used_location'] = True
                    
                    if should_replace_en:
                        if en_name:
                            graph.remove((subject, self.SCHEMA.name, Literal(en_name, lang='en')))
                        graph.add((subject, self.SCHEMA.name, Literal(en_fallback, lang='en')))
                        stats['processed'] = True
                        stats['used_location'] = True
                    
                    if not should_replace_vi and not should_replace_en:
                        stats['unchanged'] = True
                else:
                    # Could not generate fallback names, keep existing
                    stats['unchanged'] = True
        
        return stats
    
    def process_file(self, input_file: str, output_file: str) -> Dict[str, any]:
        """
        Process a single TTL file.
        
        Args:
            input_file: Path to input TTL file
            output_file: Path to output TTL file
            
        Returns:
            Dictionary with processing statistics
        """
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return {'success': False, 'error': 'File not found'}
        
        try:
            # Determine category
            category = self.determine_category(os.path.basename(input_file))
            strategy = self.get_naming_strategy(category)
            
            logger.info("="*70)
            logger.info(f"Processing: {os.path.basename(input_file)}")
            logger.info(f"Category: {category}")
            logger.info(f"Strategy: {strategy.upper()}")
            logger.info("="*70)
            
            # Load the graph
            logger.info("Loading RDF graph...")
            g = Graph()
            g.parse(input_file, format='turtle')
            
            # Fix namespace bindings
            logger.info("Fixing namespace bindings...")
            g.bind('schema', self.SCHEMA, override=True, replace=True)
            g.bind('fiware', self.FIWARE, override=True, replace=True)
            g.bind('ext', self.EXT, override=True, replace=True)
            g.bind('geo', self.GEO, override=True, replace=True)
            g.bind('xsd', self.XSD, override=True, replace=True)
            
            # Fix invalid URIs (e.g., Wikipedia links with spaces)
            logger.info("Fixing invalid URIs...")
            fixed_uris = self.fix_invalid_uris(g)
            if fixed_uris > 0:
                logger.info(f"  Fixed {fixed_uris} invalid URIs")
            
            # Get all entities
            entities = list(g.subjects(predicate=RDF.type, 
                                      object=self.FIWARE.PointOfInterest))
            
            logger.info(f"Found {len(entities)} entities to process")
            
            # Process statistics
            total_processed = 0
            total_unchanged = 0
            total_semantic = 0
            total_location = 0
            
            # Process each entity
            for i, subject in enumerate(entities, 1):
                if i % 100 == 0:
                    logger.info(f"  Processing entity {i}/{len(entities)}...")
                
                stats = self.process_entity(g, subject, category)
                
                if stats['processed']:
                    total_processed += 1
                    if stats['used_semantic']:
                        total_semantic += 1
                    if stats['used_location']:
                        total_location += 1
                elif stats['unchanged']:
                    total_unchanged += 1
            
            # Create output directory if needed
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Serialize with proper formatting
            logger.info(f"Saving cleaned data to: {output_file}")
            g.serialize(destination=output_file, format='turtle')
            
            logger.info("")
            logger.info("Processing Summary:")
            logger.info(f"  Total entities: {len(entities)}")
            logger.info(f"  Processed: {total_processed}")
            logger.info(f"    - Semantic translations: {total_semantic}")
            logger.info(f"    - Location-based names: {total_location}")
            logger.info(f"  Unchanged: {total_unchanged}")
            logger.info(f"✓ Successfully saved to: {output_file}")
            
            return {
                'success': True,
                'total': len(entities),
                'processed': total_processed,
                'semantic': total_semantic,
                'location': total_location,
                'unchanged': total_unchanged,
                'category': category,
                'strategy': strategy
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def process_all_files(self, input_dir: str = 'datav2', 
                         output_dir: str = 'datav2/cleaned') -> Dict[str, any]:
        """
        Process all remaining files in the directory.
        
        Args:
            input_dir: Directory containing input TTL files
            output_dir: Directory for output TTL files
            
        Returns:
            Dictionary with overall statistics
        """
        # Files to process (ALL 28 categories including atm, bank, clinic)
        categories_to_process = (
            ['atm', 'bank', 'clinic'] +
            self.MEDICAL_EMERGENCY +
            self.EDUCATION +
            self.INFRASTRUCTURE +
            self.COMMUNITY_LEISURE +
            self.COMMERCE +
            self.TRANSPORT
        )
        
        logger.info("="*70)
        logger.info("MASTER CLEANING PROCESS - ALL REMAINING FILES")
        logger.info("="*70)
        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Categories to process: {len(categories_to_process)}")
        logger.info("")
        
        overall_stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'results': []
        }
        
        # Process each category
        for category in categories_to_process:
            input_file = os.path.join(input_dir, f'data_hanoi_{category}.ttl')
            output_file = os.path.join(output_dir, f'data_hanoi_{category}_cleaned.ttl')
            
            # Check if file exists
            if not os.path.exists(input_file):
                logger.warning(f"File not found, skipping: {input_file}")
                continue
            
            overall_stats['total_files'] += 1
            
            # Process the file
            result = self.process_file(input_file, output_file)
            
            if result.get('success'):
                overall_stats['successful'] += 1
            else:
                overall_stats['failed'] += 1
            
            overall_stats['results'].append({
                'category': category,
                'input': input_file,
                'output': output_file,
                'result': result
            })
            
            logger.info("")
        
        # Print overall summary
        logger.info("="*70)
        logger.info("OVERALL SUMMARY")
        logger.info("="*70)
        logger.info(f"Total files processed: {overall_stats['total_files']}")
        logger.info(f"Successful: {overall_stats['successful']}")
        logger.info(f"Failed: {overall_stats['failed']}")
        logger.info("")
        
        # Print detailed results by strategy
        logger.info("Results by Strategy:")
        semantic_files = [r for r in overall_stats['results'] 
                         if r['result'].get('strategy') == 'semantic']
        location_files = [r for r in overall_stats['results'] 
                         if r['result'].get('strategy') == 'location']
        
        logger.info(f"  Semantic Translation (Logic A): {len(semantic_files)} files")
        for r in semantic_files:
            if r['result'].get('success'):
                logger.info(f"    ✓ {r['category']}: {r['result'].get('processed', 0)} entities")
        
        logger.info(f"  Location-Based (Logic B): {len(location_files)} files")
        for r in location_files:
            if r['result'].get('success'):
                logger.info(f"    ✓ {r['category']}: {r['result'].get('processed', 0)} entities")
        
        logger.info("="*70)
        logger.info("✓ Master cleaning process completed!")
        logger.info("="*70)
        
        return overall_stats


def main():
    """Main entry point."""
    cleaner = UniversalDataCleaner()
    
    # Process all files
    results = cleaner.process_all_files(
        input_dir='datav2',
        output_dir='datav2/cleaned'
    )
    
    # Exit with appropriate code
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()
