"""
Second-pass cleaning script: Improve translations using Wikidata and smart patterns
Author: Data Scientist - Entity Resolution Specialist
Date: 2025-11-30

This script reads cleaned files from datav2/cleaned/, applies smart translation
using Wikidata API, and saves improved versions to datav2/cleanedv2/.
"""

import os
import logging
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from smart_translate_lookup import SmartTranslator
from typing import Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SecondPassCleaner:
    """
    Second-pass cleaner to improve translations using Wikidata.
    """
    
    def __init__(self):
        """Initialize the second-pass cleaner."""
        # Initialize smart translator
        self.translator = SmartTranslator(cache_file="translation_cache.json")
        
        # Define namespaces
        self.SCHEMA = Namespace("http://schema.org/")
        self.FIWARE = Namespace("https://smartdatamodels.org/dataModel.PointOfInterest/")
        self.EXT = Namespace("http://opendatafithou.org/def/extension/")
        self.GEO = Namespace("http://www.opengis.net/ont/geosparql#")
        self.XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'total_entities': 0,
            'translations_improved': 0,
            'translations_unchanged': 0,
            'by_source': {
                'wikidata': 0,
                'pattern': 0,
                'transliterate': 0,
                'special': 0,
                'cache': 0
            }
        }
    
    def improve_entity_name(self, graph: Graph, subject: URIRef) -> bool:
        """
        Improve the English name of an entity using smart translation.
        
        Args:
            graph: RDF graph
            subject: Entity URI
            
        Returns:
            True if translation was improved, False otherwise
        """
        # Get current names
        vi_name = None
        en_name = None
        
        for obj in graph.objects(subject, self.SCHEMA.name):
            if isinstance(obj, Literal):
                if obj.language == 'vi':
                    vi_name = str(obj)
                elif obj.language == 'en':
                    en_name = str(obj)
        
        # If no Vietnamese name, skip
        if not vi_name:
            return False
        
        # Get improved English translation
        new_en_name, source = self.translator.get_official_english_name(vi_name)
        
        # Check if translation improved
        if new_en_name and new_en_name != en_name:
            # Remove old English name
            if en_name:
                graph.remove((subject, self.SCHEMA.name, Literal(en_name, lang='en')))
            
            # Add improved English name
            graph.add((subject, self.SCHEMA.name, Literal(new_en_name, lang='en')))
            
            # Update statistics
            self.stats['translations_improved'] += 1
            self.stats['by_source'][source] += 1
            
            logger.info(f"  ✓ Improved: '{vi_name}' → '{new_en_name}' (source: {source})")
            return True
        else:
            self.stats['translations_unchanged'] += 1
            return False
    
    def process_file(self, input_file: str, output_file: str) -> Dict:
        """
        Process a single TTL file to improve translations.
        
        Args:
            input_file: Input TTL file path
            output_file: Output TTL file path
            
        Returns:
            Processing statistics
        """
        logger.info("="*70)
        logger.info(f"Processing: {os.path.basename(input_file)}")
        logger.info("="*70)
        
        try:
            # Load RDF graph
            logger.info("Loading RDF graph...")
            g = Graph()
            g.parse(input_file, format='turtle')
            
            # Bind namespaces
            g.bind('schema', self.SCHEMA)
            g.bind('fiware', self.FIWARE)
            g.bind('ext', self.EXT)
            g.bind('geo', self.GEO)
            
            # Find all entities (subjects with schema:name)
            entities = set(g.subjects(self.SCHEMA.name, None))
            entity_count = len(entities)
            logger.info(f"Found {entity_count} entities to process")
            
            self.stats['total_entities'] += entity_count
            
            # Process each entity
            improved_count = 0
            for idx, subject in enumerate(entities, 1):
                if idx % 50 == 0:
                    logger.info(f"  Processing entity {idx}/{entity_count}...")
                
                if self.improve_entity_name(g, subject):
                    improved_count += 1
            
            # Save improved graph
            logger.info(f"Saving improved data to: {output_file}")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            g.serialize(destination=output_file, format='turtle')
            
            # Summary
            logger.info("")
            logger.info("Processing Summary:")
            logger.info(f"  Total entities: {entity_count}")
            logger.info(f"  Translations improved: {improved_count}")
            logger.info(f"  Translations unchanged: {entity_count - improved_count}")
            logger.info(f"✓ Successfully saved to: {output_file}")
            
            return {
                'success': True,
                'entities': entity_count,
                'improved': improved_count,
                'unchanged': entity_count - improved_count
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def process_all_files(self, input_dir: str = 'datav2/cleaned',
                         output_dir: str = 'datav2/cleanedv2') -> Dict:
        """
        Process all TTL files in the cleaned directory.
        
        Args:
            input_dir: Input directory with cleaned files
            output_dir: Output directory for improved files
            
        Returns:
            Overall statistics
        """
        logger.info("="*70)
        logger.info("SECOND-PASS CLEANING - SMART TRANSLATION")
        logger.info("="*70)
        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")
        logger.info("")
        
        # Get all TTL files
        input_files = [f for f in os.listdir(input_dir) if f.endswith('_cleaned.ttl')]
        self.stats['total_files'] = len(input_files)
        
        logger.info(f"Found {len(input_files)} files to process")
        logger.info("")
        
        # Process each file
        for input_filename in sorted(input_files):
            input_path = os.path.join(input_dir, input_filename)
            output_filename = input_filename.replace('_cleaned.ttl', '_cleanedv2.ttl')
            output_path = os.path.join(output_dir, output_filename)
            
            result = self.process_file(input_path, output_path)
            logger.info("")
        
        # Print overall summary
        logger.info("="*70)
        logger.info("OVERALL SUMMARY")
        logger.info("="*70)
        logger.info(f"Total files processed: {self.stats['total_files']}")
        logger.info(f"Total entities: {self.stats['total_entities']}")
        logger.info(f"Translations improved: {self.stats['translations_improved']}")
        logger.info(f"Translations unchanged: {self.stats['translations_unchanged']}")
        logger.info("")
        logger.info("Improvements by source:")
        for source, count in self.stats['by_source'].items():
            if count > 0:
                logger.info(f"  {source}: {count}")
        logger.info("")
        
        # Translation statistics
        translator_stats = self.translator.get_stats()
        logger.info("Translation engine statistics:")
        logger.info(f"  Cache size: {translator_stats['cache_size']} entries")
        logger.info(f"  Cache hits: {translator_stats['cache_hits']}")
        logger.info(f"  Wikidata API calls: {translator_stats['api_calls']}")
        logger.info(f"  Cache file: {translator_stats['cache_file']}")
        logger.info("="*70)
        
        return self.stats


def main():
    """Main execution function."""
    cleaner = SecondPassCleaner()
    results = cleaner.process_all_files(
        input_dir='datav2/cleaned',
        output_dir='datav2/cleanedv2'
    )


if __name__ == "__main__":
    main()
