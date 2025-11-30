#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    : generate_topology.py
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
from pathlib import Path
from typing import Dict, List, Tuple, Set
from math import radians, cos, sin, asin, sqrt

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, GEO
from tqdm import tqdm

# ============================================================================
# NAMESPACE DEFINITIONS
# ============================================================================
SCHEMA = Namespace("http://schema.org/")
EXT = Namespace("http://opendatafithou.org/def/extension/")
WGS84 = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
FIWARE = Namespace("https://smartdatamodels.org/dataModel.PointOfInterest/")
NGSILD = Namespace("https://uri.etsi.org/ngsi-ld/")

# ============================================================================
# RELATIONSHIP CONFIGURATION MATRIX
# ============================================================================
LINK_CONFIG = [
    # --- TRANSPORT (Bus Connects to Everything) ---
    {
        "source": "bus_stop",
        "targets": ["school", "university", "hospital", "marketplace", "supermarket", 
                    "community_centre", "park", "clinic", "library", "post_office"],
        "predicate": "schema:amenityFeature",  # Bus stop serves these places
        "max_dist": 500  # 500m is max walking distance for bus
    },
    
    # --- PARKING (Parking supports Destinations) ---
    {
        "source": "parking",
        "targets": ["park", "marketplace", "supermarket", "hospital", "clinic", 
                    "restaurant", "cafe", "library", "community_centre"],
        "predicate": "schema:publicAccess",
        "max_dist": 300
    },
    
    # --- HEALTH ECOSYSTEM ---
    {
        "source": "pharmacy",
        "targets": ["hospital", "clinic"],
        "predicate": "schema:isNextTo",  # Pharmacy usually next to Hospital
        "max_dist": 100
    },
    {
        "source": "clinic",
        "targets": ["pharmacy", "hospital"],
        "predicate": "ext:healthcareNetwork",
        "max_dist": 200
    },
    
    # --- EDUCATION PROXIMITY ---
    {
        "source": "school",
        "targets": ["playground", "library", "bus_stop", "park"],
        "predicate": "ext:educationSupport",
        "max_dist": 300
    },
    {
        "source": "kindergarten",
        "targets": ["playground", "park"],
        "predicate": "ext:childFriendly",
        "max_dist": 200
    },
    {
        "source": "university",
        "targets": ["library", "cafe", "restaurant", "bus_stop"],
        "predicate": "ext:campusAmenity",
        "max_dist": 500
    },
    
    # --- COMMERCIAL CLUSTERS ---
    {
        "source": "cafe",
        "targets": ["restaurant", "convenience_store", "supermarket"],
        "predicate": "ext:commercialCluster",
        "max_dist": 200
    },
    {
        "source": "restaurant",
        "targets": ["cafe", "marketplace", "supermarket"],
        "predicate": "ext:diningArea",
        "max_dist": 200
    },
    {
        "source": "supermarket",
        "targets": ["pharmacy", "bank", "atm"],
        "predicate": "ext:shoppingDistrict",
        "max_dist": 250
    },
    
    # --- FINANCIAL SERVICES ---
    {
        "source": "bank",
        "targets": ["atm", "post_office"],
        "predicate": "schema:financialService",
        "max_dist": 100
    },
    {
        "source": "atm",
        "targets": ["bank", "supermarket", "marketplace", "fuel_station"],
        "predicate": "ext:financialAccess",
        "max_dist": 150
    },
    
    # --- PUBLIC SERVICES ---
    {
        "source": "police",
        "targets": ["fire_station", "hospital", "post_office"],
        "predicate": "ext:emergencyService",
        "max_dist": 300
    },
    {
        "source": "fire_station",
        "targets": ["police", "hospital"],
        "predicate": "ext:emergencyService",
        "max_dist": 300
    },
    {
        "source": "post_office",
        "targets": ["bank", "community_centre"],
        "predicate": "ext:publicService",
        "max_dist": 200
    },
    
    # --- INFRASTRUCTURE ---
    {
        "source": "charging_station",
        "targets": ["parking", "fuel_station", "supermarket", "marketplace"],
        "predicate": "schema:containedInPlace",
        "max_dist": 50
    },
    {
        "source": "fuel_station",
        "targets": ["charging_station", "convenience_store"],
        "predicate": "ext:vehicleService",
        "max_dist": 100
    },
    {
        "source": "waste_basket",
        "targets": ["bus_stop", "park", "playground", "public_toilet"],
        "predicate": "ext:locatedNear",
        "max_dist": 30
    },
    {
        "source": "drinking_water",
        "targets": ["park", "playground", "school", "kindergarten"],
        "predicate": "ext:locatedNear",
        "max_dist": 50
    },
    {
        "source": "public_toilet",
        "targets": ["park", "marketplace", "bus_stop", "restaurant"],
        "predicate": "ext:publicFacility",
        "max_dist": 100
    },
    
    # --- RECREATION & COMMUNITY ---
    {
        "source": "park",
        "targets": ["playground", "drinking_water", "public_toilet", "waste_basket"],
        "predicate": "ext:parkFacility",
        "max_dist": 200
    },
    {
        "source": "playground",
        "targets": ["park", "school", "kindergarten"],
        "predicate": "ext:recreationArea",
        "max_dist": 150
    },
    {
        "source": "library",
        "targets": ["school", "university", "community_centre"],
        "predicate": "ext:educationHub",
        "max_dist": 400
    },
    {
        "source": "community_centre",
        "targets": ["library", "park", "post_office"],
        "predicate": "ext:communityHub",
        "max_dist": 300
    }
]

