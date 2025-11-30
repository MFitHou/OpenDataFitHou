"""
OSM Data Fetcher - Fetch OpenStreetMap data via Overpass API
Handles retry logic, rate limiting, and robust error handling
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path


class OverpassAPIError(Exception):
    """Custom exception for Overpass API errors"""
    pass


# ============================================================================
# BRAND KNOWLEDGE BASE - Auto-enrichment for famous Vietnamese brands
# ============================================================================
# This dictionary provides Wikidata IDs, official websites, and legal names
# for brands that are commonly found in OSM data but lack these tags
BRAND_KNOWLEDGE_BASE = {
    # === BANKS (Vietnamese Banking Sector) ===
    "BIDV": {
        "wikidata": "Q1003180",
        "website": "https://www.bidv.com.vn",
        "legalName_vi": "Ngân hàng TMCP Đầu tư và Phát triển Việt Nam",
        "legalName_en": "Bank for Investment and Development of Vietnam"
    },
    "Agribank": {
        "wikidata": "Q4693331",
        "website": "https://www.agribank.com.vn",
        "legalName_vi": "Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam",
        "legalName_en": "Vietnam Bank for Agriculture and Rural Development"
    },
    "Vietcombank": {
        "wikidata": "Q1527276",
        "website": "https://www.vietcombank.com.vn",
        "legalName_vi": "Ngân hàng TMCP Ngoại thương Việt Nam",
        "legalName_en": "Joint Stock Commercial Bank for Foreign Trade of Vietnam"
    },
    "Techcombank": {
        "wikidata": "Q7692186",
        "website": "https://www.techcombank.com.vn",
        "legalName_vi": "Ngân hàng TMCP Kỹ thương Việt Nam",
        "legalName_en": "Vietnam Technological and Commercial Joint Stock Bank"
    },
    "VietinBank": {
        "wikidata": "Q1369325",
        "website": "https://www.vietinbank.vn",
        "legalName_vi": "Ngân hàng TMCP Công thương Việt Nam",
        "legalName_en": "Vietnam Joint Stock Commercial Bank for Industry and Trade"
    },
    "TPBank": {
        "wikidata": "Q10822606",
        "website": "https://tpb.vn",
        "legalName_vi": "Ngân hàng TMCP Tiên Phong"
    },
    "MB": {
        "wikidata": "Q10795460",
        "website": "https://mbbank.com.vn",
        "legalName_vi": "Ngân hàng TMCP Quân đội",
        "legalName_en": "Military Commercial Joint Stock Bank"
    },
    "ACB": {
        "wikidata": "Q4651228",
        "website": "https://www.acb.com.vn",
        "legalName_vi": "Ngân hàng TMCP Á Châu"
    },
    "Sacombank": {
        "wikidata": "Q6099933",
        "website": "https://www.sacombank.com.vn",
        "legalName_vi": "Ngân hàng TMCP Sài Gòn Thương Tín"
    },
    "VPBank": {
        "wikidata": "Q7906932",
        "website": "https://www.vpbank.com.vn",
        "legalName_vi": "Ngân hàng TMCP Việt Nam Thịnh Vượng"
    },
    
    # === FUEL STATIONS (Petroleum Companies) ===
    "Petrolimex": {
        "wikidata": "Q7179041",
        "website": "https://www.petrolimex.com.vn",
        "legalName_vi": "Tập đoàn Xăng dầu Việt Nam",
        "legalName_en": "Vietnam National Petroleum Group",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/22/Petrolimex_logo.svg"
    },
    "PVOIL": {
        "wikidata": "Q7120617",
        "website": "https://www.pvoil.com.vn",
        "legalName_vi": "Tổng Công ty Dầu Việt Nam",
        "legalName_en": "PetroVietnam Oil Corporation"
    },
    "Shell": {
        "wikidata": "Q154950",
        "website": "https://www.shell.com.vn",
        "legalName_en": "Shell Vietnam"
    },
    
    # === RETAIL & SUPERMARKETS ===
    "WinMart": {
        "wikidata": "Q10834617",
        "website": "https://winmart.vn",
        "legalName_vi": "Siêu thị WinMart"
    },
    "VinMart": {
        "wikidata": "Q10834617",
        "website": "https://winmart.vn",
        "legalName_vi": "Siêu thị VinMart"
    },
    "Co.opMart": {
        "wikidata": "Q5138053",
        "website": "https://www.co-opmart.com.vn",
        "legalName_vi": "Siêu thị Co.op Mart"
    },
    "BigC": {
        "wikidata": "Q857695",
        "website": "https://www.bigc.vn",
        "legalName_en": "Big C Vietnam"
    },
    
    # === COFFEE & FOOD CHAINS ===
    "Highlands Coffee": {
        "wikidata": "Q5759368",
        "website": "https://www.highlandscoffee.com.vn",
        "legalName_vi": "Cà phê Highlands"
    },
    "Starbucks": {
        "wikidata": "Q37158",
        "website": "https://www.starbucks.vn",
        "legalName_en": "Starbucks Vietnam"
    },
    "The Coffee House": {
        "wikidata": "Q60775742",
        "website": "https://www.thecoffeehouse.vn",
        "legalName_vi": "The Coffee House"
    },
    "Phở 24": {
        "wikidata": "Q65088019",
        "website": "https://www.pho24.com.vn",
        "legalName_vi": "Phở 24"
    },
    "Lotteria": {
        "wikidata": "Q249525",
        "website": "https://www.lotteria.vn",
        "legalName_en": "Lotteria Vietnam"
    },
    "KFC": {
        "wikidata": "Q524757",
        "website": "https://kfcvietnam.com.vn",
        "legalName_en": "KFC Vietnam"
    },
    
    # === AUTOMOTIVE ===
    "VinFast": {
        "wikidata": "Q56660561",
        "website": "https://vinfastauto.com",
        "legalName_vi": "VinFast",
        "legalName_en": "VinFast"
    },
    
    # === ELECTRONICS & RETAIL ===
    "Thế Giới Di Động": {
        "wikidata": "Q61739190",
        "website": "https://www.thegioididong.com",
        "legalName_vi": "Công ty Cổ phần Đầu tư Thế Giới Di Động"
    },
    "FPT Shop": {
        "wikidata": "Q5423418",
        "website": "https://fptshop.com.vn",
        "legalName_vi": "FPT Shop"
    }
}


def fetch_osm_data(osm_key: str, osm_value: str, area_name: str = "Hanoi") -> List[Dict[str, Any]]:
    """
    Fetch OSM data from Overpass API with retry mechanism
    Uses bounding box approach instead of named area search
    
    Args:
        osm_key: OSM key (e.g., "amenity")
        osm_value: OSM value (e.g., "atm")
        area_name: Area name to search in (default: "Hanoi")
    
    Returns:
        List of OSM elements (nodes, ways, relations)
    
    Raises:
        OverpassAPIError: If API request fails after retries
    """
    
    # Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Hà Nội bounding boxes (chia thành 9 ô 3x3)
    LAT_MIN, LAT_MAX = 20.9, 21.2
    LON_MIN, LON_MAX = 105.7, 106.0
    
    N_LAT, N_LON = 3, 3
    lat_step = (LAT_MAX - LAT_MIN) / N_LAT
    lon_step = (LON_MAX - LON_MIN) / N_LON
    
    # Tạo danh sách 9 bbox
    bboxes = []
    for i in range(N_LAT):
        for j in range(N_LON):
            bbox = (
                LAT_MIN + i * lat_step,
                LON_MIN + j * lon_step,
                LAT_MIN + (i + 1) * lat_step,
                LON_MIN + (j + 1) * lon_step
            )
            bboxes.append(bbox)
    
    # Collect all elements from all bboxes
    all_elements = []
    seen = set()  # Để tránh trùng lặp
    
    print(f"🔍 Fetching {osm_key}={osm_value} from {len(bboxes)} bounding boxes...")
    
    for bbox_idx, bbox in enumerate(bboxes, 1):
        bbox_str = f"({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]})"
        
        # Build Overpass QL query for this bbox
        overpass_query = f"""
