"""
Batch processor for fetching all OSM amenity types
Clean orchestrator - delegates all data fetching and file writing to osm_data_fetcher.py
Handles only progress tracking, error handling, and batch coordination
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# CRITICAL: Import the centralized processing function
# This is the ONLY function that should handle data fetching and writing
from osm_data_fetcher import process_amenity_data
from config_amenity_types import AMENITY_TYPES, BATCH_CONFIG


class BatchProcessor:
    """
    Clean batch orchestrator for OSM data processing
    
    Responsibilities:
    - Progress tracking (completed/failed categories)
    - Error handling and logging
    - Batch coordination and timing
    - Summary reporting
    
    NOT Responsible For:
    - Data fetching (delegated to osm_data_fetcher.fetch_osm_data)
    - Data enrichment (delegated to osm_data_fetcher.enrich_with_wikidata)
    - File writing (delegated to osm_data_fetcher.write_turtle_file)
    """
    
    def __init__(self, output_dir: str = "datav2"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.progress_file = self.output_dir / "processing_progress.json"
        self.error_log_file = self.output_dir / "processing_errors.log"
        self.summary_file = self.output_dir / "processing_summary.json"
        
        self.progress = self._load_progress()
        self.summary = {
            'start_time': datetime.now().isoformat(),
            'total_categories': len(AMENITY_TYPES),
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
        
        print(f"[BatchProcessor] Initialized with output directory: {self.output_dir.absolute()}")
        print(f"[BatchProcessor] Progress will be saved to: {self.progress_file}")
    
    def _load_progress(self) -> Dict[str, Any]:
        """Load processing progress from file"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load progress file: {e}")
        
        return {'completed': [], 'failed': [], 'last_processed': None}
    
    def _save_progress(self):
        """Save current progress to file"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")
    
    def _log_error(self, category_name: str, error: str):
        """Log error to file"""
        try:
            with open(self.error_log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] {category_name}: {error}\n")
        except Exception as e:
            print(f"Warning: Could not write to error log: {e}")
    
    def _save_summary(self):
        """Save processing summary"""
        try:
            self.summary['end_time'] = datetime.now().isoformat()
            with open(self.summary_file, 'w', encoding='utf-8') as f:
                json.dump(self.summary, f, indent=2, ensure_ascii=False)
            
            print(f"\n{'='*60}")
            print(f"Processing Summary saved to: {self.summary_file}")
            print(f"{'='*60}")
        except Exception as e:
            print(f"Warning: Could not save summary: {e}")
    
    def should_process(self, category_name: str) -> bool:
        """Check if category should be processed (not already completed)"""
        if category_name in self.progress['completed']:
            print(f"Skipping {category_name} (already completed)")
            return False
        return True
    
    def process_category(self, category_name: str, osm_key: str, osm_value: str, schema_type: str) -> bool:
        """
        Process a single category by delegating to osm_data_fetcher.process_amenity_data
        
        This method ONLY handles:
        - Progress tracking
        - Error handling
        - Performance measurement
        
        All data fetching, enrichment, and file writing is delegated to:
        osm_data_fetcher.process_amenity_data()
        
        Args:
            category_name: Category identifier (e.g., "atm", "fuel_station")
            osm_key: OpenStreetMap key (e.g., "amenity")
            osm_value: OpenStreetMap value (e.g., "atm")
            schema_type: Schema.org type (e.g., "schema:FinancialService")
        
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"[BatchProcessor] Processing: {category_name.upper()}")
        print(f"[BatchProcessor] OSM Query: {osm_key}={osm_value}")
        print(f"[BatchProcessor] Schema Type: {schema_type}")
        print(f"[BatchProcessor] Output Dir: {self.output_dir}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            # CRITICAL: Delegate ALL processing to osm_data_fetcher
            # This function handles:
            # 1. fetch_osm_data() - API calls to Overpass
            # 2. enrich_with_wikidata() - Wikidata enrichment
            # 3. write_turtle_file() - RDF/Turtle generation with Linked Data
            print(f"[BatchProcessor] Calling process_amenity_data() from osm_data_fetcher...")
            
            elements = process_amenity_data(
                category_name=category_name,
                osm_key=osm_key,
                osm_value=osm_value,
                schema_type=schema_type,
                output_dir=str(self.output_dir),
                area_name="Hanoi"
            )
            
            elapsed_time = time.time() - start_time
            
            # Count elements with Wikidata enrichment
            enriched_count = len([e for e in elements 
                                 if e.get('multilingual_labels') or e.get('multilingual_descriptions')])
            
            # Count elements with Wikidata links (from original tags)
            wikidata_count = len([e for e in elements 
                                 if e.get('tags', {}).get('wikidata')])
            
            # Record success
            result = {
                'category': category_name,
                'status': 'success',
                'elements_count': len(elements),
                'enriched_count': enriched_count,
                'wikidata_links': wikidata_count,
                'processing_time': round(elapsed_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            self.progress['completed'].append(category_name)
            self.progress['last_processed'] = category_name
            self._save_progress()
            
            self.summary['processed'] += 1
            self.summary['successful'] += 1
            self.summary['details'].append(result)
            
            print(f"\n[BatchProcessor] ✓ SUCCESS: {category_name}")
            print(f"  - Total elements: {len(elements)}")
            print(f"  - Wikidata-enriched: {enriched_count}")
            print(f"  - Wikidata links: {wikidata_count}")
            print(f"  - Processing time: {elapsed_time:.2f}s")
            return True
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = str(e)
            
            print(f"\n[BatchProcessor] ✗ FAILED: {category_name}")
            print(f"  - Error: {error_msg}")
            print(f"  - Processing time: {elapsed_time:.2f}s")
            
            self._log_error(category_name, error_msg)
            
            # Record failure
            result = {
                'category': category_name,
                'status': 'failed',
                'error': error_msg,
                'processing_time': round(elapsed_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            self.progress['failed'].append(category_name)
            self._save_progress()
            
            self.summary['processed'] += 1
            self.summary['failed'] += 1
            self.summary['details'].append(result)
            
            return False
    
    def process_all(self, start_from: str = None, max_categories: int = None):
        """
        Process all amenity types
        
        Args:
            start_from: Category name to start from (useful for resuming)
            max_categories: Maximum number of categories to process (for testing)
        """
        print(f"\n{'#'*60}")
        print(f"# Batch Processing: OSM Data Fetcher & RDF Generator")
        print(f"# Total categories: {len(AMENITY_TYPES)}")
        print(f"# Output directory: {self.output_dir.absolute()}")
        print(f"{'#'*60}\n")
        
        # Filter test cases
        test_cases = AMENITY_TYPES
        
        # Start from specific category if requested
        if start_from:
            try:
                start_idx = next(i for i, (name, _, _, _) in enumerate(test_cases) if name == start_from)
                test_cases = test_cases[start_idx:]
                print(f"Resuming from: {start_from}\n")
            except StopIteration:
                print(f"Warning: Category '{start_from}' not found, starting from beginning\n")
        
        # Limit number of categories if requested
        if max_categories:
            test_cases = test_cases[:max_categories]
            print(f"Processing limited to first {max_categories} categories\n")
        
        # Process each category
        for idx, (category_name, osm_key, osm_value, schema_type) in enumerate(test_cases, 1):
            print(f"\n[{idx}/{len(test_cases)}] Current: {category_name}")
            
            # Check if already processed
            if not self.should_process(category_name):
                self.summary['skipped'] += 1
                continue
            
            # Process the category
            success = self.process_category(category_name, osm_key, osm_value, schema_type)
            
            # Wait between categories (except for the last one)
            if idx < len(test_cases):
                delay = BATCH_CONFIG['delay_between_categories']
                print(f"\nWaiting {delay}s before next category...")
                time.sleep(delay)
        
        # Save final summary
        self._save_summary()
        
        # Print final statistics
        print(f"\n{'#'*60}")
        print(f"# Batch Processing Complete!")
        print(f"{'#'*60}")
        print(f"Total processed: {self.summary['processed']}")
        print(f"Successful: {self.summary['successful']}")
        print(f"Failed: {self.summary['failed']}")
        print(f"Skipped: {self.summary['skipped']}")
        
        if self.progress['failed']:
            print(f"\nFailed categories: {', '.join(self.progress['failed'])}")
            print(f"Check error log: {self.error_log_file}")
        
        print(f"\nAll results saved to: {self.output_dir.absolute()}")
        print(f"{'#'*60}\n")
    
    def retry_failed(self):
        """Retry all failed categories"""
        failed = self.progress.get('failed', [])
        
        if not failed:
            print("No failed categories to retry")
            return
        
        print(f"\nRetrying {len(failed)} failed categories...")
        
        # Remove from failed list (will be re-added if they fail again)
        self.progress['failed'] = []
        self._save_progress()
        
        # Find and process failed categories
        for category_name in failed:
            test_case = next(
                ((name, key, val, schema) for name, key, val, schema in AMENITY_TYPES if name == category_name),
                None
            )
            
            if test_case:
                self.process_category(*test_case)
                time.sleep(BATCH_CONFIG['delay_between_categories'])


def main():
    """Main entry point"""
    import sys
    
    processor = BatchProcessor()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'retry':
            # Retry failed categories
            processor.retry_failed()
        elif command == 'test':
            # Test mode: process only first 3 categories
            print("Running in TEST mode (first 3 categories only)\n")
            processor.process_all(max_categories=3)
        elif command.startswith('from:'):
            # Resume from specific category
            start_category = command.split(':', 1)[1]
            processor.process_all(start_from=start_category)
        else:
            print(f"Unknown command: {command}")
            print("Usage:")
            print("  python batch_processor.py          # Process all categories")
            print("  python batch_processor.py test     # Process first 3 categories (test mode)")
            print("  python batch_processor.py retry    # Retry failed categories")
            print("  python batch_processor.py from:atm # Resume from specific category")
    else:
        # Process all categories
        processor.process_all()


if __name__ == "__main__":
    main()
