"""
Clean and standardize RDF/Turtle file for Medical Clinics.
Fixes namespace issues, applies smart semantic translation, and implements address fallback.

Author: Semantic Web & NLP Engineering Team
Date: 2025-11-30
"""

import os
import re
import unicodedata
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, GEO
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClinicDataCleaner:
    """Clean and translate clinic facility names in RDF/Turtle files."""
    
    def __init__(self, input_file='datav2/data_hanoi_clinic.ttl', 
                 output_file='datav2/data_hanoi_clinic_cleaned.ttl'):
        """
        Initialize the clinic cleaner.
        
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
        
        # Pattern 0b: "Điểm Trạm Y tế X" -> "X Health Station Point"
        match = re.match(r'^Diem\s+Tram\s+[Yy]\s+[Tt]e\s+(.+)$', result, re.IGNORECASE)
        if match:
            place_name = match.group(1).strip()
            return self.capitalize_properly(f"{place_name} Health Station")
        
        # Pattern 1: "Trạm Y tế phường/xã X" -> "X Ward/Commune Health Station"
        # Handles: "Tram Y te phuong Mo Lao" -> "Mo Lao Ward Health Station"
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
        
        # Pattern 8: Handle "Nha khoa" (Dental)
        if re.search(r'Nha\s+khoa', result, re.IGNORECASE):
            # Extract the rest of the name
            result_clean = re.sub(r'Nha\s+khoa\s*', '', result, flags=re.IGNORECASE).strip()
            if result_clean:
                return self.capitalize_properly(f"{result_clean} Dental Clinic")
            else:
                return "Dental Clinic"
        
        # Pattern 9: Administrative terms translation
        admin_replacements = {
            r'\bphuong\b': 'Ward',
            r'\bquan\b': 'District',
            r'\bthanh pho\b': 'City',
            r'\bhuyen\b': 'District',
            r'\bxa\b': 'Commune',
            r'\bthi xa\b': 'Town',
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
        Process the clinic TTL file with all transformations.
        
        Returns:
            Dictionary with processing statistics
        """
        if not os.path.exists(self.input_file):
            logger.error(f"Input file not found: {self.input_file}")
            return {'success': False, 'error': 'File not found'}
        
        try:
            logger.info("="*70)
            logger.info("Starting Clinic Data Cleaning")
            logger.info("="*70)
            logger.info(f"Input: {self.input_file}")
            logger.info(f"Output: {self.output_file}")
            
            # Load the graph
            logger.info("Loading RDF graph...")
            g = Graph()
            g.parse(self.input_file, format='turtle')
            
            # CRITICAL: Remove wrong namespace bindings and rebind correctly
            logger.info("Fixing namespace bindings...")
            # Remove any existing schema bindings
            for prefix, ns in list(g.namespaces()):
                if str(ns) == "http://schema.org/":
                    g.namespace_manager.bind(prefix, ns, override=False, replace=True)
            
            # Force rebind with correct prefixes (override=True, replace=True)
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
                
                # Determine if we need address fallback
                needs_fallback = False
                if old_en_name and self.is_generic_name(old_en_name):
                    needs_fallback = True
                    logger.debug(f"Generic name detected: {old_en_name}")
                
                # Generate new English name
                new_en_name = None
                
                if needs_fallback:
                    # Try address fallback
                    fallback_vi, fallback_en = self.get_address_fallback_name(g, subject)
                    if fallback_en:
                        new_en_name = fallback_en
                        # Also update Vietnamese name if it was generic
                        if vi_name and self.is_generic_name(vi_name):
                            # Remove old Vietnamese name
                            g.remove((subject, self.SCHEMA.name, Literal(vi_name, lang='vi')))
                            # Add new Vietnamese name
                            g.add((subject, self.SCHEMA.name, Literal(fallback_vi, lang='vi')))
                            vi_name = fallback_vi
                        stats['address_fallback'] += 1
                        logger.debug(f"  Applied address fallback: {new_en_name}")
                    else:
                        # Keep the generic name as last resort
                        new_en_name = str(old_en_name)
                        stats['kept_original'] += 1
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
            logger.info(f"Kept original: {stats['kept_original']}")
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
    print("CLINIC DATA CLEANER")
    print("Fixes: Namespaces, Smart Translation, Address Fallback")
    print("="*70 + "\n")
    
    cleaner = ClinicDataCleaner()
    results = cleaner.process_clinic_file()
    
    if results['success']:
        print("\n✓ SUCCESS - Clinic data cleaned successfully!")
        print(f"\n📊 Statistics:")
        print(f"   - Total entities: {results.get('total_entities', 0)}")
        print(f"   - Smart translations: {results.get('translated', 0)}")
        print(f"   - Address fallbacks: {results.get('address_fallback', 0)}")
        print(f"   - Kept original: {results.get('kept_original', 0)}")
    else:
        print(f"\n✗ FAILED - {results.get('error', 'Unknown error')}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
