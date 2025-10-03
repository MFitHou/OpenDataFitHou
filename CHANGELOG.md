# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Copyright headers compliance with GPL-3.0 license requirements
- CHANGELOG.md to track project changes

### Changed
- Improved documentation structure

## [0.0.1] - 2025-10-03
- Initial release
- Project setup and basic structure

## [1.0.0] - 2025-10-03
### Added
- Overpass API integration for collecting geographical data from OpenStreetMap
- RDF/Turtle data conversion functionality
- Support for multiple data types:
  - ATM locations (`atm.geojson`, `atm_expanded_clean.ttl`)
  - Bus stops (`bus_stop.geojson`, `bus_stop_expanded_clean.ttl`)
  - Drinking water fountains (`drinking_water.geojson`, `drinking_water_expanded_clean.ttl`)
  - Hospitals (`hospital.geojson`, `hospital_expanded_clean.ttl`)
  - Playgrounds (`playground.geojson`, `playgrounds_expanded_clean.ttl`)
  - Schools (`school.geojson`, `school_expanded_clean.ttl`)
  - Public toilets (`toilets.geojson`, `toilets_expanded_clean.ttl`)
- Jupyter notebooks for data processing:
  - `OverpassApi.ipynb` - Data collection from Overpass API
  - `ParseRDF.ipynb` - RDF parsing and conversion
- Structured data directories:
  - `data/` - GeoJSON format data
  - `opendata_hanoi/` - RDF/Turtle format data
- Project documentation:
  - `README.md` with project overview and usage instructions
  - `LICENSE` file with GNU GPL v3.0 terms
  - `SECURITY.md` for security policy

### Technical Details
- Geographic coverage: Hanoi area (lat: 20.9-21.2, lon: 105.7-106.0)
- Data format support: GeoJSON, RDF/Turtle
- Integration with Wikidata SPARQL endpoint for data enrichment
- Grid-based data collection approach for comprehensive coverage

### Dependencies
- `requests` - HTTP library for API calls
- `pandas` - Data manipulation and analysis
- `rdflib` - RDF processing library

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

## Version Format

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backwards compatible manner  
- **PATCH** version when you make backwards compatible bug fixes

## Links

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html)