[out:json][timeout:120];
(
  node["{osm_key}"="{osm_value}"]{bbox_str};
  way["{osm_key}"="{osm_value}"]{bbox_str};
  relation["{osm_key}"="{osm_value}"]{bbox_str};
);
out center;
"""
        
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                if bbox_idx == 1 and attempt == 0:
                    print(f"  Bbox {bbox_idx}/{len(bboxes)}: {bbox_str}")
                elif attempt > 0:
                    print(f"  Bbox {bbox_idx}/{len(bboxes)}: Retry {attempt + 1}/{max_retries}")
                
                # Make the API request
                response = requests.post(
                    overpass_url,
                    data={'data': overpass_query},
                    timeout=120
                )
                
                # Check for rate limiting (HTTP 429)
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        print(f"    ⚠ Rate limit (HTTP 429). Waiting {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    else:
                        print(f"    ⚠ Skipping bbox {bbox_idx} due to rate limit")
                        break
                
                # Check for other HTTP errors
                if response.status_code != 200:
                    print(f"    ⚠ HTTP {response.status_code}, skipping bbox")
                    break
                
                # Parse JSON response
                try:
                    data = response.json()
                except json.JSONDecodeError as e:
                    print(f"    ⚠ Invalid JSON, skipping bbox")
                    break
                
                # Extract elements and avoid duplicates
                elements = data.get('elements', [])
                for el in elements:
                    key = (el['type'], el['id'])
                    if key not in seen:
                        seen.add(key)
                        all_elements.append(el)
                
                # Success - move to next bbox
                if bbox_idx % 3 == 0 or bbox_idx == len(bboxes):
                    print(f"  Progress: {bbox_idx}/{len(bboxes)} boxes, {len(all_elements)} unique elements")
                
                break  # Exit retry loop
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"    ⚠ Timeout. Retrying...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"    ⚠ Skipping bbox {bbox_idx} due to timeout")
                    break
            
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"    ⚠ Network error. Retrying...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"    ⚠ Skipping bbox {bbox_idx} due to network error")
                    break
        
        # Small delay between bboxes to avoid rate limiting
        if bbox_idx < len(bboxes):
            time.sleep(1)
    
    print(f"✓ Successfully fetched {len(all_elements)} unique elements for {osm_key}={osm_value}")
    return all_elements


def enrich_with_wikidata(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enrich OSM elements with Wikidata information (labels and descriptions)
    
    Args:
        elements: List of OSM elements
    
    Returns:
        Enriched elements with multilingual_labels and multilingual_descriptions
    """
    enriched_elements = []
    
    for element in elements:
        enriched = element.copy()
        
        # Extract wikidata ID
        wikidata_id = element.get('tags', {}).get('wikidata')
        
        if wikidata_id:
            try:
                # Fetch Wikidata entity
                wikidata_url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
                response = requests.get(wikidata_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    entity = data.get('entities', {}).get(wikidata_id, {})
                    
                    # Extract multilingual labels
                    labels = entity.get('labels', {})
                    enriched['multilingual_labels'] = {
                        lang: label['value'] 
                        for lang, label in labels.items()
                    }
                    
                    # Extract multilingual descriptions
                    descriptions = entity.get('descriptions', {})
                    enriched['multilingual_descriptions'] = {
                        lang: desc['value'] 
                        for lang, desc in descriptions.items()
                    }
                    
            except Exception as e:
                print(f"Warning: Could not fetch Wikidata for {wikidata_id}: {e}")
        
        enriched_elements.append(enriched)
    
    return enriched_elements


def process_amenity_data(
    category_name: str,
    osm_key: str,
    osm_value: str,
    schema_type: str,
    output_dir: str = "datav2",
    area_name: str = "Hanoi"
) -> List[Dict[str, Any]]:
    """
    Complete pipeline: fetch, enrich, and save OSM data as RDF/Turtle
    
    Args:
        category_name: Name for the output file (e.g., "atm")
        osm_key: OSM key (e.g., "amenity")
        osm_value: OSM value (e.g., "atm")
        schema_type: Schema.org type (e.g., "schema:FinancialService")
        output_dir: Output directory for Turtle files
        area_name: Area name to search in
    
    Returns:
        List of enriched elements
    """
    
    # Step 1: Fetch data from Overpass API
    elements = fetch_osm_data(osm_key, osm_value, area_name)
    
    if not elements:
        print(f"No data found for {osm_key}={osm_value}")
        return []
    
    # Step 2: Enrich with Wikidata (if available)
    enriched_elements = enrich_with_wikidata(elements)
    
    # Step 3: Convert to RDF/Turtle
    output_path = Path(output_dir) / f"data_{area_name.lower()}_{category_name}.ttl"
    write_turtle_file(enriched_elements, output_path, category_name, schema_type)
    
    return enriched_elements


def remove_vietnamese_accents(text: str) -> str:
    """
    Remove Vietnamese accents from text for generating English names
    
    Args:
        text: Vietnamese text with accents
    
    Returns:
        Text without Vietnamese accents
    """
    if not text:
        return text
    
    # Vietnamese accent mapping
    accent_map = {
        'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'đ': 'd',
        'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'Ă': 'A', 'Ắ': 'A', 'Ằ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
        'Â': 'A', 'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
        'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
        'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
        'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
        'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
        'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
        'Ơ': 'O', 'Ớ': 'O', 'Ờ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
        'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
        'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
        'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
        'Đ': 'D'
    }
    
    result = []
    for char in text:
        result.append(accent_map.get(char, char))
    return ''.join(result)


def enrich_from_brand_knowledge(tags: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich element data using the Brand Knowledge Base
    
    This function automatically fills in missing Wikidata IDs, websites, legal names,
    and images based on the brand/operator tag if it matches a known brand.
    
    Args:
        tags: OSM tags dictionary
    
    Returns:
        Dictionary with enriched data (wikidata, website, legalName_vi, legalName_en, image)
    """
    enrichment = {
        'wikidata': None,
        'website': None,
        'legalName_vi': None,
        'legalName_en': None,
        'image': None
    }
    
    # Try to find brand in tags
    brand = tags.get('brand', '').strip()
    if not brand:
        brand = tags.get('operator', '').strip()
    
    if not brand:
        return enrichment
    
    # Check if brand exists in knowledge base
    # Try exact match first
    if brand in BRAND_KNOWLEDGE_BASE:
        kb_entry = BRAND_KNOWLEDGE_BASE[brand]
        enrichment['wikidata'] = kb_entry.get('wikidata')
        enrichment['website'] = kb_entry.get('website')
        enrichment['legalName_vi'] = kb_entry.get('legalName_vi')
        enrichment['legalName_en'] = kb_entry.get('legalName_en')
        enrichment['image'] = kb_entry.get('image')
        
        print(f"    [ENRICHMENT] Brand '{brand}' found in Knowledge Base!")
        return enrichment
    
    # Try case-insensitive partial match
    brand_lower = brand.lower()
    for kb_brand, kb_entry in BRAND_KNOWLEDGE_BASE.items():
        if kb_brand.lower() in brand_lower or brand_lower in kb_brand.lower():
            enrichment['wikidata'] = kb_entry.get('wikidata')
            enrichment['website'] = kb_entry.get('website')
            enrichment['legalName_vi'] = kb_entry.get('legalName_vi')
            enrichment['legalName_en'] = kb_entry.get('legalName_en')
            enrichment['image'] = kb_entry.get('image')
            
            print(f"    [ENRICHMENT] Brand '{brand}' matched with '{kb_brand}' in Knowledge Base!")
            return enrichment
    
    return enrichment


def generate_bilingual_names(tags: Dict[str, Any], category_name: str) -> tuple:
    """
    Generate bilingual names (Vietnamese and English) with smart fallback logic
    
    Args:
        tags: OSM tags dictionary
        category_name: Category name for generic fallback
    
    Returns:
        Tuple of (name_vi, name_en)
    """
    
    # Type mapping for generic names
    TYPE_MAPPING = {
        "atm": {"vi": "Trạm ATM", "en": "ATM"},
        "fuel_station": {"vi": "Trạm xăng", "en": "Gas Station"},
        "school": {"vi": "Trường học", "en": "School"},
        "hospital": {"vi": "Bệnh viện", "en": "Hospital"},
        "bus_stop": {"vi": "Trạm xe buýt", "en": "Bus Stop"},
        "playground": {"vi": "Sân chơi", "en": "Playground"},
        "toilets": {"vi": "Nhà vệ sinh", "en": "Toilet"},
        "drinking_water": {"vi": "Nước uống", "en": "Drinking Water"},
        "pharmacy": {"vi": "Hiệu thuốc", "en": "Pharmacy"},
        "restaurant": {"vi": "Nhà hàng", "en": "Restaurant"},
        "cafe": {"vi": "Quán cà phê", "en": "Cafe"},
        "bank": {"vi": "Ngân hàng", "en": "Bank"},
        "police": {"vi": "Đồn công an", "en": "Police Station"},
        "post_office": {"vi": "Bưu điện", "en": "Post Office"},
        "library": {"vi": "Thư viện", "en": "Library"},
        "parking": {"vi": "Bãi đỗ xe", "en": "Parking"},
        "bicycle_parking": {"vi": "Bãi đỗ xe đạp", "en": "Bicycle Parking"},
        "taxi": {"vi": "Điểm taxi", "en": "Taxi Stand"},
        "charging_station": {"vi": "Trạm sạc xe", "en": "Charging Station"},
        "clinic": {"vi": "Phòng khám", "en": "Clinic"},
        "dentist": {"vi": "Nha khoa", "en": "Dentist"},
        "kindergarten": {"vi": "Mẫu giáo", "en": "Kindergarten"},
        "university": {"vi": "Đại học", "en": "University"},
        "college": {"vi": "Cao đẳng", "en": "College"},
        "market": {"vi": "Chợ", "en": "Market"},
        "supermarket": {"vi": "Siêu thị", "en": "Supermarket"}
    }
    
    # Vietnamese to English keyword translation
    KEYWORD_TRANSLATION = {
        "Trạm xăng": "Gas Station",
        "Trạm ATM": "ATM",
        "Bệnh viện": "Hospital",
        "Trường": "School",
        "Đại học": "University",
        "Nhà hàng": "Restaurant",
        "Quán": "Cafe",
        "Ngân hàng": "Bank",
        "Siêu thị": "Supermarket",
        "Chợ": "Market"
    }
    
    # Get generic names for this category
    generic = TYPE_MAPPING.get(category_name, {"vi": "Điểm", "en": "Point"})
    generic_vi = generic["vi"]
    generic_en = generic["en"]
    
    # Step A: Check for valid name tag
    name = tags.get('name', '').strip()
    name_vi_tag = tags.get('name:vi', '').strip()
    name_en_tag = tags.get('name:en', '').strip()
    
    # If we have explicit bilingual tags, use them
    if name_vi_tag and name_en_tag:
        return (name_vi_tag, name_en_tag)
    
    if name and name.lower() not in ['unknown', 'unnamed', '']:
        # Use the name as Vietnamese
        name_vi = name
        
        # Generate English name by translating keywords and removing accents
        name_en = name
        for vi_keyword, en_keyword in KEYWORD_TRANSLATION.items():
            name_en = name_en.replace(vi_keyword, en_keyword)
        name_en = remove_vietnamese_accents(name_en)
        
        # If we have name:en tag, prefer it
        if name_en_tag:
            name_en = name_en_tag
        
        return (name_vi, name_en)
    
    # Step B: Fallback to brand or operator
    brand = tags.get('brand', '').strip() or tags.get('operator', '').strip()
    if brand:
        name_vi = f"{generic_vi} {brand}"
        name_en = f"{brand} {generic_en}"
        return (name_vi, name_en)
    
    # Step C: Fallback to street address
    street = tags.get('addr:street', '').strip()
    if street:
        name_vi = f"{generic_vi} tại {street}"
        name_en = f"{generic_en} at {remove_vietnamese_accents(street)}"
        return (name_vi, name_en)
    
    # Step D: Last resort - use generic with OSM ID if available
    osm_id = tags.get('_osm_id', '')
    if osm_id:
        name_vi = f"{generic_vi} #{osm_id}"
        name_en = f"{generic_en} #{osm_id}"
    else:
        name_vi = generic_vi
        name_en = generic_en
    
    return (name_vi, name_en)


def write_turtle_file(
    elements: List[Dict[str, Any]],
    output_path: Path,
    category_name: str,
    schema_type: str
):
    """
    Write OSM elements to Turtle/RDF file with bilingual support and proper syntax
    
    Args:
        elements: List of OSM elements
        output_path: Path to output Turtle file
        category_name: Category name for URI generation
        schema_type: Schema.org type
    """
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write prefixes with correct namespace
        f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        f.write("@prefix schema: <http://schema.org/> .\n")
        f.write("@prefix geo: <http://www.opengis.net/ont/geosparql#> .\n")
        f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        f.write("@prefix ext: <http://opendatafithou.org/def/extension/> .\n")
        f.write("@prefix fiware: <https://smartdatamodels.org/dataModel.PointOfInterest/> .\n")
        f.write("\n")
        
        # Write each element
        for element in elements:
            osm_id = element.get('id')
            osm_type = element.get('type', 'node')
            tags = element.get('tags', {})
            
            # Get coordinates (handle both nodes and ways/relations)
            if osm_type == 'node':
                lat = element.get('lat')
                lon = element.get('lon')
            else:
                # For ways/relations, use center coordinates
                center = element.get('center', {})
                lat = center.get('lat')
                lon = center.get('lon')
            
            if not lat or not lon:
                continue
            
            # Add OSM ID to tags for fallback naming
            tags['_osm_id'] = osm_id
            
            # CRITICAL: Subject URI with angle brackets
            subject_uri = f"<urn:ngsi-ld:PointOfInterest:Hanoi:{category_name}:{osm_id}>"
            
            f.write(f"{subject_uri}\n")
            # Dual typing: FIWARE + Schema.org for maximum interoperability
            f.write(f"    a fiware:PointOfInterest, {schema_type} ;\n")
            f.write(f"    ext:osm_id \"{osm_id}\"^^xsd:integer ;\n")
            f.write(f"    ext:osm_type \"{osm_type}\" ;\n")
            
            # Generate bilingual names using smart naming algorithm
            name_vi, name_en = generate_bilingual_names(tags, category_name)
            f.write(f"    schema:name \"{escape_turtle_string(name_vi)}\"@vi ,\n")
            f.write(f"                \"{escape_turtle_string(name_en)}\"@en ;\n")
            
            # === BRAND-BASED ENRICHMENT (Auto-fill from Knowledge Base) ===
            # Enrich data using Brand Knowledge Base for famous Vietnamese brands
            brand_enrichment = enrich_from_brand_knowledge(tags)
            
            # === OFFICIAL/LEGAL NAMES (Priority: OSM tags > Brand KB) ===
            # Map official_name to schema:legalName with language tags
            off_name = tags.get('official_name', '').strip() or tags.get('official_name:vi', '').strip()
            if not off_name and brand_enrichment['legalName_vi']:
                # Use Brand KB if OSM tag is missing
                off_name = brand_enrichment['legalName_vi']
                print(f"    [ENRICHMENT] Using legal name (VI) from Brand KB")
            
            if off_name:
                f.write(f"    schema:legalName \"{escape_turtle_string(off_name)}\"@vi ;\n")
            
            off_name_en = tags.get('official_name:en', '').strip()
            if not off_name_en and brand_enrichment['legalName_en']:
                # Use Brand KB if OSM tag is missing
                off_name_en = brand_enrichment['legalName_en']
                print(f"    [ENRICHMENT] Using legal name (EN) from Brand KB")
            
            if off_name_en:
                f.write(f"    schema:legalName \"{escape_turtle_string(off_name_en)}\"@en ;\n")
            
            # === BRAND & OPERATOR (Use standard schema.org properties) ===
            if 'brand' in tags:
                f.write(f"    schema:brand \"{escape_turtle_string(tags['brand'])}\" ;\n")
            if 'operator' in tags:
                f.write(f"    schema:operator \"{escape_turtle_string(tags['operator'])}\" ;\n")
            
            # === ADDRESS (Structured address information) ===
            addr_housenumber = tags.get('addr:housenumber', '').strip()
            addr_street = tags.get('addr:street', '').strip()
            addr_district = tags.get('addr:district', '').strip()
            addr_city = tags.get('addr:city', '').strip()
            addr_postcode = tags.get('addr:postcode', '').strip()
            
            if addr_housenumber:
                f.write(f"    ext:addr_housenumber \"{escape_turtle_string(addr_housenumber)}\" ;\n")
            if addr_street:
                f.write(f"    ext:addr_street \"{escape_turtle_string(addr_street)}\" ;\n")
            if addr_district:
                f.write(f"    ext:addr_district \"{escape_turtle_string(addr_district)}\" ;\n")
            if addr_city:
                f.write(f"    ext:addr_city \"{escape_turtle_string(addr_city)}\" ;\n")
            if addr_postcode:
                f.write(f"    ext:addr_postcode \"{escape_turtle_string(addr_postcode)}\" ;\n")
            
            # === CONTACT INFORMATION ===
            # Phone/Contact
            phone = tags.get('phone', '').strip() or tags.get('contact:phone', '').strip()
            if phone:
                f.write(f"    schema:telephone \"{escape_turtle_string(phone)}\" ;\n")
            
            # Email
            email = tags.get('email', '').strip() or tags.get('contact:email', '').strip()
            if email:
                f.write(f"    schema:email \"{escape_turtle_string(email)}\" ;\n")
            
            # Opening hours
            if 'opening_hours' in tags:
                f.write(f"    schema:openingHours \"{escape_turtle_string(tags['opening_hours'])}\" ;\n")
            
            # --- LINKED DATA & EXTERNAL LINKS ---
            # Critical section for establishing connections to external knowledge bases
            # These links enable data integration, entity resolution, and semantic enrichment
            
            # 1. WIKIDATA LINK (Priority: OSM tags > Brand KB)
            # Maps OSM entities to Wikidata knowledge graph
            # Predicate: schema:sameAs (indicates identity equivalence)
            wikidata_id = tags.get('wikidata', '').strip()
            
            # If no Wikidata in OSM tags, try Brand Knowledge Base
            if not wikidata_id and brand_enrichment['wikidata']:
                wikidata_id = brand_enrichment['wikidata']
                print(f"    [ENRICHMENT] Using Wikidata ID from Brand KB: {wikidata_id}")
            
            if wikidata_id:
                # DEBUG: Track Wikidata links
                print(f"    [DEBUG] Found Wikidata ID for OSM {osm_type}/{osm_id}: {wikidata_id}")
                # Construct full Wikidata URI (e.g., Q1003180 -> http://www.wikidata.org/entity/Q1003180)
                wikidata_uri = f"http://www.wikidata.org/entity/{wikidata_id}"
                f.write(f"    schema:sameAs <{wikidata_uri}> ;\n")
                print(f"    [DEBUG] ✓ Written schema:sameAs <{wikidata_uri}>")
            else:
                # DEBUG: Track missing Wikidata
                if osm_id % 10 == 0:  # Sample 10% to avoid spam
                    print(f"    [DEBUG] ⚠ No Wikidata ID for OSM {osm_type}/{osm_id}")
            
            # 2. WEBSITE / OFFICIAL URL (Priority: OSM tags > Brand KB > Social media)
            # Check multiple possible OSM tags in order of preference
            # Predicate: schema:url (official website)
            website = tags.get('website', '').strip()
            if not website:
                website = tags.get('contact:website', '').strip()
            if not website:
                website = tags.get('url', '').strip()
            
            # If no website in OSM tags, try Brand Knowledge Base
            if not website and brand_enrichment['website']:
                website = brand_enrichment['website']
                print(f"    [ENRICHMENT] Using website from Brand KB: {website}")
            
            # Fallback to social media (Facebook, etc.)
            if not website:
                website = tags.get('facebook', '').strip()
                if website and not website.startswith('http'):
                    # Convert Facebook username to full URL
                    if '/' not in website:
                        website = f"https://www.facebook.com/{website}"
            
            if website:
                # Ensure URL is properly formatted with protocol
                if not website.startswith(('http://', 'https://', 'ftp://')):
                    website = 'http://' + website
                f.write(f"    schema:url <{website}> ;\n")
                if 'facebook.com' in website:
                    print(f"    [ENRICHMENT] Using Facebook URL as fallback: {website}")
            
            # 3. WIKIPEDIA ARTICLE (Human-Readable Reference)
            # Links to Wikipedia article for additional context
            # Predicate: rdfs:seeAlso (see also reference)
            wikipedia = tags.get('wikipedia', '').strip()
            if wikipedia:
                # Format: "language:Article_Title" (e.g., "vi:Ngân_hàng_Ngoại_thương")
                if ':' in wikipedia:
                    lang, article = wikipedia.split(':', 1)
                    # Construct Wikipedia URL
                    wiki_url = f"https://{lang}.wikipedia.org/wiki/{article}"
                    f.write(f"    rdfs:seeAlso <{wiki_url}> ;\n")
            
            # 4. IMAGE / PHOTO (Priority: OSM tags > Brand KB)
            # Links to image resources (photos, logos, etc.)
            # Predicate: schema:image
            image = tags.get('image', '').strip()
            if not image:
                image = tags.get('image:url', '').strip()
            
            # If no image in OSM tags, try Brand Knowledge Base
            if not image and brand_enrichment['image']:
                image = brand_enrichment['image']
                print(f"    [ENRICHMENT] Using image from Brand KB: {image}")
            
            if image:
                if image.startswith(('http://', 'https://')):
                    # Full URL - use as URI
                    f.write(f"    schema:image <{image}> ;\n")
                else:
                    # Relative path or filename - use as literal
                    f.write(f"    schema:image \"{escape_turtle_string(image)}\" ;\n")
            
            # Multilingual labels (from Wikidata enrichment)
            if 'multilingual_labels' in element:
                for lang, label in element['multilingual_labels'].items():
                    f.write(f"    rdfs:label \"{escape_turtle_string(label)}\"@{lang} ;\n")
            
            # Multilingual descriptions (from Wikidata enrichment)
            if 'multilingual_descriptions' in element:
                for lang, desc in element['multilingual_descriptions'].items():
                    f.write(f"    schema:description \"{escape_turtle_string(desc)}\"@{lang} ;\n")
            
            # Geometry (WKT format)
            wkt = f"POINT({lon} {lat})"
            f.write(f"    geo:asWKT \"{wkt}\"^^geo:wktLiteral .\n")
            f.write("\n")
    
    print(f"✓ Saved {len(elements)} elements to {output_path}")


def escape_turtle_string(s: str) -> str:
    """
    Escape special characters in Turtle strings
    
    Args:
        s: Input string
    
    Returns:
        Escaped string safe for Turtle format
    """
    if not isinstance(s, str):
        s = str(s)
    
    # Escape backslashes and quotes
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    
    return s


# Example usage
if __name__ == "__main__":
    # Test fetch
    elements = fetch_osm_data("amenity", "atm", "Hanoi")
    print(f"Fetched {len(elements)} ATMs in Hanoi")
    
    # Test full pipeline
    process_amenity_data("test_atm", "amenity", "atm", "schema:FinancialService")
