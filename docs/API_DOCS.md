# OpenDataFitHou API Documentation

**Version:** 1.0.0  
**Standard:** ETSI ISG CIM NGSI-LD  
**Last Updated:** December 1, 2025  
**Language:** English | [Vietnamese](#phần-tiếng-việt)

---

## Table of Contents

1. [Introduction](#introduction)
2. [NGSI-LD Standard Overview](#ngsi-ld-standard-overview)
3. [Core API Endpoints](#core-api-endpoints)
   - [3.1 Retrieve Entity](#31-retrieve-entity)
   - [3.2 Query Entities](#32-query-entities)
   - [3.3 Temporal Evolution](#33-temporal-evolution)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Vietnamese Version](#phần-tiếng-việt)

---

## 1. Introduction

The OpenDataFitHou API provides standardized access to Smart City data for Hanoi, Vietnam. The API integrates:

- **Static Data**: Points of Interest (POI) stored in Apache Jena Fuseki (RDF/SPARQL)
- **IoT Time-Series Data**: Sensor observations stored in InfluxDB
- **Topology**: Spatial relationships between entities

This documentation is designed for backend developers implementing the NestJS API layer.

### Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  NestJS API  │─────▶│Jena Fuseki  │
│ Application │      │  (NGSI-LD)   │      │   (Static)  │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            │
                            ▼
                     ┌─────────────┐
                     │  InfluxDB   │
                     │ (Time-Series)│
                     └─────────────┘
```

---

## 2. NGSI-LD Standard Overview

### 2.1 What is NGSI-LD?

**NGSI-LD** (Next Generation Service Interface - Linked Data) is an **information model and API specification** developed by the ETSI Industry Specification Group for Context Information Management (ISG CIM).

It enables:
- **Publishing** context information (entities and their properties)
- **Querying** context information (filtering by type, attributes, location)
- **Subscribing** to context changes (notifications when data updates)

NGSI-LD uses **JSON-LD** (JSON for Linked Data) to link data concepts to global ontologies such as:
- **SOSA/SSN**: Sensor, Observation, Sample, and Actuator ontology
- **Schema.org**: Structured data vocabularies
- **GeoSPARQL**: Geographic queries and spatial relationships

### 2.2 Core Rules for Developers

#### 🔴 **Mandatory Rule #1: MIME Type**
All API responses **MUST** use:
```
Content-Type: application/ld+json
```

Alternatively, if using `application/json`, include a Link header:
```
Link: <http://context-url>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"
```

#### 🔴 **Mandatory Rule #2: Entity IDs**
All entity identifiers **MUST** be URNs (Uniform Resource Names):

```
Format: urn:ngsi-ld:{EntityType}:{Location}:{Category}:{UniqueId}

Examples:
✅ urn:ngsi-ld:Device:Hanoi:station:CauGiay
✅ urn:ngsi-ld:PointOfInterest:Hanoi:atm:1000087341
❌ "device-123" (Invalid - not a URN)
❌ "http://example.com/device/123" (Invalid - HTTP URL, not URN)
```

#### 🔴 **Mandatory Rule #3: @context Field**
Every JSON-LD response **MUST** include a `@context` field linking to vocabulary definitions:

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "http://opendatafithou.org/contexts/smart-city.jsonld"
  ],
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  ...
}
```

#### 🔴 **Mandatory Rule #4: GeoJSON Format**
Location data **MUST** follow the GeoJSON specification:

```json
{
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [105.8245, 21.0285]  // [longitude, latitude]
    }
  }
}
```

**⚠️ Important:** Coordinates order is `[longitude, latitude]`, not `[latitude, longitude]`.

### 2.3 NGSI-LD Property Types

NGSI-LD defines three types of attributes:

| Type | Purpose | Example |
|------|---------|---------|
| **Property** | Simple attribute with value | `"temperature": {"type": "Property", "value": 28.5}` |
| **Relationship** | Reference to another entity | `"isSampledBy": {"type": "Relationship", "object": "urn:ngsi-ld:Device:..."}` |
| **GeoProperty** | Geographic location | `"location": {"type": "GeoProperty", "value": {"type": "Point", ...}}` |

### 2.4 Temporal Representation

For historical data, NGSI-LD uses a temporal format with `observedAt`:

```json
{
  "temperature": {
    "type": "Property",
    "value": 28.5,
    "observedAt": "2025-12-01T10:30:00Z"
  }
}
```

For temporal queries, responses contain arrays of historical values.

---

## 3. Core API Endpoints

### 3.1 Retrieve Entity

**Get the current state of a single entity (Context Snapshot)**

#### Endpoint
```
GET /ngsi-ld/v1/entities/{entityId}
```

#### Purpose
Retrieve the **current snapshot** of an entity, combining:
- **Static metadata** from Jena Fuseki (name, location, relationships)
- **Latest IoT values** from InfluxDB (temperature, AQI, traffic intensity)

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entityId` | Path | ✅ Yes | URN of the entity (e.g., `urn:ngsi-ld:Device:Hanoi:station:Lang`) |
| `options` | Query | ❌ No | `keyValues` for simplified representation (default: `normalized`) |
| `attrs` | Query | ❌ No | Comma-separated list of attributes to include |

#### Example Request

```bash
GET /ngsi-ld/v1/entities/urn:ngsi-ld:Device:Hanoi:station:Lang
Accept: application/ld+json
```

#### Example Response (Normalized Format)

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    {
      "sosa": "http://www.w3.org/ns/sosa/",
      "schema": "http://schema.org/",
      "property": "http://opendatafithou.org/property/"
    }
  ],
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  "type": "Device",
  "name": {
    "type": "Property",
    "value": "Trạm Láng - IoT Monitoring Station"
  },
  "description": {
    "type": "Property",
    "value": "Multi-sensor IoT station for air quality, weather, and traffic monitoring"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [105.8084, 21.0245]
    }
  },
  "serialNumber": {
    "type": "Property",
    "value": "STATION-LANG-2025"
  },
  "controlledAsset": {
    "type": "Property",
    "value": "Dong Da District Monitoring Area"
  },
  "temperature": {
    "type": "Property",
    "value": 28.5,
    "unitCode": "CEL",
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "humidity": {
    "type": "Property",
    "value": 72,
    "unitCode": "P1",
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "pm25": {
    "type": "Property",
    "value": 45.3,
    "unitCode": "GQ",
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "aqi": {
    "type": "Property",
    "value": 89,
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "hosts": {
    "type": "Relationship",
    "object": [
      "http://opendatafithou.org/sensor/Lang:Weather",
      "http://opendatafithou.org/sensor/Lang:AirQuality",
      "http://opendatafithou.org/sensor/Lang:Traffic"
    ]
  }
}
```

#### Example Response (KeyValues Format)

```bash
GET /ngsi-ld/v1/entities/urn:ngsi-ld:Device:Hanoi:station:Lang?options=keyValues
```

```json
{
  "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  "type": "Device",
  "name": "Trạm Láng - IoT Monitoring Station",
  "location": {
    "type": "Point",
    "coordinates": [105.8084, 21.0245]
  },
  "temperature": 28.5,
  "humidity": 72,
  "pm25": 45.3,
  "aqi": 89
}
```

#### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Entity found and returned |
| 404 | Not Found | Entity ID does not exist |
| 400 | Bad Request | Invalid entity ID format |
| 500 | Internal Server Error | Database connection error |

---

### 3.2 Query Entities

**Discover and filter entities (Discovery & Geo-fencing)**

#### Endpoint
```
GET /ngsi-ld/v1/entities
```

#### Purpose
Search for entities matching specific criteria:
- Filter by **type** (e.g., all ATMs, all IoT stations)
- Filter by **attributes** (e.g., AQI > 100)
- Filter by **geographic location** (e.g., within 1km of a point)

#### Query Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `type` | Query | ✅ Yes | Entity type to filter | `PointOfInterest`, `Device` |
| `q` | Query | ❌ No | Query language filter (simple expressions) | `aqi>100`, `temperature>=30` |
| `georel` | Query | ❌ No | Spatial relationship | `near;maxDistance==1000` (1km) |
| `geometry` | Query | ❌ No | GeoJSON geometry type | `Point`, `Polygon` |
| `coordinates` | Query | ❌ No | Coordinates for spatial query | `[105.8245,21.0285]` |
| `limit` | Query | ❌ No | Max number of results (default: 20) | `50` |
| `offset` | Query | ❌ No | Pagination offset | `20` |
| `attrs` | Query | ❌ No | Comma-separated attributes to include | `name,location,aqi` |

#### Example 1: Find All ATMs

```bash
GET /ngsi-ld/v1/entities?type=PointOfInterest&q=amenity=="atm"
Accept: application/ld+json
```

#### Response

```json
{
  "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
  "type": "EntityCollection",
  "totalCount": 1250,
  "entities": [
    {
      "id": "urn:ngsi-ld:PointOfInterest:Hanoi:atm:1000087341",
      "type": "PointOfInterest",
      "name": {
        "type": "Property",
        "value": "Trạm ATM Eximbank"
      },
      "location": {
        "type": "GeoProperty",
        "value": {
          "type": "Point",
          "coordinates": [105.8371058, 21.0264133]
        }
      },
      "brand": {
        "type": "Property",
        "value": "Eximbank"
      }
    },
    // ... more entities
  ]
}
```

#### Example 2: Find Sensors with High AQI

```bash
GET /ngsi-ld/v1/entities?type=Device&q=aqi>100
Accept: application/ld+json
```

#### Example 3: Geo-fencing - Find POIs within 1km

**Scenario:** Find all points of interest within 1 kilometer of Hoan Kiem Lake (21.0285°N, 105.8542°E).

```bash
GET /ngsi-ld/v1/entities?type=PointOfInterest&georel=near;maxDistance==1000&geometry=Point&coordinates=[105.8542,21.0285]
Accept: application/ld+json
```

#### Response

```json
{
  "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
  "type": "EntityCollection",
  "totalCount": 45,
  "entities": [
    {
      "id": "urn:ngsi-ld:PointOfInterest:Hanoi:atm:1000087341",
      "type": "PointOfInterest",
      "name": {
        "type": "Property",
        "value": "Trạm ATM Eximbank"
      },
      "location": {
        "type": "GeoProperty",
        "value": {
          "type": "Point",
          "coordinates": [105.8371058, 21.0264133]
        }
      },
      "distance": {
        "type": "Property",
        "value": 850,
        "unitCode": "MTR"
      }
    },
    // ... more entities
  ]
}
```

#### Backend Implementation Notes

For geo-spatial queries, the backend must:

1. **Extract coordinates** from the query parameters
2. **Convert to SPARQL Geo query** using GeoSPARQL functions:

```sparql
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

SELECT ?entity ?name ?location
WHERE {
  ?entity a schema:PointOfInterest ;
          schema:name ?name ;
          geo:hasGeometry ?geom .
  
  ?geom geo:asWKT ?location .
  
  FILTER(geof:distance(?location, "POINT(105.8542 21.0285)"^^geo:wktLiteral, <http://www.opengis.net/def/uom/OGC/1.0/metre>) < 1000)
}
```

3. **Transform SPARQL results** to NGSI-LD format
4. **Sort by distance** (optional)

#### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Query executed successfully |
| 400 | Bad Request | Invalid query syntax or parameters |
| 413 | Payload Too Large | Result set exceeds maximum size |
| 500 | Internal Server Error | Database query error |

---

### 3.3 Temporal Evolution

**Get historical time-series data (History)**

#### Endpoint
```
GET /ngsi-ld/v1/temporal/entities/{entityId}
```

#### Purpose
Retrieve **historical values** of entity attributes over a time range. This endpoint queries InfluxDB for time-series data.

#### Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `entityId` | Path | ✅ Yes | URN of the entity | `urn:ngsi-ld:Device:Hanoi:station:Lang` |
| `timeAt` | Query | ✅ Yes | Start time (ISO 8601) | `2025-11-01T00:00:00Z` |
| `endTimeAt` | Query | ✅ Yes | End time (ISO 8601) | `2025-12-01T00:00:00Z` |
| `attrs` | Query | ❌ No | Comma-separated attributes | `temperature,humidity,aqi` |
| `lastN` | Query | ❌ No | Return only last N values | `100` |
| `timeproperty` | Query | ❌ No | Temporal property to query (default: `observedAt`) | `observedAt` |

#### Example Request

```bash
GET /ngsi-ld/v1/temporal/entities/urn:ngsi-ld:Device:Hanoi:station:Lang?timeAt=2025-11-01T00:00:00Z&endTimeAt=2025-12-01T00:00:00Z&attrs=temperature,aqi
Accept: application/ld+json
```

#### Example Response (Temporal Representation)

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    {
      "property": "http://opendatafithou.org/property/"
    }
  ],
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  "type": "Device",
  "temperature": [
    {
      "type": "Property",
      "value": 25.3,
      "unitCode": "CEL",
      "observedAt": "2025-11-01T00:00:00Z"
    },
    {
      "type": "Property",
      "value": 26.1,
      "unitCode": "CEL",
      "observedAt": "2025-11-01T01:00:00Z"
    },
    {
      "type": "Property",
      "value": 27.5,
      "unitCode": "CEL",
      "observedAt": "2025-11-01T02:00:00Z"
    },
    // ... more values
  ],
  "aqi": [
    {
      "type": "Property",
      "value": 78,
      "observedAt": "2025-11-01T00:00:00Z"
    },
    {
      "type": "Property",
      "value": 82,
      "observedAt": "2025-11-01T01:00:00Z"
    },
    {
      "type": "Property",
      "value": 95,
      "observedAt": "2025-11-01T02:00:00Z"
    },
    // ... more values
  ]
}
```

#### Backend Implementation Notes

The temporal endpoint requires:

1. **Query InfluxDB** using Flux query language:

```flux
from(bucket: "opendatafithou")
  |> range(start: 2025-11-01T00:00:00Z, stop: 2025-12-01T00:00:00Z)
  |> filter(fn: (r) => r["station"] == "Lang")
  |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "aqi")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
```

2. **Transform results** to NGSI-LD temporal format
3. **Group by attribute name** (temperature, aqi, etc.)
4. **Sort by timestamp** (ascending)

#### Aggregation Support (Optional)

For large time ranges, support aggregation:

```bash
GET /ngsi-ld/v1/temporal/entities/urn:ngsi-ld:Device:Hanoi:station:Lang?timeAt=2025-01-01T00:00:00Z&endTimeAt=2025-12-01T00:00:00Z&attrs=temperature&aggrMethod=avg&aggrPeriodDuration=PT1H
```

- `aggrMethod`: `avg`, `min`, `max`, `sum`
- `aggrPeriodDuration`: ISO 8601 duration (e.g., `PT1H` = 1 hour)

#### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Temporal data retrieved |
| 400 | Bad Request | Invalid time format or parameters |
| 404 | Not Found | Entity does not exist |
| 413 | Payload Too Large | Time range too large (> 1 year) |
| 500 | Internal Server Error | InfluxDB query error |

---

## 4. Data Models

### 4.1 Device (IoT Station)

Represents an IoT monitoring station with multiple sensors.

```json
{
  "id": "urn:ngsi-ld:Device:Hanoi:station:{StationName}",
  "type": "Device",
  "name": { "type": "Property", "value": "string" },
  "description": { "type": "Property", "value": "string" },
  "location": { "type": "GeoProperty", "value": { "type": "Point", "coordinates": [lon, lat] } },
  "serialNumber": { "type": "Property", "value": "string" },
  "controlledAsset": { "type": "Property", "value": "string" },
  "hosts": { "type": "Relationship", "object": ["sensor-uri-1", "sensor-uri-2"] }
}
```

**Real-time IoT Properties (from InfluxDB):**
- `temperature`, `humidity`, `windSpeed`, `rainfall` (Weather)
- `pm25`, `pm10`, `aqi` (Air Quality)
- `trafficIntensity`, `vehicleSpeed` (Traffic)
- `noiseLevel` (Noise)
- `waterLevel`, `floodRisk` (Flood)

### 4.2 PointOfInterest (POI)

Represents a static location (ATM, hospital, school, etc.).

```json
{
  "id": "urn:ngsi-ld:PointOfInterest:Hanoi:{category}:{osmId}",
  "type": "PointOfInterest",
  "name": { "type": "Property", "value": "string" },
  "location": { "type": "GeoProperty", "value": { "type": "Point", "coordinates": [lon, lat] } },
  "brand": { "type": "Property", "value": "string" },
  "operator": { "type": "Property", "value": "string" },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "string",
      "addressLocality": "string",
      "addressRegion": "string"
    }
  },
  "isNextTo": { "type": "Relationship", "object": "urn:ngsi-ld:..." },
  "isSampledBy": { "type": "Relationship", "object": "urn:ngsi-ld:Device:..." }
}
```

### 4.3 AirQualityObserved

Specialized entity for air quality data (FIWARE data model).

```json
{
  "id": "urn:ngsi-ld:AirQualityObserved:Hanoi:{station}:{timestamp}",
  "type": "AirQualityObserved",
  "dateObserved": { "type": "Property", "value": "2025-12-01T10:30:00Z" },
  "location": { "type": "GeoProperty", "value": { "type": "Point", "coordinates": [lon, lat] } },
  "pm25": { "type": "Property", "value": 45.3, "unitCode": "GQ" },
  "pm10": { "type": "Property", "value": 78.2, "unitCode": "GQ" },
  "aqi": { "type": "Property", "value": 89 },
  "refDevice": { "type": "Relationship", "object": "urn:ngsi-ld:Device:..." }
}
```

---

## 5. Error Handling

### 5.1 Error Response Format

All errors must follow the NGSI-LD error format:

```json
{
  "type": "https://uri.etsi.org/ngsi-ld/errors/BadRequestData",
  "title": "Invalid query syntax",
  "detail": "The 'q' parameter contains an invalid expression: 'aqi>>100'",
  "status": 400
}
```

### 5.2 Standard Error Types

| Type | HTTP Code | Description |
|------|-----------|-------------|
| `BadRequestData` | 400 | Invalid request syntax or parameters |
| `ResourceNotFound` | 404 | Entity or resource does not exist |
| `AlreadyExists` | 409 | Attempting to create an entity that already exists |
| `OperationNotSupported` | 422 | Operation is not supported by the implementation |
| `LdContextNotAvailable` | 503 | @context URL is unreachable |
| `InternalError` | 500 | Unexpected server error |

### 5.3 Validation Rules

**Entity ID Validation:**
```typescript
const entityIdPattern = /^urn:ngsi-ld:[A-Za-z0-9]+:[A-Za-z0-9:_-]+$/;

if (!entityIdPattern.test(entityId)) {
  throw new BadRequestException({
    type: 'https://uri.etsi.org/ngsi-ld/errors/BadRequestData',
    title: 'Invalid Entity ID',
    detail: 'Entity ID must be a valid URN',
    status: 400
  });
}
```

**Coordinates Validation:**
```typescript
function validateCoordinates(lon: number, lat: number) {
  if (lon < -180 || lon > 180) {
    throw new BadRequestException('Longitude must be between -180 and 180');
  }
  if (lat < -90 || lat > 90) {
    throw new BadRequestException('Latitude must be between -90 and 90');
  }
}
```

---

## 6. Implementation Checklist

### Backend Developers Must:

- [ ] Set `Content-Type: application/ld+json` for all responses
- [ ] Validate all entity IDs are valid URNs
- [ ] Include `@context` in all JSON-LD responses
- [ ] Use GeoJSON format for location data (coordinates: [lon, lat])
- [ ] Implement SPARQL geo-spatial queries for `georel` parameter
- [ ] Connect to InfluxDB for temporal queries
- [ ] Handle ISO 8601 timestamps correctly
- [ ] Support pagination (`limit`, `offset`)
- [ ] Return proper NGSI-LD error format
- [ ] Log all API requests for debugging

### Testing Checklist:

- [ ] Test with Postman/curl using URN entity IDs
- [ ] Test geo-fencing with different distances (100m, 1km, 5km)
- [ ] Test temporal queries with different time ranges (1 day, 1 week, 1 month)
- [ ] Test pagination with large result sets
- [ ] Test error handling (invalid IDs, missing parameters)
- [ ] Validate JSON-LD syntax using online validators

---

# Phần Tiếng Việt

## Tài liệu API OpenDataFitHou

**Phiên bản:** 1.0.0  
**Tiêu chuẩn:** ETSI ISG CIM NGSI-LD  
**Cập nhật lần cuối:** 1 tháng 12, 2025  
**Ngôn ngữ:** [English](#opendatafithou-api-documentation) | Tiếng Việt

---

## Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Tổng quan tiêu chuẩn NGSI-LD](#2-tổng-quan-tiêu-chuẩn-ngsi-ld)
3. [Các Endpoint API chính](#3-các-endpoint-api-chính)
   - [3.1 Truy xuất thực thể](#31-truy-xuất-thực-thể)
   - [3.2 Truy vấn thực thể](#32-truy-vấn-thực-thể)
   - [3.3 Diễn biến theo thời gian](#33-diễn-biến-theo-thời-gian)
4. [Mô hình dữ liệu](#4-mô-hình-dữ-liệu)
5. [Xử lý lỗi](#5-xử-lý-lỗi)

---

## 1. Giới thiệu

API OpenDataFitHou cung cấp quyền truy cập chuẩn hóa vào dữ liệu Thành phố Thông minh cho Hà Nội, Việt Nam. API tích hợp:

- **Dữ liệu tĩnh**: Các điểm quan tâm (POI) được lưu trữ trong Apache Jena Fuseki (RDF/SPARQL)
- **Dữ liệu chuỗi thời gian IoT**: Quan sát từ cảm biến được lưu trữ trong InfluxDB
- **Topology**: Mối quan hệ không gian giữa các thực thể

Tài liệu này được thiết kế cho các nhà phát triển backend triển khai lớp API NestJS.

### Tổng quan kiến trúc

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  NestJS API  │─────▶│Jena Fuseki  │
│ Application │      │  (NGSI-LD)   │      │  (Tĩnh)     │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            │
                            ▼
                     ┌─────────────┐
                     │  InfluxDB   │
                     │(Chuỗi T.Gian)│
                     └─────────────┘
```

---

## 2. Tổng quan tiêu chuẩn NGSI-LD

### 2.1 NGSI-LD là gì?

**NGSI-LD** (Next Generation Service Interface - Linked Data) là một **mô hình thông tin và đặc tả API** được phát triển bởi Nhóm Đặc tả Công nghiệp ETSI cho Quản lý Thông tin Ngữ cảnh (ISG CIM).

Nó cho phép:
- **Xuất bản** thông tin ngữ cảnh (thực thể và các thuộc tính của chúng)
- **Truy vấn** thông tin ngữ cảnh (lọc theo loại, thuộc tính, vị trí)
- **Đăng ký** thay đổi ngữ cảnh (thông báo khi dữ liệu cập nhật)

NGSI-LD sử dụng **JSON-LD** (JSON cho Linked Data) để liên kết các khái niệm dữ liệu với các ontology toàn cầu như:
- **SOSA/SSN**: Ontology cho Cảm biến, Quan sát, Mẫu và Thiết bị kích hoạt
- **Schema.org**: Từ vựng dữ liệu có cấu trúc
- **GeoSPARQL**: Truy vấn địa lý và quan hệ không gian

### 2.2 Quy tắc cốt lõi cho nhà phát triển

#### 🔴 **Quy tắc bắt buộc #1: MIME Type**
Tất cả phản hồi API **BẮT BUỘC** sử dụng:
```
Content-Type: application/ld+json
```

Hoặc nếu sử dụng `application/json`, thêm header Link:
```
Link: <http://context-url>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"
```

#### 🔴 **Quy tắc bắt buộc #2: ID thực thể**
Tất cả định danh thực thể **BẮT BUỘC** là URN (Uniform Resource Names):

```
Định dạng: urn:ngsi-ld:{LoạiThựcThể}:{VịTrí}:{DanhMục}:{IdDuyNhất}

Ví dụ:
✅ urn:ngsi-ld:Device:Hanoi:station:CauGiay
✅ urn:ngsi-ld:PointOfInterest:Hanoi:atm:1000087341
❌ "device-123" (Không hợp lệ - không phải URN)
❌ "http://example.com/device/123" (Không hợp lệ - HTTP URL, không phải URN)
```

#### 🔴 **Quy tắc bắt buộc #3: Trường @context**
Mọi phản hồi JSON-LD **BẮT BUỘC** bao gồm trường `@context` liên kết đến định nghĩa từ vựng:

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "http://opendatafithou.org/contexts/smart-city.jsonld"
  ],
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  ...
}
```

#### 🔴 **Quy tắc bắt buộc #4: Định dạng GeoJSON**
Dữ liệu vị trí **BẮT BUỘC** tuân theo đặc tả GeoJSON:

```json
{
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [105.8245, 21.0285]  // [kinh độ, vĩ độ]
    }
  }
}
```

**⚠️ Quan trọng:** Thứ tự tọa độ là `[kinh độ, vĩ độ]`, không phải `[vĩ độ, kinh độ]`.

### 2.3 Các loại thuộc tính NGSI-LD

NGSI-LD định nghĩa ba loại thuộc tính:

| Loại | Mục đích | Ví dụ |
|------|---------|--------|
| **Property** | Thuộc tính đơn giản với giá trị | `"temperature": {"type": "Property", "value": 28.5}` |
| **Relationship** | Tham chiếu đến thực thể khác | `"isSampledBy": {"type": "Relationship", "object": "urn:ngsi-ld:Device:..."}` |
| **GeoProperty** | Vị trí địa lý | `"location": {"type": "GeoProperty", "value": {"type": "Point", ...}}` |

### 2.4 Biểu diễn theo thời gian

Đối với dữ liệu lịch sử, NGSI-LD sử dụng định dạng thời gian với `observedAt`:

```json
{
  "temperature": {
    "type": "Property",
    "value": 28.5,
    "observedAt": "2025-12-01T10:30:00Z"
  }
}
```

Đối với truy vấn thời gian, phản hồi chứa mảng các giá trị lịch sử.

---

## 3. Các Endpoint API chính

### 3.1 Truy xuất thực thể

**Lấy trạng thái hiện tại của một thực thể đơn (Ảnh chụp nhanh ngữ cảnh)**

#### Endpoint
```
GET /ngsi-ld/v1/entities/{entityId}
```

#### Mục đích
Truy xuất **ảnh chụp nhanh hiện tại** của một thực thể, kết hợp:
- **Metadata tĩnh** từ Jena Fuseki (tên, vị trí, mối quan hệ)
- **Giá trị IoT mới nhất** từ InfluxDB (nhiệt độ, AQI, mật độ giao thông)

#### Tham số

| Tham số | Loại | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `entityId` | Path | ✅ Có | URN của thực thể (vd: `urn:ngsi-ld:Device:Hanoi:station:Lang`) |
| `options` | Query | ❌ Không | `keyValues` cho biểu diễn đơn giản (mặc định: `normalized`) |
| `attrs` | Query | ❌ Không | Danh sách các thuộc tính cần bao gồm (phân cách bằng dấu phẩy) |

#### Ví dụ Request

```bash
GET /ngsi-ld/v1/entities/urn:ngsi-ld:Device:Hanoi:station:Lang
Accept: application/ld+json
```

#### Ví dụ Response (Định dạng Normalized)

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    {
      "sosa": "http://www.w3.org/ns/sosa/",
      "schema": "http://schema.org/",
      "property": "http://opendatafithou.org/property/"
    }
  ],
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  "type": "Device",
  "name": {
    "type": "Property",
    "value": "Trạm Láng - Trạm quan trắc IoT"
  },
  "description": {
    "type": "Property",
    "value": "Trạm IoT đa cảm biến giám sát chất lượng không khí, thời tiết và giao thông"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [105.8084, 21.0245]
    }
  },
  "serialNumber": {
    "type": "Property",
    "value": "STATION-LANG-2025"
  },
  "controlledAsset": {
    "type": "Property",
    "value": "Khu vực giám sát Quận Đống Đa"
  },
  "temperature": {
    "type": "Property",
    "value": 28.5,
    "unitCode": "CEL",
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "humidity": {
    "type": "Property",
    "value": 72,
    "unitCode": "P1",
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "pm25": {
    "type": "Property",
    "value": 45.3,
    "unitCode": "GQ",
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "aqi": {
    "type": "Property",
    "value": 89,
    "observedAt": "2025-12-01T10:30:00Z"
  },
  "hosts": {
    "type": "Relationship",
    "object": [
      "http://opendatafithou.org/sensor/Lang:Weather",
      "http://opendatafithou.org/sensor/Lang:AirQuality",
      "http://opendatafithou.org/sensor/Lang:Traffic"
    ]
  }
}
```

