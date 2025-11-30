# -*- coding: utf-8 -*-
"""
@File    : generate_iot_semantics.py
@Project : OpenDataFitHou
@Date    : 2025-12-01
@Author  : MFitHou Team

Script để generate semantic metadata (RDF/Turtle) cho IoT infrastructure và coverage.
Tạo liên kết giữa Static Data (POIs) và Real-time Data (InfluxDB sensors).

Part 1: iot_infrastructure.ttl - Định nghĩa Stations và Sensors theo W3C SOSA/SSN
Part 2: iot_coverage.ttl - Linking POIs với nearest monitoring stations

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
from typing import Dict, List, Tuple
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, OWL
from geopy.distance import geodesic
from tqdm import tqdm

# ============================================================================
# NAMESPACES
# ============================================================================

# W3C Semantic Sensor Network Ontology
SOSA = Namespace("http://www.w3.org/ns/sosa/")
SSN = Namespace("http://www.w3.org/ns/ssn/")

# FIWARE NGSI-LD
FIWARE = Namespace("https://uri.fiware.org/ns/data-models#")
NGSI_LD = Namespace("https://uri.etsi.org/ngsi-ld/")

# GeoSPARQL
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
SF = Namespace("http://www.opengis.net/ont/sf#")

# Schema.org
SCHEMA = Namespace("http://schema.org/")

# Project-specific
EX = Namespace("http://opendatafithou.org/resource/")
PROPERTY = Namespace("http://opendatafithou.org/property/")
STATION = Namespace("http://opendatafithou.org/station/")
SENSOR = Namespace("http://opendatafithou.org/sensor/")


# ============================================================================
# STATION CONFIGURATION (from iot_collector.py)
# ============================================================================

STATIONS = [
    # CENTER & HIGH TRAFFIC
    {"id": "urn:ngsi-ld:Device:Hanoi:station:Lang", "name": "Trạm Láng", "key": "Lang", "lat": 21.017, "lon": 105.800, "traffic_factor": 1.2, "drainage_rate": 2.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:CauGiay", "name": "Trạm Cầu Giấy", "key": "CauGiay", "lat": 21.033, "lon": 105.800, "traffic_factor": 1.4, "drainage_rate": 3.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:RoyalCity", "name": "Trạm Ngã Tư Sở", "key": "RoyalCity", "lat": 21.003, "lon": 105.813, "traffic_factor": 1.5, "drainage_rate": 1.5},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:HoGuom", "name": "Trạm Hồ Gươm", "key": "HoGuom", "lat": 21.028, "lon": 105.852, "traffic_factor": 1.1, "drainage_rate": 6.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:TimeCity", "name": "Trạm Minh Khai", "key": "TimeCity", "lat": 20.995, "lon": 105.868, "traffic_factor": 1.3, "drainage_rate": 4.0},
    # SUBURBAN & OPEN SPACE
    {"id": "urn:ngsi-ld:Device:Hanoi:station:HaDong", "name": "Trạm Hà Đông", "key": "HaDong", "lat": 20.971, "lon": 105.776, "traffic_factor": 1.0, "drainage_rate": 5.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:LongBien", "name": "Trạm Long Biên", "key": "LongBien", "lat": 21.036, "lon": 105.894, "traffic_factor": 0.8, "drainage_rate": 9.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:MyDinh", "name": "Trạm Mỹ Đình", "key": "MyDinh", "lat": 21.020, "lon": 105.763, "traffic_factor": 0.9, "drainage_rate": 6.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:TayHo", "name": "Trạm Tây Hồ", "key": "TayHo", "lat": 21.070, "lon": 105.823, "traffic_factor": 0.7, "drainage_rate": 8.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:HoangMai", "name": "Trạm Hoàng Mai", "key": "HoangMai", "lat": 20.963, "lon": 105.843, "traffic_factor": 1.2, "drainage_rate": 3.0},
]


# ============================================================================
# OBSERVABLE PROPERTIES DEFINITIONS
# ============================================================================

OBSERVABLE_PROPERTIES = {
    # Air Quality Properties
    "PM2.5": {
        "uri": PROPERTY["PM2.5"],
        "label": "PM2.5 Particulate Matter",
        "unit": "µg/m³",
        "description": "Fine particulate matter with diameter < 2.5 micrometers"
    },
    "PM10": {
        "uri": PROPERTY["PM10"],
        "label": "PM10 Particulate Matter",
        "unit": "µg/m³",
        "description": "Particulate matter with diameter < 10 micrometers"
    },
    "AQI": {
        "uri": PROPERTY["AQI"],
        "label": "Air Quality Index",
        "unit": "index",
        "description": "Vietnam Air Quality Index (0-500 scale)"
    },
    # Weather Properties
    "Temperature": {
        "uri": PROPERTY["Temperature"],
        "label": "Air Temperature",
        "unit": "°C",
        "description": "Ambient air temperature"
    },
    "Humidity": {
        "uri": PROPERTY["Humidity"],
        "label": "Relative Humidity",
        "unit": "%",
        "description": "Relative humidity percentage"
    },
    "WindSpeed": {
        "uri": PROPERTY["WindSpeed"],
        "label": "Wind Speed",
        "unit": "m/s",
        "description": "Wind speed at surface level"
    },
    "Rainfall": {
        "uri": PROPERTY["Rainfall"],
        "label": "Rainfall",
        "unit": "mm",
        "description": "Precipitation amount in 1 hour"
    },
    # Traffic Properties
    "TrafficIntensity": {
        "uri": PROPERTY["TrafficIntensity"],
        "label": "Traffic Intensity",
        "unit": "0-100",
        "description": "Traffic congestion intensity (0=empty, 100=jam)"
    },
    "VehicleSpeed": {
        "uri": PROPERTY["VehicleSpeed"],
        "label": "Average Vehicle Speed",
        "unit": "km/h",
        "description": "Average speed of vehicles on road"
    },
    # Noise Property
    "NoiseLevel": {
        "uri": PROPERTY["NoiseLevel"],
        "label": "Environmental Noise Level",
        "unit": "dB",
        "description": "Ambient noise level"
    },
    # Flood Properties
    "WaterLevel": {
        "uri": PROPERTY["WaterLevel"],
        "label": "Flood Water Level",
        "unit": "cm",
        "description": "Height of flood water accumulation"
    },
    "FloodRisk": {
        "uri": PROPERTY["FloodRisk"],
        "label": "Flood Risk Level",
        "unit": "categorical",
        "description": "Flood risk assessment (Low, Moderate, High, Critical)"
    }
}


# ============================================================================
# SENSOR TYPES & CONFIGURATIONS
# ============================================================================

SENSOR_TYPES = {
    "AirQuality": {
        "label": "Air Quality Sensor",
        "observes": ["PM2.5", "PM10", "AQI"],
        "description": "Multi-parameter air quality monitoring sensor"
    },
    "Weather": {
        "label": "Weather Sensor",
        "observes": ["Temperature", "Humidity", "WindSpeed", "Rainfall"],
        "description": "Meteorological sensor station"
    },
    "Traffic": {
        "label": "Traffic Flow Sensor",
        "observes": ["TrafficIntensity", "VehicleSpeed"],
        "description": "Traffic monitoring sensor using simulation"
    },
    "Noise": {
        "label": "Noise Level Sensor",
        "observes": ["NoiseLevel"],
        "description": "Environmental noise monitoring sensor"
    },
    "Flood": {
        "label": "Flood Monitoring Sensor",
        "observes": ["WaterLevel", "FloodRisk"],
        "description": "Water level and flood risk assessment sensor"
    }
}


# ============================================================================
# PART 1: GENERATE IOT INFRASTRUCTURE
# ============================================================================

def generate_iot_infrastructure(output_path: str = "datav2/iot_infrastructure.ttl"):
    """
    Generate iot_infrastructure.ttl - Định nghĩa IoT Stations, Sensors và Observable Properties.
    
    Follows:
    - W3C SOSA/SSN Ontology
    - FIWARE NGSI-LD Device Model
    - GeoSPARQL for spatial data
    """
    print("=" * 80)
    print("🏗️  PART 1: GENERATING IOT INFRASTRUCTURE")
    print("=" * 80)
    
    # Initialize graph
    g = Graph()
    
    # Bind namespaces
    g.bind("sosa", SOSA)
    g.bind("ssn", SSN)
    g.bind("fiware", FIWARE)
    g.bind("ngsi-ld", NGSI_LD)
    g.bind("geo", GEO)
    g.bind("sf", SF)
    g.bind("schema", SCHEMA)
    g.bind("ex", EX)
    g.bind("property", PROPERTY)
    g.bind("station", STATION)
    g.bind("sensor", SENSOR)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("owl", OWL)
    
    print(f"\n📋 Step 1: Defining Observable Properties...")
    # Define Observable Properties
    for prop_name, prop_data in OBSERVABLE_PROPERTIES.items():
        prop_uri = prop_data["uri"]
        
        g.add((prop_uri, RDF.type, SOSA.ObservableProperty))
        g.add((prop_uri, RDF.type, SSN.Property))
        g.add((prop_uri, RDFS.label, Literal(prop_data["label"], lang="en")))
        g.add((prop_uri, SCHEMA.description, Literal(prop_data["description"], lang="en")))
        g.add((prop_uri, SCHEMA.unitText, Literal(prop_data["unit"])))
    
    print(f"   ✅ Defined {len(OBSERVABLE_PROPERTIES)} observable properties")
    
    print(f"\n📋 Step 2: Generating Stations and Sensors...")
    # Generate for each station
    for station in tqdm(STATIONS, desc="Processing stations"):
        station_key = station["key"]
        station_uri = URIRef(station["id"])
        station_name = station["name"]
        lat = station["lat"]
        lon = station["lon"]
        
        # ========== PLATFORM (STATION) ==========
        # The Station is a Platform that hosts multiple sensors
        g.add((station_uri, RDF.type, SOSA.Platform))
        g.add((station_uri, RDF.type, FIWARE.Device))
        g.add((station_uri, RDF.type, SSN.System))
        g.add((station_uri, RDFS.label, Literal(station_name, lang="vi")))
        g.add((station_uri, SCHEMA.name, Literal(station_name, lang="vi")))
        
        # Location using GeoSPARQL
        point_wkt = f"POINT({lon} {lat})"
        g.add((station_uri, GEO.hasGeometry, URIRef(f"{station_uri}/geometry")))
        g.add((URIRef(f"{station_uri}/geometry"), RDF.type, SF.Point))
        g.add((URIRef(f"{station_uri}/geometry"), GEO.asWKT, Literal(point_wkt, datatype=GEO.wktLiteral)))
        
        # Schema.org location
        g.add((station_uri, SCHEMA.latitude, Literal(lat, datatype=XSD.decimal)))
        g.add((station_uri, SCHEMA.longitude, Literal(lon, datatype=XSD.decimal)))
        
        # Station metadata
        g.add((station_uri, SCHEMA.address, Literal(f"Hanoi, Vietnam")))
        g.add((station_uri, FIWARE.category, Literal("IoT Monitoring Station")))
        
        # ========== SENSORS (HOSTED BY PLATFORM) ==========
        for sensor_type, sensor_config in SENSOR_TYPES.items():
            sensor_uri = SENSOR[f"{station_key}:{sensor_type}"]
            sensor_label = f"{station_name} - {sensor_config['label']}"
            
            # Sensor definition
            g.add((sensor_uri, RDF.type, SOSA.Sensor))
            g.add((sensor_uri, RDF.type, SSN.System))
            g.add((sensor_uri, RDFS.label, Literal(sensor_label, lang="vi")))
            g.add((sensor_uri, SCHEMA.description, Literal(sensor_config["description"], lang="en")))
            
            # Link sensor to platform
            g.add((sensor_uri, SOSA.isHostedBy, station_uri))
            g.add((station_uri, SOSA.hosts, sensor_uri))
            
            # Link sensor to observable properties
            for prop_name in sensor_config["observes"]:
                prop_uri = OBSERVABLE_PROPERTIES[prop_name]["uri"]
                g.add((sensor_uri, SOSA.observes, prop_uri))
            
            # Sensor metadata
            g.add((sensor_uri, FIWARE.controlledProperty, Literal(", ".join(sensor_config["observes"]))))
    
    print(f"\n✅ Generated infrastructure for {len(STATIONS)} stations")
    print(f"   - Total sensors: {len(STATIONS) * len(SENSOR_TYPES)}")
    
    # Save to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    g.serialize(destination=str(output_file), format="turtle")
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"   - Triples: {len(g)}")
    print(f"   - Size: {output_file.stat().st_size / 1024:.2f} KB")
    
    return g


# ============================================================================
# PART 2: GENERATE IOT COVERAGE (POI-STATION LINKS)
# ============================================================================

def load_pois_from_ttl(data_dir: str = "datav2/cleaned") -> List[Tuple[URIRef, float, float]]:
    """
    Load tất cả POIs từ các file .ttl trong data_dir.
    
    Returns:
        List of tuples: (POI_URI, latitude, longitude)
    """
    print("=" * 80)
    print("📥 LOADING POIs FROM TTL FILES")
    print("=" * 80)
    
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"❌ Directory not found: {data_dir}")
        return []
    
    ttl_files = list(data_path.glob("*.ttl"))
    print(f"\n📂 Found {len(ttl_files)} TTL files")
    
    pois = []
    
    for ttl_file in tqdm(ttl_files, desc="Loading POIs"):
        g = Graph()
        try:
            g.parse(str(ttl_file), format="turtle")
            
            # Query để lấy POI URIs và coordinates từ WKT format
            # Format: "POINT(lon lat)"^^geo:wktLiteral
            query = """
                PREFIX geo: <http://www.opengis.net/ont/geosparql#>
                
                SELECT ?poi ?wkt
                WHERE {
                    ?poi geo:asWKT ?wkt .
                }
            """
            
            results = g.query(query)
            
            for row in results:
                poi_uri = row.poi
                wkt_str = str(row.wkt)
                
                # Parse WKT: "POINT(lon lat)"
                try:
                    # Extract coordinates from POINT(lon lat)
                    coords = wkt_str.replace("POINT(", "").replace(")", "").strip()
                    lon_str, lat_str = coords.split()
                    lon = float(lon_str)
                    lat = float(lat_str)
                    pois.append((poi_uri, lat, lon))
                except Exception as e:
                    # Skip invalid WKT
                    continue
        
        except Exception as e:
            print(f"   ⚠️  Error parsing {ttl_file.name}: {e}")
    
    print(f"\n✅ Loaded {len(pois)} POIs")
    return pois


def find_nearest_station(poi_lat: float, poi_lon: float, stations: List[Dict]) -> Tuple[str, float]:
    """
    Tìm trạm gần nhất với POI dựa trên khoảng cách geodesic.
    
    Returns:
        Tuple of (station_uri, distance_km)
    """
    min_distance = float('inf')
    nearest_station_uri = None
    
    poi_coords = (poi_lat, poi_lon)
    
    for station in stations:
        station_coords = (station["lat"], station["lon"])
        distance = geodesic(poi_coords, station_coords).kilometers
        
        if distance < min_distance:
            min_distance = distance
            nearest_station_uri = station["id"]
    
    return nearest_station_uri, min_distance


def generate_iot_coverage(
    pois: List[Tuple[URIRef, float, float]], 
    output_path: str = "datav2/iot_coverage.ttl"
):
    """
    Generate iot_coverage.ttl - Linking POIs to nearest monitoring stations.
    
    Concept: POI sosa:isSampledBy Station
    Meaning: Environmental data for this POI is sampled/monitored by that station
    """
    print("\n" + "=" * 80)
    print("🔗 PART 2: GENERATING IOT COVERAGE LINKS")
    print("=" * 80)
    
    # Initialize graph
    g = Graph()
    
    # Bind namespaces
    g.bind("sosa", SOSA)
    g.bind("ex", EX)
    g.bind("schema", SCHEMA)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    
    print(f"\n📊 Processing {len(pois)} POIs...")
    
    # Statistics
    coverage_stats = {station["id"]: 0 for station in STATIONS}
    total_distance = 0.0
    
    # Generate links
    for poi_uri, poi_lat, poi_lon in tqdm(pois, desc="Linking POIs to stations"):
        nearest_station_uri, distance_km = find_nearest_station(poi_lat, poi_lon, STATIONS)
        
        # Generate triple: POI sosa:isSampledBy Station
        g.add((poi_uri, SOSA.isSampledBy, URIRef(nearest_station_uri)))
        
        # Optional: Add distance as annotation
        # g.add((poi_uri, SCHEMA.distance, Literal(distance_km, datatype=XSD.decimal)))
        
        coverage_stats[nearest_station_uri] += 1
        total_distance += distance_km
    
    print(f"\n✅ Generated {len(pois)} POI-Station links")
    
    # Print coverage statistics
    print(f"\n📊 Coverage Statistics:")
    print(f"{'Station':<30} {'POIs Covered':<15}")
    print("-" * 50)
    for station in STATIONS:
        count = coverage_stats[station["id"]]
        print(f"{station['name']:<30} {count:<15}")
    
    avg_distance = total_distance / len(pois) if pois else 0
    print(f"\n📏 Average distance POI → Station: {avg_distance:.2f} km")
    
    # Save to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    g.serialize(destination=str(output_file), format="turtle")
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"   - Triples: {len(g)}")
    print(f"   - Size: {output_file.stat().st_size / 1024:.2f} KB")
    
    return g


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Entry point."""
    print("\n" + "=" * 80)
    print("🌐 IOT SEMANTIC METADATA GENERATOR")
    print("=" * 80)
    print("\nGenerating semantic links between Static Data (POIs) and Real-time Data (IoT)")
    print("Following W3C SOSA/SSN and FIWARE NGSI-LD standards\n")
    
    # Part 1: Generate IoT Infrastructure
    infrastructure_graph = generate_iot_infrastructure()
    
    # Part 2: Load POIs and generate coverage
    pois = load_pois_from_ttl()
    
    if pois:
        coverage_graph = generate_iot_coverage(pois)
    else:
        print("\n⚠️  No POIs found. Skipping coverage generation.")
        print("   Make sure datav2/cleaned/ contains TTL files with POIs")
    
    print("\n" + "=" * 80)
    print("✅ SEMANTIC METADATA GENERATION COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    print("  1. datav2/iot_infrastructure.ttl - IoT Stations, Sensors, Observable Properties")
    print("  2. datav2/iot_coverage.ttl - POI-Station coverage links")
    print("\nThese files can now be:")
    print("  - Loaded into Apache Jena Fuseki")
    print("  - Queried using SPARQL")
    print("  - Used to link real-time InfluxDB data with static POI data")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