# ============================================================================
# OPTIMIZED HAVERSINE DISTANCE CALCULATION
# ============================================================================
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth (in meters).
    Uses the Haversine formula for accuracy.
    
    Args:
        lat1, lon1: Coordinates of first point (decimal degrees)
        lat2, lon2: Coordinates of second point (decimal degrees)
    
    Returns:
        Distance in meters
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    
    return c * r

# ============================================================================
# COORDINATE EXTRACTION
# ============================================================================
def extract_coordinates(graph: Graph) -> Dict[str, Tuple[float, float]]:
    """
    Extract all coordinates from a graph into a dictionary for fast lookup.
    Supports multiple coordinate formats:
    - WKT POINT format (geo:asWKT)
    - Separate lat/long properties (wgs84:lat, wgs84:long, geo:lat, geo:long)
    
    Args:
        graph: RDF graph containing spatial data
    
    Returns:
        Dictionary mapping URIRef to (latitude, longitude) tuples
    """
    coords = {}
    
    # GeoSPARQL namespace for WKT
    GEO_SPARQL = Namespace("http://www.opengis.net/ont/geosparql#")
    
    # Try both WGS84 and GEO namespaces
    for subj in graph.subjects(predicate=RDF.type):
        lat = None
        lon = None
        
        # Method 1: Check for WKT POINT format (most common in this dataset)
        for wkt_obj in graph.objects(subject=subj, predicate=GEO_SPARQL.asWKT):
            wkt_str = str(wkt_obj)
            # Parse "POINT(lon lat)" format
            if "POINT" in wkt_str:
                try:
                    # Extract coordinates from "POINT(lon lat)"
                    coords_str = wkt_str.split("POINT(")[1].split(")")[0]
                    lon_str, lat_str = coords_str.strip().split()
                    lon = float(lon_str)
                    lat = float(lat_str)
                except (IndexError, ValueError):
                    pass
        
        # Method 2: Check WGS84 namespace (fallback)
        if lat is None or lon is None:
            for lat_obj in graph.objects(subject=subj, predicate=WGS84.lat):
                lat = float(lat_obj)
            for lon_obj in graph.objects(subject=subj, predicate=WGS84.long):
                lon = float(lon_obj)
        
        # Method 3: Check GEO namespace (fallback)
        if lat is None or lon is None:
            for lat_obj in graph.objects(subject=subj, predicate=GEO.lat):
                lat = float(lat_obj)
            for lon_obj in graph.objects(subject=subj, predicate=GEO.long):
                lon = float(lon_obj)
        
        if lat is not None and lon is not None:
            coords[str(subj)] = (lat, lon)
    
    return coords