#### Mã trạng thái HTTP

| Mã | Ý nghĩa | Mô tả |
|----|---------|-------|
| 200 | Thành công | Tìm thấy và trả về thực thể |
| 404 | Không tìm thấy | ID thực thể không tồn tại |
| 400 | Yêu cầu không hợp lệ | Định dạng ID thực thể không hợp lệ |
| 500 | Lỗi máy chủ nội bộ | Lỗi kết nối cơ sở dữ liệu |

---

### 3.2 Truy vấn thực thể

**Khám phá và lọc thực thể (Khám phá & Rào chắn địa lý)**

#### Endpoint
```
GET /ngsi-ld/v1/entities
```

#### Mục đích
Tìm kiếm các thực thể khớp với tiêu chí cụ thể:
- Lọc theo **loại** (vd: tất cả ATM, tất cả trạm IoT)
- Lọc theo **thuộc tính** (vd: AQI > 100)
- Lọc theo **vị trí địa lý** (vd: trong vòng 1km từ một điểm)

#### Tham số truy vấn

| Tham số | Loại | Bắt buộc | Mô tả | Ví dụ |
|---------|------|----------|-------|-------|
| `type` | Query | ✅ Có | Loại thực thể cần lọc | `PointOfInterest`, `Device` |
| `q` | Query | ❌ Không | Bộ lọc ngôn ngữ truy vấn (biểu thức đơn giản) | `aqi>100`, `temperature>=30` |
| `georel` | Query | ❌ Không | Quan hệ không gian | `near;maxDistance==1000` (1km) |
| `geometry` | Query | ❌ Không | Loại hình học GeoJSON | `Point`, `Polygon` |
| `coordinates` | Query | ❌ Không | Tọa độ cho truy vấn không gian | `[105.8245,21.0285]` |
| `limit` | Query | ❌ Không | Số kết quả tối đa (mặc định: 20) | `50` |
| `offset` | Query | ❌ Không | Độ lệch phân trang | `20` |
| `attrs` | Query | ❌ Không | Thuộc tính cần bao gồm (phân cách bằng dấu phẩy) | `name,location,aqi` |

