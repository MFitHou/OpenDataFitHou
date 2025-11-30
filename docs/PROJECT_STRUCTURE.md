# Project Structure

This document describes the organization of the OpenDataFitHou repository.

## Directory Overview

### `/src`
Main source code directory containing all application logic:

- **`fetchers/`**: Data fetching modules
  - `osm_data_fetcher.py`: Fetches data from OpenStreetMap via Overpass API
  
- **`processors/`**: Data processing and transformation modules
  - `batch_processor.py`: Batch processing utilities
  - `clean_*.py`: Data cleaning scripts for various data types
  - `generate_topology.py`: Generates topology data
  - `second_pass_cleaning.py`: Secondary data cleaning pass
  
- **`validators/`**: Data validation modules
  - `verify_*.py`: Various verification scripts
  
- **`utils/`**: Utility functions and helpers
  - `smart_translate_lookup.py`: Translation utilities

### `/tests`
Testing directory containing all test files:
- `test_*.py`: Unit tests
- `check_*.py`: Validation checks
- `debug_*.py`: Debug scripts

### `/notebooks`
Jupyter notebooks for data exploration and documentation:
- `OverpassApi.ipynb`: Demonstrates OSM data fetching
- `ParseRDF.ipynb`: Shows RDF conversion process

### `/scripts`
Standalone utility scripts:
- `example_topology_queries.py`: Example queries for topology data

### `/config`
Configuration files:
- `config_amenity_types.py`: Amenity type configurations

### `/data`
Data directory (not versioned except for samples):
- `*.geojson`: GeoJSON data files
- `ontology.owl`: Ontology definitions
- `opendata_hanoi/`: Processed RDF data

### `/datav2`
Version 2 of processed data:
- `data_hanoi_*.ttl`: RDF files by category
- `cleaned/`: Cleaned data files

### `/docs`
Documentation files:
- API documentation
- Setup guides
- System design documents

## Code Organization Principles

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Modularity**: Code is organized into reusable modules
3. **Testability**: Tests are separated from source code
4. **Documentation**: Notebooks and docs provide examples and guidance

## Import Patterns

When importing from within the project:

```python
# From root directory
from src.fetchers.osm_data_fetcher import fetch_osm_data
from src.processors.batch_processor import process_batch
from src.utils.smart_translate_lookup import translate

# Within src modules
from fetchers.osm_data_fetcher import fetch_osm_data
```

## Adding New Modules

1. Place source code in appropriate `src/` subdirectory
2. Add tests in `tests/` directory
3. Update this document
4. Add examples to `notebooks/` if applicable
