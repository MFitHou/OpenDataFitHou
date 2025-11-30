# Spatial Topology Generator for Smart City Data

## Overview

The **Spatial Topology Generator** (`generate_topology.py`) is a comprehensive tool that creates semantic spatial relationships between different amenity types in Hanoi. It uses distance-based tiers to assign appropriate predicates, enabling intelligent querying and reasoning over the city's infrastructure.

## Key Features

### 1. **Multi-Tier Distance Semantics**
The system automatically assigns predicates based on calculated distances:

- **≤ 50m**: `schema:containedInPlace` - Strictly inside/adjacent (e.g., ATM inside a fuel station)
- **50-200m**: `schema:isNextTo` - Short walking distance (e.g., pharmacy next to hospital)
- **>200m**: Domain-specific predicates based on configuration (e.g., `schema:amenityFeature` for bus stops serving schools)

### 2. **Comprehensive Relationship Matrix**
The system handles 24 logical connection patterns across multiple domains:

#### Transport Connectivity
- **Bus Stops** connect to schools, hospitals, markets, community centers (up to 500m)
- **Parking** supports parks, markets, hospitals, restaurants (up to 300m)

#### Health Ecosystem
- **Pharmacies** cluster near hospitals and clinics (100m)
- **Clinics** networked with hospitals (200m)

#### Education Infrastructure
- **Schools** linked to playgrounds, libraries, parks (300m)
- **Kindergartens** near child-friendly facilities (200m)
- **Universities** connected to cafes, libraries, bus stops (500m)

#### Commercial Clusters
- **Cafes** clustered with restaurants and stores (200m)
- **Supermarkets** near banks, pharmacies (250m)

#### Public Services
- **Emergency services** (police, fire stations) networked (300m)
- **Financial services** (banks, ATMs) interconnected (100-150m)

#### Urban Amenities
- **Parks** connected to playgrounds, toilets, drinking water (200m)
- **Public facilities** (toilets, waste baskets, drinking water) near high-traffic areas (30-100m)

### 3. **Performance Optimizations**

- ✅ **Memory Loading**: All graphs loaded into RAM before processing
- ✅ **Coordinate Caching**: WKT coordinates extracted once per dataset
- ✅ **Optimized Haversine**: Fast distance calculations using pure Python
- ✅ **Progress Tracking**: Real-time progress bars via `tqdm`
- ✅ **Smart Filtering**: Only checks configured pairs (avoids O(N²) explosion)

## Generated Topology Statistics

```
Total Relationships: 84,397
Unique Entities: 11,170

Distance Tier Breakdown:
  • ≤ 50m (containedInPlace):     7,388 (8.8%)
  • 50-200m (isNextTo):          55,884 (66.2%)
  • >200m (domain-specific):     21,125 (25.0%)

Top Predicates:
  • isNextTo: 55,884
  • amenityFeature: 14,096
  • containedInPlace: 7,388
  • publicAccess: 2,552
  • campusAmenity: 2,317
  • educationSupport: 1,501
  • shoppingDistrict: 392
  • educationHub: 102
  • emergencyService: 89
  • communityHub: 76
```

## Usage

### Basic Execution
```bash
python generate_topology.py
```

### Input Requirements
- TTL files in `datav2/` or `datav2/cleaned/`
- Files must contain WKT POINT coordinates: `geo:asWKT "POINT(lon lat)"`
- Naming convention: `data_hanoi_{amenity_type}.ttl`

### Output
- **File**: `datav2/data_hanoi_topology.ttl`
- **Format**: Turtle (RDF)
- **Content**: Spatial relationship triples

## Architecture

### 1. Configuration Matrix (`LINK_CONFIG`)
Defines which amenity pairs to check:

```python
{
    "source": "bus_stop",
    "targets": ["school", "hospital", "market"],
    "predicate": "schema:amenityFeature",
    "max_dist": 500
}
```

### 2. Coordinate Extraction
Supports multiple formats:
- WKT POINT format (primary): `geo:asWKT "POINT(105.789 20.981)"`
- Separate properties (fallback): `wgs84:lat`, `wgs84:long`

### 3. Distance Calculation
Uses optimized Haversine formula for great-circle distances on Earth's surface.

### 4. Predicate Assignment
Dynamic tier-based logic:
```python
if distance <= 50m:
    predicate = schema:containedInPlace
elif distance <= 200m:
    predicate = schema:isNextTo
else:
    predicate = configured_predicate
```

## Example Queries

### Find all amenities within 50m of a specific location
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?target WHERE {
  <urn:ngsi-ld:PointOfInterest:Hanoi:hospital:123>
    schema:containedInPlace ?target .
}
```

### Find all schools accessible by bus
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?school WHERE {
  ?bus_stop a schema:BusStop ;
            schema:amenityFeature ?school .
  ?school a schema:School .
}
```

### Find healthcare networks
```sparql
PREFIX ex: <http://example.org/hanoi/>

SELECT ?clinic ?hospital WHERE {
  ?clinic ex:healthcareNetwork ?hospital .
  ?clinic a schema:Clinic .
  ?hospital a schema:Hospital .
}
```

## Configuration Guide

### Adding New Relationship Types

1. **Identify the amenity types** (source and targets)
2. **Choose semantic predicate** based on relationship nature
3. **Set max distance** appropriate for use case
4. **Add to LINK_CONFIG**:

```python
{
    "source": "library",
    "targets": ["cafe", "coworking_space"],
    "predicate": "ex:studyHub",
    "max_dist": 400
}
```

### Custom Predicates

Define custom namespaces in the script:
```python
EX = Namespace("http://example.org/hanoi/")
CUSTOM = Namespace("http://mycity.org/topology/")
```

## Performance Metrics

**Test Environment**: Windows, 27 datasets, 13,146 entities total

- **Loading Time**: ~4 seconds
- **Processing Time**: ~25 seconds
- **Total Runtime**: ~30 seconds
- **Output Size**: 93,513 lines (84,397 triples)

## Dependencies

```txt
rdflib>=7.0.0
tqdm>=4.66.0
```

Install via:
```bash
pip install rdflib tqdm
```

## Troubleshooting

### No relationships generated?
- Verify input files contain `geo:asWKT` coordinates
- Check file naming matches configuration (e.g., `data_hanoi_bus_stop.ttl`)
- Ensure max_dist values are appropriate for your city

### Out of memory errors?
- Process datasets in batches
- Reduce max_dist values to limit combinations
- Filter LINK_CONFIG to essential relationships only

### Slow performance?
- Ensure coordinate extraction happens once (cached)
- Use cleaned dataset files if available
- Reduce number of target amenities per source

## Future Enhancements

- [ ] Add spatial indexing (R-tree) for very large datasets
- [ ] Support for polygon containment (beyond point distances)
- [ ] Time-based accessibility (e.g., bus schedules)
- [ ] Weighted relationships based on accessibility metrics
- [ ] Export to GeoJSON for visualization

## License

Same as parent project (see root LICENSE file)

## Contact

For questions or suggestions about the topology generator, please open an issue in the repository.