#### Ví dụ 1: Tìm tất cả ATM

```bash
GET /ngsi-ld/v1/entities?type=PointOfInterest&q=amenity=="atm"
Accept: application/ld+json
```

#### Ví dụ 2: Tìm cảm biến có AQI cao

```bash
GET /ngsi-ld/v1/entities?type=Device&q=aqi>100
Accept: application/ld+json
```

#### Ví dụ 3: Rào chắn địa lý - Tìm POI trong vòng 1km

**Tình huống:** Tìm tất cả điểm quan tâm trong vòng 1 kilomet từ Hồ Hoàn Kiếm (21.0285°N, 105.8542°E).

```bash
GET /ngsi-ld/v1/entities?type=PointOfInterest&georel=near;maxDistance==1000&geometry=Point&coordinates=[105.8542,21.0285]
Accept: application/ld+json
```

#### Ghi chú triển khai Backend

Đối với truy vấn không gian địa lý, backend phải:

1. **Trích xuất tọa độ** từ tham số truy vấn
2. **Chuyển đổi sang truy vấn SPARQL Geo** sử dụng hàm GeoSPARQL:

```sparql
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

SELECT ?entity ?name ?location
WHERE {
  ?entity a schema:PointOfInterest ;
          schema:name ?name ;
          geo:hasGeometry ?geom .
  
  ?geom geo:asWKT ?location .
  
  FILTER(geof:distance(?location, "POINT(105.8542 21.0285)"^^geo:wktLiteral, <http://www.opengis.net/def/uom/OGC/1.0/metre>) < 1000)
}
```

