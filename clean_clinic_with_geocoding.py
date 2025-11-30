"""
Clean and standardize RDF/Turtle file for Medical Clinics with Reverse Geocoding.
Fixes namespace issues, applies smart semantic translation, implements address fallback,
and uses reverse geocoding for entries without names or addresses.

Author: Python Data Engineer for Smart City
Date: 2025-11-30
"""

import os
import re
import time
import unicodedata
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, GEO
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClinicDataCleanerWithGeocoding:
    """Clean and translate clinic facility names with reverse geocoding support."""
    
    def __init__(self, input_file='datav2/data_hanoi_clinic.ttl', 
                 output_file='datav2/data_hanoi_clinic_cleaned.ttl'):
        """
        Initialize the clinic cleaner with geocoding.
        
        Args:
            input_file: Path to input TTL file
            output_file: Path to output TTL file
        """
        self.input_file = input_file
        self.output_file = output_file
        
        # Define namespaces with CORRECT URIs
        self.SCHEMA = Namespace("http://schema.org/")
        self.FIWARE = Namespace("https://smartdatamodels.org/dataModel.PointOfInterest/")
        self.EXT = Namespace("http://opendatafithou.org/def/extension/")
        self.GEO = Namespace("http://www.opengis.net/ont/geosparql#")
        self.XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
        
        # Initialize geocoder
        self.geolocator = Nominatim(user_agent="hanoi_smart_city_data_cleaner_v1.0")
        
        # Cache for geocoding results to avoid duplicate API calls
        self.geocoding_cache = {}
        
    def remove_vietnamese_accents(self, text):
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
    
    def capitalize_properly(self, text):
        """
        Capitalize words properly for English names.
        
        Args:
            text: Input text
            
        Returns:
            Properly capitalized text
        """
        # Words that should remain lowercase (unless at start)
        lowercase_words = {'and', 'of', 'the', 'in', 'at', 'for', 'on', 'to'}
        
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
    
    def parse_wkt_point(self, wkt_string):
        """
        Parse WKT POINT string to extract coordinates.
        
        Args:
            wkt_string: WKT string like "POINT(105.7837193 20.9851095)"
            
        Returns:
            Tuple of (longitude, latitude) or (None, None)
        """
        try:
            # Extract coordinates from POINT(lon lat)
            match = re.search(r'POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)', wkt_string, re.IGNORECASE)
            if match:
                lon = float(match.group(1))
                lat = float(match.group(2))
                return (lon, lat)
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse WKT: {wkt_string} - {e}")
        
        return (None, None)
    
    def get_street_name(self, wkt_string):
        """
        Get street name from coordinates using reverse geocoding.
        
        Args:
            wkt_string: WKT string with coordinates
            
        Returns:
            Street name or None if not found
        """
        # Parse coordinates
        lon, lat = self.parse_wkt_point(wkt_string)
        if lon is None or lat is None:
            return None
        
        # Check cache first
        cache_key = f"{lat:.6f},{lon:.6f}"
        if cache_key in self.geocoding_cache:
            logger.debug(f"Using cached geocoding result for {cache_key}")
            return self.geocoding_cache[cache_key]
        
        try:
            # Rate limiting - Nominatim requires 1 second between requests
            time.sleep(1.1)
            
            # Reverse geocode (lat, lon order for geopy)
            logger.debug(f"Geocoding coordinates: {lat}, {lon}")
            location = self.geolocator.reverse((lat, lon), language='vi', timeout=10)
            
            if location and location.raw.get('address'):
                address = location.raw['address']
                
                # Try to extract street name (priority order)
                street = None
                
                # Priority 1: road
                if 'road' in address:
                    street = address['road']
                # Priority 2: suburb/neighbourhood
                elif 'suburb' in address:
                    street = address['suburb']
                elif 'neighbourhood' in address:
                    street = address['neighbourhood']
                # Priority 3: city_district
                elif 'city_district' in address:
                    street = address['city_district']
                # Priority 4: town/village
                elif 'town' in address:
                    street = address['town']
                elif 'village' in address:
                    street = address['village']
                
                # Cache the result
                self.geocoding_cache[cache_key] = street
                
                if street:
                    logger.info(f"  Geocoded: ({lat}, {lon}) -> {street}")
                    return street
                else:
                    logger.warning(f"  No street found in geocoding result for ({lat}, {lon})")
                    self.geocoding_cache[cache_key] = None
                    return None
            else:
                logger.warning(f"  No geocoding result for ({lat}, {lon})")
                self.geocoding_cache[cache_key] = None
                return None
                
        except GeocoderTimedOut:
            logger.error(f"Geocoding timeout for ({lat}, {lon})")
            return None
        except GeocoderServiceError as e:
            logger.error(f"Geocoding service error for ({lat}, {lon}): {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during geocoding for ({lat}, {lon}): {e}")
            return None
    
    def translate_health_name(self, vi_name):
        """
        Apply smart translation using regex-based pattern matching.
        
        Args:
            vi_name: Vietnamese name (original or transliterated)
            
        Returns:
            Semantically translated English name
        """
        if not vi_name:
            return vi_name
        
        # Remove accents for pattern matching
        name_no_accent = self.remove_vietnamese_accents(vi_name)
        result = name_no_accent
        
        # Pattern 0a: "Phòng khám Đa khoa khu vực - Trạm y tế xã X" -> "X Commune Regional Health Station"
        match = re.match(r'^Phong\s+kham\s+[Dd]a\s+khoa\s+khu\s+vuc\s*-\s*Tram\s+y\s+te\s+xa\s+(.+)$', result, re.IGNORECASE)
        if match:
            place_name = match.group(1).strip()
            return self.capitalize_properly(f"{place_name} Commune Regional Health Station")
        
        # Pattern 0b: "Điểm Trạm Y tế X" -> "X Health Station"
        match = re.match(r'^Diem\s+Tram\s+[Yy]\s+[Tt]e\s+(.+)$', result, re.IGNORECASE)
        if match:
            place_name = match.group(1).strip()
            return self.capitalize_properly(f"{place_name} Health Station")
        
        # Pattern 0c: "Điểm Y tế X" -> "X Health Station"
        match = re.match(r'^Diem\s+[Yy]\s+[Tt]e\s+(.+)$', result, re.IGNORECASE)
        if match:
            place_name = match.group(1).strip()
            return self.capitalize_properly(f"{place_name} Health Station")
        
        # Pattern 1: "Trạm Y tế phường/xã X" -> "X Ward/Commune Health Station"
        match = re.match(r'^Tram\s+[Yy]\s+te\s+(phuong|xa)\s+(.+)$', result, re.IGNORECASE)
        if match:
            admin_type = match.group(1).lower()
            place_name = match.group(2).strip()
            admin_label = "Ward" if admin_type == "phuong" else "Commune"
            return self.capitalize_properly(f"{place_name} {admin_label} Health Station")
        
        # Pattern 2: "Trạm Y tế X" (without admin type) -> "X Health Station"
        match = re.match(r'^Tram\s+[Yy]\s+te\s+(.+)$', result, re.IGNORECASE)
        if match:
            place_name = match.group(1).strip()
            return self.capitalize_properly(f"{place_name} Health Station")
        
        # Pattern 3: "Trạm y tế X" (lowercase variant)
        match = re.match(r'^Tram\s+y\s+te\s+(.+)$', result, re.IGNORECASE)
        if match:
            place_name = match.group(1).strip()
            return self.capitalize_properly(f"{place_name} Health Station")
        
        # Pattern 4: "Phòng khám Đa khoa X" -> "X General Clinic"
        match = re.match(r'^Phong\s+kham\s+[Dd]a\s+khoa\s+(.+)$', result, re.IGNORECASE)
        if match:
            clinic_name = match.group(1).strip()
            return self.capitalize_properly(f"{clinic_name} General Clinic")
        
        # Pattern 5: "Phòng khám X" -> "X Clinic"
        match = re.match(r'^Phong\s+kham\s+(.+)$', result, re.IGNORECASE)
        if match:
            clinic_name = match.group(1).strip()
            return self.capitalize_properly(f"{clinic_name} Clinic")
        
        # Pattern 6: "Y tế học đường" -> "School Health Unit"
        if re.match(r'^Y\s+te\s+hoc\s+duong$', result, re.IGNORECASE):
            return "School Health Unit"
        
        # Pattern 7: "Dãy Nhà X" -> "Block X"
        match = re.match(r'^Day\s+Nha\s+(.+)$', result, re.IGNORECASE)
        if match:
            block_name = match.group(1).strip()
            return self.capitalize_properly(f"Block {block_name}")
        
        # Pattern 8: "Trung tâm Y tế X" -> "X Medical Center"
        match = re.match(r'^Trung\s+tam\s+[Yy]\s+te\s+(.+)$', result, re.IGNORECASE)
        if match:
            center_name = match.group(1).strip()
            return self.capitalize_properly(f"{center_name} Medical Center")
        
        # Pattern 9: Handle "Nha khoa" (Dental)
        if re.search(r'Nha\s+khoa', result, re.IGNORECASE):
            result_clean = re.sub(r'Nha\s+khoa\s*', '', result, flags=re.IGNORECASE).strip()
            if result_clean:
                return self.capitalize_properly(f"{result_clean} Dental Clinic")
            else:
                return "Dental Clinic"
        
        # Pattern 10: Administrative terms translation
        admin_replacements = {
            r'\bphuong\b': 'Ward',
            r'\bquan\b': 'District',
            r'\bthanh pho\b': 'City',
            r'\bhuyen\b': 'District',
            r'\bxa\b': 'Commune',
            r'\bthi tran\b': 'Town',
            r'\bkhu\s+vuc\b': 'Regional'
        }
        
        for pattern, replacement in admin_replacements.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and capitalize
        result = re.sub(r'\s+', ' ', result).strip()
        return self.capitalize_properly(result)
    
    def get_address_fallback_name(self, graph, subject):
        """
        Generate fallback name from address if available.
        
        Args:
            graph: RDF graph
            subject: Subject URI
            
        Returns:
            Tuple of (vietnamese_name, english_name) or (None, None)
        """
        # Try to get street address
        street = None
        district = None
        
        for obj in graph.objects(subject=subject, predicate=self.EXT.addr_street):
            if isinstance(obj, Literal):
                street = str(obj)
                break
        
        for obj in graph.objects(subject=subject, predicate=self.EXT.addr_district):
            if isinstance(obj, Literal):
                district = str(obj)
                break
        
        if street:
            vi_name = f"Phòng khám tại {street}"
            en_name_raw = f"Clinic at {self.remove_vietnamese_accents(street)}"
            en_name = self.capitalize_properly(en_name_raw)
            return (vi_name, en_name)
        elif district:
            vi_name = f"Phòng khám tại {district}"
            en_name_raw = f"Clinic at {self.remove_vietnamese_accents(district)}"
            en_name = self.capitalize_properly(en_name_raw)
            return (vi_name, en_name)
        
        return (None, None)
    
    def is_generic_name(self, name):
        """
        Check if a name is generic/placeholder.
        
        Args:
            name: Name to check
            
        Returns:
            True if generic, False otherwise
        """
        if not name:
            return True
        
        name_str = str(name).strip()
        
        # Check for generic patterns
        if name_str.lower() in ['unknown', 'clinic', 'n/a', '']:
            return True
        
        # Check for "Clinic #ID" pattern
        if re.match(r'^Clinic\s*#\d+$', name_str, re.IGNORECASE):
            return True
        
        # Check for "Phòng khám #ID" pattern
        if re.match(r'^Phong\s+kham\s*#\d+$', name_str, re.IGNORECASE):
            return True
        
        return False
    
    def process_clinic_file(self):
        """
        Process the clinic TTL file with all transformations including geocoding.
        
        Returns:
            Dictionary with processing statistics
        """
        if not os.path.exists(self.input_file):
            logger.error(f"Input file not found: {self.input_file}")
            return {'success': False, 'error': 'File not found'}
        
        try:
            logger.info("="*70)
            logger.info("Starting Clinic Data Cleaning with Reverse Geocoding")
            logger.info("="*70)
            logger.info(f"Input: {self.input_file}")
            logger.info(f"Output: {self.output_file}")
            
            # Load the graph
            logger.info("Loading RDF graph...")
            g = Graph()
            g.parse(self.input_file, format='turtle')
            
            # CRITICAL: Bind namespaces correctly
            logger.info("Fixing namespace bindings...")
            g.bind('schema', self.SCHEMA, override=True, replace=True)
            g.bind('fiware', self.FIWARE, override=True, replace=True)
            g.bind('ext', self.EXT, override=True, replace=True)
            g.bind('geo', self.GEO, override=True, replace=True)
            g.bind('xsd', self.XSD, override=True, replace=True)
            g.bind('rdf', RDF, override=True, replace=True)
            g.bind('rdfs', RDFS, override=True, replace=True)
            
            # Statistics
            stats = {
                'total_entities': 0,
                'translated': 0,
                'address_fallback': 0,
                'geocoded': 0,
                'unnamed_fallback': 0,
                'kept_original': 0,
                'errors': []
            }
            
            # Process each clinic entity
            logger.info("Processing clinic entities...")
            for subject in g.subjects(predicate=RDF.type, object=self.SCHEMA.MedicalClinic):
                stats['total_entities'] += 1
                
                # Get all names for this subject
                names = list(g.objects(subject=subject, predicate=self.SCHEMA.name))
                
                vi_name = None
                old_en_name = None
                
                # Find Vietnamese and English names
                for name in names:
                    if isinstance(name, Literal):
                        if name.language == 'vi':
                            vi_name = str(name)
                        elif name.language == 'en':
                            old_en_name = name
                
                # Determine if we need special handling
                needs_geocoding = False
                if old_en_name and self.is_generic_name(old_en_name):
                    needs_geocoding = True
                    logger.debug(f"Generic name detected: {old_en_name}")
                
                # Generate new English name
                new_en_name = None
                new_vi_name = None
                
                if needs_geocoding:
                    # Try address fallback first
                    fallback_vi, fallback_en = self.get_address_fallback_name(g, subject)
                    if fallback_en:
                        new_en_name = fallback_en
                        new_vi_name = fallback_vi
                        
                        # Update Vietnamese name (remove old generic name)
                        if vi_name:
                            g.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                        g.add((subject, self.SCHEMA.name, Literal(new_vi_name, lang='vi')))
                        
                        stats['address_fallback'] += 1
                        logger.debug(f"  Applied address fallback: {new_vi_name} / {new_en_name}")
                    else:
                        # Try reverse geocoding
                        logger.info(f"  Attempting reverse geocoding for {subject}")
                        
                        # Get geometry
                        wkt = None
                        for obj in g.objects(subject=subject, predicate=self.GEO.asWKT):
                            if isinstance(obj, Literal):
                                wkt = str(obj)
                                break
                        
                        if wkt:
                            street_name = self.get_street_name(wkt)
                            if street_name:
                                # Generate names from geocoded street
                                new_vi_name = f"Phòng khám tại {street_name}"
                                en_street = self.remove_vietnamese_accents(street_name)
                                new_en_name = self.capitalize_properly(f"Clinic at {en_street}")
                                
                                # Add the street to the graph for future use
                                g.add((subject, self.EXT.addr_street, Literal(street_name, lang='vi')))
                                
                                # Update Vietnamese name (remove old generic name)
                                if vi_name:
                                    g.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                                g.add((subject, self.SCHEMA.name, Literal(new_vi_name, lang='vi')))
                                
                                stats['geocoded'] += 1
                                logger.info(f"  ✓ Geocoded successfully: {new_vi_name} / {new_en_name}")
                            else:
                                # Geocoding failed - use generic fallback
                                new_vi_name = "Cơ sở y tế (Chưa cập nhật tên)"
                                new_en_name = "Medical Facility (Unnamed)"
                                
                                # Update Vietnamese name
                                if vi_name:
                                    g.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                                g.add((subject, self.SCHEMA.name, Literal(new_vi_name, lang='vi')))
                                
                                stats['unnamed_fallback'] += 1
                                logger.warning(f"  Geocoding failed, using unnamed fallback")
                        else:
                            # No geometry - use generic fallback
                            new_vi_name = "Cơ sở y tế (Chưa cập nhật tên)"
                            new_en_name = "Medical Facility (Unnamed)"
                            
                            # Update Vietnamese name
                            if vi_name:
                                g.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                            g.add((subject, self.SCHEMA.name, Literal(new_vi_name, lang='vi')))
                            
                            stats['unnamed_fallback'] += 1
                            logger.warning(f"  No geometry available, using unnamed fallback")
                    
                elif vi_name:
                    # Apply smart translation
                    new_en_name = self.translate_health_name(vi_name)
                    stats['translated'] += 1
                    logger.debug(f"  Translated: {vi_name} -> {new_en_name}")
                else:
                    # No Vietnamese name, keep original
                    if old_en_name:
                        new_en_name = str(old_en_name)
                    stats['kept_original'] += 1
                
                # Update the graph
                if new_en_name and old_en_name:
                    # Remove old English name
                    g.remove((subject, self.SCHEMA.name, old_en_name))
                    # Add new English name
                    g.add((subject, self.SCHEMA.name, Literal(new_en_name, lang='en')))
            
            # Save the cleaned graph
            logger.info("Saving cleaned data...")
            g.serialize(destination=self.output_file, format='turtle')
            
            logger.info("="*70)
            logger.info("Processing Complete!")
            logger.info("="*70)
            logger.info(f"Total entities processed: {stats['total_entities']}")
            logger.info(f"Smart translations: {stats['translated']}")
            logger.info(f"Address fallbacks: {stats['address_fallback']}")
            logger.info(f"Reverse geocoded: {stats['geocoded']}")
            logger.info(f"Unnamed fallbacks: {stats['unnamed_fallback']}")
            logger.info(f"Kept original: {stats['kept_original']}")
            logger.info(f"Geocoding cache size: {len(self.geocoding_cache)}")
            logger.info(f"Output saved to: {self.output_file}")
            logger.info("="*70)
            
            stats['success'] = True
            return stats
            
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            logger.error(error_msg)
            import traceback
            logger.error(traceback.format_exc())
            return {'success': False, 'error': error_msg}


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("CLINIC DATA CLEANER WITH REVERSE GEOCODING")
    print("Fixes: Namespaces, Smart Translation, Address Fallback, Geocoding")
    print("="*70 + "\n")
    
    print("⚠️  NOTE: This script uses Nominatim reverse geocoding.")
    print("   It respects rate limits (1 request per second).")
    print("   Processing may take several minutes for many entries.\n")
    
    cleaner = ClinicDataCleanerWithGeocoding()
    results = cleaner.process_clinic_file()
    
    if results['success']:
        print("\n✓ SUCCESS - Clinic data cleaned successfully!")
        print(f"\n📊 Statistics:")
        print(f"   - Total entities: {results.get('total_entities', 0)}")
        print(f"   - Smart translations: {results.get('translated', 0)}")
        print(f"   - Address fallbacks: {results.get('address_fallback', 0)}")
        print(f"   - Reverse geocoded: {results.get('geocoded', 0)}")
        print(f"   - Unnamed fallbacks: {results.get('unnamed_fallback', 0)}")
        print(f"   - Kept original: {results.get('kept_original', 0)}")
    else:
        print(f"\n✗ FAILED - {results.get('error', 'Unknown error')}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