# ============================================================================
# DISTANCE TIER LOGIC
# ============================================================================
def get_predicate_for_distance(distance_m: float, base_predicate: str) -> URIRef:
    """
    Determine the appropriate semantic predicate based on distance tiers.
    
    Distance Tiers:
    - <= 50m: schema:containedInPlace (Strictly inside/adjacent)
    - 50m < d <= 200m: schema:isNextTo (Short walk)
    - 200m < d <= max_dist: Use base_predicate from config
    
    Args:
        distance_m: Distance in meters
        base_predicate: The generic predicate from LINK_CONFIG (e.g., "schema:amenityFeature")
    
    Returns:
        URIRef of the appropriate predicate
    """
    # Critical distance tier logic
    if distance_m <= 50:
        return SCHEMA.containedInPlace
    elif 50 < distance_m <= 200:
        return SCHEMA.isNextTo
    else:
        # Use the generic predicate from config for distances > 200m
        # Parse the base predicate (e.g., "schema:amenityFeature")
        if base_predicate.startswith("schema:"):
            return SCHEMA[base_predicate.split(":")[1]]
        elif base_predicate.startswith("ext:"):
            return EXT[base_predicate.split(":")[1]]
        else:
            return URIRef(base_predicate)

# ============================================================================
# MAIN TOPOLOGY GENERATION
# ============================================================================
def generate_topology(data_dir: Path, output_file: Path):
    """
    Generate spatial topology relationships between all configured amenity types.
    
    Args:
        data_dir: Directory containing input TTL files
        output_file: Path to output topology file
    """
    print("=" * 80)
    print("SPATIAL TOPOLOGY GENERATOR")
    print("=" * 80)
    
    # Initialize output graph
    topology_graph = Graph()
    # Explicit namespace binding to avoid schema1: prefix issue
    topology_graph.bind("schema", SCHEMA)
    topology_graph.bind("ext", EXT)
    topology_graph.bind("geo", GEO)
    topology_graph.bind("wgs84", WGS84)
    topology_graph.bind("fiware", FIWARE)
    topology_graph.bind("ngsi-ld", NGSILD)
    topology_graph.bind("rdf", RDF)
    topology_graph.bind("rdfs", RDFS)
    
    # Step 1: Collect all unique dataset names from config
    dataset_names = set()
    for config in LINK_CONFIG:
        dataset_names.add(config["source"])
        dataset_names.update(config["targets"])
    
    print(f"\n📊 Found {len(dataset_names)} unique dataset types in configuration")
    print(f"📁 Data directory: {data_dir}")
    
    # Step 2: Load all graphs into memory
    print("\n⏳ Loading graphs into memory...")
    graphs = {}
    coords = {}
    
    for dataset_name in tqdm(sorted(dataset_names), desc="Loading datasets"):
        # Try cleaned version first, then original
        file_path = data_dir / f"data_hanoi_{dataset_name}_cleaned.ttl"
        if not file_path.exists():
            file_path = data_dir / f"data_hanoi_{dataset_name}.ttl"
        
        if file_path.exists():
            try:
                g = Graph()
                g.parse(str(file_path), format="turtle")
                graphs[dataset_name] = g
                
                # Extract coordinates for fast lookup
                coords[dataset_name] = extract_coordinates(g)
                
                print(f"  ✓ {dataset_name}: {len(coords[dataset_name])} entities")
            except Exception as e:
                print(f"  ✗ {dataset_name}: Error loading - {e}")
        else:
            print(f"  ⚠ {dataset_name}: File not found")
    
    print(f"\n✓ Loaded {len(graphs)} datasets successfully")
    
    # Step 3: Generate topology relationships
    print("\n🔗 Generating spatial topology relationships...")
    total_links = 0
    stats = {
        "containedInPlace": 0,  # <= 50m
        "isNextTo": 0,           # 50-200m
        "other": 0               # > 200m
    }
    
    for config in tqdm(LINK_CONFIG, desc="Processing link configurations"):
        source_name = config["source"]
        target_names = config["targets"]
        base_predicate = config["predicate"]
        max_dist = config["max_dist"]
        
        # Skip if source doesn't exist
        if source_name not in graphs or source_name not in coords:
            continue
        
        source_coords = coords[source_name]
        
        # Process each target
        for target_name in target_names:
            if target_name not in graphs or target_name not in coords:
                continue
            
            target_coords = coords[target_name]
            
            # Calculate distances between all source-target pairs
            for source_uri, (s_lat, s_lon) in source_coords.items():
                for target_uri, (t_lat, t_lon) in target_coords.items():
                    # Skip self-links
                    if source_uri == target_uri:
                        continue
                    
                    # Calculate distance in meters
                    distance_m = haversine_distance(s_lat, s_lon, t_lat, t_lon)
                    
                    # Check if within max distance
                    if distance_m <= max_dist:
                        # Get appropriate predicate based on distance tier
                        # Critical: Use distance_m consistently
                        predicate = get_predicate_for_distance(distance_m, base_predicate)
                        
                        # Add triple to topology graph
                        topology_graph.add((
                            URIRef(source_uri),
                            predicate,
                            URIRef(target_uri)
                        ))
                        
                        # Update statistics - verify distance tiers match predicate logic
                        total_links += 1
                        if distance_m <= 50:
                            stats["containedInPlace"] += 1
                        elif 50 < distance_m <= 200:
                            stats["isNextTo"] += 1
                        else:
                            stats["other"] += 1
    
    # Step 4: Write output
    print(f"\n💾 Writing topology to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Force rebind namespaces to avoid schema1: prefix issue
    # Clear any conflicting namespace bindings and rebind explicitly
    for prefix, namespace in list(topology_graph.namespace_manager.namespaces()):
        if str(namespace) == "http://schema.org/":
            topology_graph.namespace_manager.bind(prefix, namespace, override=False, replace=True)
    
    # Ensure schema: is properly bound (override any auto-generated prefix)
    topology_graph.namespace_manager.bind("schema", SCHEMA, override=True, replace=True)
    
    topology_graph.serialize(destination=str(output_file), format="turtle")
    
    # Step 5: Report statistics
    print("\n" + "=" * 80)
    print("TOPOLOGY GENERATION COMPLETE")
    print("=" * 80)
    print(f"📊 Total relationships generated: {total_links:,}")
    
    if total_links > 0:
        print(f"\nDistance Tier Breakdown:")
        print(f"  • ≤ 50m (containedInPlace):  {stats['containedInPlace']:>8,} ({stats['containedInPlace']/total_links*100:.1f}%)")
        print(f"  • 50-200m (isNextTo):        {stats['isNextTo']:>8,} ({stats['isNextTo']/total_links*100:.1f}%)")
        print(f"  • >200m (domain-specific):   {stats['other']:>8,} ({stats['other']/total_links*100:.1f}%)")
    else:
        print("\n⚠️  No relationships were generated. This could be because:")
        print("  • No coordinate data found in input files")
        print("  • All amenities are beyond configured max distances")
        print("  • Input files are empty or improperly formatted")
    
    print(f"\n✅ Output saved to: {output_file}")
    print("=" * 80)

# ============================================================================
# ENTRY POINT
# ============================================================================
def main():
    """Main entry point for the topology generator."""
    # Determine paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "datav2" / "cleaned"
    
    # Fall back to non-cleaned if cleaned directory doesn't exist
    if not data_dir.exists():
        data_dir = script_dir / "datav2"
    
    output_file = script_dir / "datav2" / "data_hanoi_topology.ttl"
    
    # Generate topology
    try:
        generate_topology(data_dir, output_file)
    except KeyboardInterrupt:
        print("\n\n⚠ Topology generation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during topology generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