3. **Chuyển đổi kết quả SPARQL** sang định dạng NGSI-LD
4. **Sắp xếp theo khoảng cách** (tùy chọn)

---

### 3.3 Diễn biến theo thời gian

**Lấy dữ liệu chuỗi thời gian lịch sử (Lịch sử)**

#### Endpoint
```
GET /ngsi-ld/v1/temporal/entities/{entityId}
```

#### Mục đích
Truy xuất **giá trị lịch sử** của các thuộc tính thực thể trong một khoảng thời gian. Endpoint này truy vấn InfluxDB cho dữ liệu chuỗi thời gian.

#### Tham số

| Tham số | Loại | Bắt buộc | Mô tả | Ví dụ |
|---------|------|----------|-------|-------|
| `entityId` | Path | ✅ Có | URN của thực thể | `urn:ngsi-ld:Device:Hanoi:station:Lang` |
| `timeAt` | Query | ✅ Có | Thời gian bắt đầu (ISO 8601) | `2025-11-01T00:00:00Z` |
| `endTimeAt` | Query | ✅ Có | Thời gian kết thúc (ISO 8601) | `2025-12-01T00:00:00Z` |
| `attrs` | Query | ❌ Không | Thuộc tính (phân cách bằng dấu phẩy) | `temperature,humidity,aqi` |
| `lastN` | Query | ❌ Không | Chỉ trả về N giá trị cuối cùng | `100` |

#### Ví dụ Request

```bash
GET /ngsi-ld/v1/temporal/entities/urn:ngsi-ld:Device:Hanoi:station:Lang?timeAt=2025-11-01T00:00:00Z&endTimeAt=2025-12-01T00:00:00Z&attrs=temperature,aqi
Accept: application/ld+json
```

#### Ví dụ Response (Biểu diễn theo thời gian)

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    {
      "property": "http://opendatafithou.org/property/"
    }
  ],
  "id": "urn:ngsi-ld:Device:Hanoi:station:Lang",
  "type": "Device",
  "temperature": [
    {
      "type": "Property",
      "value": 25.3,
      "unitCode": "CEL",
      "observedAt": "2025-11-01T00:00:00Z"
    },
    {
      "type": "Property",
      "value": 26.1,
      "unitCode": "CEL",
      "observedAt": "2025-11-01T01:00:00Z"
    },
    {
      "type": "Property",
      "value": 27.5,
      "unitCode": "CEL",
      "observedAt": "2025-11-01T02:00:00Z"
    }
    // ... thêm giá trị
  ],
  "aqi": [
    {
      "type": "Property",
      "value": 78,
      "observedAt": "2025-11-01T00:00:00Z"
    },
    {
      "type": "Property",
      "value": 82,
      "observedAt": "2025-11-01T01:00:00Z"
    },
    {
      "type": "Property",
      "value": 95,
      "observedAt": "2025-11-01T02:00:00Z"
    }
    // ... thêm giá trị
  ]
}
```

#### Ghi chú triển khai Backend

Endpoint thời gian yêu cầu:

1. **Truy vấn InfluxDB** sử dụng ngôn ngữ truy vấn Flux:

```flux
from(bucket: "opendatafithou")
  |> range(start: 2025-11-01T00:00:00Z, stop: 2025-12-01T00:00:00Z)
  |> filter(fn: (r) => r["station"] == "Lang")
  |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "aqi")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
```

2. **Chuyển đổi kết quả** sang định dạng thời gian NGSI-LD
3. **Nhóm theo tên thuộc tính** (temperature, aqi, v.v.)
4. **Sắp xếp theo timestamp** (tăng dần)

---

## 4. Mô hình dữ liệu

### 4.1 Device (Trạm IoT)

Đại diện cho một trạm giám sát IoT với nhiều cảm biến.

```json
{
  "id": "urn:ngsi-ld:Device:Hanoi:station:{TênTrạm}",
  "type": "Device",
  "name": { "type": "Property", "value": "string" },
  "description": { "type": "Property", "value": "string" },
  "location": { "type": "GeoProperty", "value": { "type": "Point", "coordinates": [lon, lat] } },
  "serialNumber": { "type": "Property", "value": "string" },
  "controlledAsset": { "type": "Property", "value": "string" },
  "hosts": { "type": "Relationship", "object": ["sensor-uri-1", "sensor-uri-2"] }
}
```

**Thuộc tính IoT thời gian thực (từ InfluxDB):**
- `temperature`, `humidity`, `windSpeed`, `rainfall` (Thời tiết)
- `pm25`, `pm10`, `aqi` (Chất lượng không khí)
- `trafficIntensity`, `vehicleSpeed` (Giao thông)
- `noiseLevel` (Tiếng ồn)
- `waterLevel`, `floodRisk` (Lũ lụt)

### 4.2 PointOfInterest (POI)

Đại diện cho một vị trí tĩnh (ATM, bệnh viện, trường học, v.v.).

```json
{
  "id": "urn:ngsi-ld:PointOfInterest:Hanoi:{danh_mục}:{osmId}",
  "type": "PointOfInterest",
  "name": { "type": "Property", "value": "string" },
  "location": { "type": "GeoProperty", "value": { "type": "Point", "coordinates": [lon, lat] } },
  "brand": { "type": "Property", "value": "string" },
  "operator": { "type": "Property", "value": "string" },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "string",
      "addressLocality": "string",
      "addressRegion": "string"
    }
  },
  "isNextTo": { "type": "Relationship", "object": "urn:ngsi-ld:..." },
  "isSampledBy": { "type": "Relationship", "object": "urn:ngsi-ld:Device:..." }
}
```

---

## 5. Xử lý lỗi

### 5.1 Định dạng phản hồi lỗi

Tất cả các lỗi phải tuân theo định dạng lỗi NGSI-LD:

```json
{
  "type": "https://uri.etsi.org/ngsi-ld/errors/BadRequestData",
  "title": "Cú pháp truy vấn không hợp lệ",
  "detail": "Tham số 'q' chứa biểu thức không hợp lệ: 'aqi>>100'",
  "status": 400
}
```

### 5.2 Các loại lỗi chuẩn

| Loại | Mã HTTP | Mô tả |
|------|---------|-------|
| `BadRequestData` | 400 | Cú pháp yêu cầu hoặc tham số không hợp lệ |
| `ResourceNotFound` | 404 | Thực thể hoặc tài nguyên không tồn tại |
| `AlreadyExists` | 409 | Cố gắng tạo thực thể đã tồn tại |
| `OperationNotSupported` | 422 | Thao tác không được hỗ trợ |
| `LdContextNotAvailable` | 503 | URL @context không thể truy cập |
| `InternalError` | 500 | Lỗi máy chủ không mong đợi |

---

## 6. Danh sách kiểm tra triển khai

### Nhà phát triển Backend phải:

- [ ] Đặt `Content-Type: application/ld+json` cho tất cả phản hồi
- [ ] Xác thực tất cả ID thực thể là URN hợp lệ
- [ ] Bao gồm `@context` trong tất cả phản hồi JSON-LD
- [ ] Sử dụng định dạng GeoJSON cho dữ liệu vị trí (coordinates: [lon, lat])
- [ ] Triển khai truy vấn SPARQL không gian địa lý cho tham số `georel`
- [ ] Kết nối với InfluxDB cho truy vấn thời gian
- [ ] Xử lý timestamp ISO 8601 chính xác
- [ ] Hỗ trợ phân trang (`limit`, `offset`)
- [ ] Trả về định dạng lỗi NGSI-LD đúng
- [ ] Ghi log tất cả yêu cầu API để debug

### Danh sách kiểm tra thử nghiệm:

- [ ] Thử nghiệm với Postman/curl sử dụng ID thực thể URN
- [ ] Thử nghiệm rào chắn địa lý với các khoảng cách khác nhau (100m, 1km, 5km)
- [ ] Thử nghiệm truy vấn thời gian với các khoảng thời gian khác nhau (1 ngày, 1 tuần, 1 tháng)
- [ ] Thử nghiệm phân trang với bộ kết quả lớn
- [ ] Thử nghiệm xử lý lỗi (ID không hợp lệ, thiếu tham số)
- [ ] Xác thực cú pháp JSON-LD sử dụng công cụ xác thực trực tuyến

---

**© 2025 OpenDataFitHou Team | Licensed under GNU GPL v3.0**
