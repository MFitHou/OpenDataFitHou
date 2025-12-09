"""
 * Copyright (C) 2025 MFitHou
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

# Test OpenAQ V3 API - Following Official Documentation
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENAQ_API_KEY')
print(f"API Key loaded: {'Yes' if API_KEY else 'No'}")
print(f"Testing OpenAQ V3 API for Hanoi, Vietnam\n")

# Test 1: Search for locations near Hanoi
print("=== Step 1: Search locations near Hanoi ===")
url = "https://api.openaq.org/v3/locations"
params = {
    'limit': 3,
    'coordinates': '21.0285,105.8542',
    'radius': 25000  # Max 25km
}
headers = {'X-API-Key': API_KEY}

try:
    r = requests.get(url, params=params, headers=headers, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Results found: {len(data.get('results', []))}\n")
        
        if data.get('results'):
            for idx, loc in enumerate(data['results'][:3], 1):
                print(f"Location {idx}:")
                print(f"  ID: {loc.get('id')}")
                print(f"  Name: {loc.get('name')}")
                print(f"  Distance: {loc.get('distance', 0)/1000:.1f} km")
                print(f"  Parameters count: {len(loc.get('parameters', []))}")
                
            # Get detailed info for first location
            first_loc_id = data['results'][0]['id']
            print(f"\n=== Step 2: Get detailed data for location {first_loc_id} ===")
            
            r2 = requests.get(
                f"https://api.openaq.org/v3/locations/{first_loc_id}",
                headers=headers,
                timeout=30
            )
            
            if r2.status_code == 200:
                loc_detail = r2.json()
                print(f"Location: {loc_detail.get('name')}")
                print(f"\nParameters with latest data:")
                
                pm25_found = False
                pm10_found = False
                
                for param in loc_detail.get('parameters', []):
                    param_name = param.get('name', '')
                    param_id = param.get('id')
                    latest = param.get('latest', {})
                    
                    if 'pm' in param_name.lower():
                        value = latest.get('value')
                        datetime_str = latest.get('datetime', {}).get('utc', 'N/A')
                        print(f"  - {param_name} (ID: {param_id}): {value} µg/m³ @ {datetime_str}")
                        
                        if 'pm2.5' in param_name.lower() or 'pm25' in param_name.lower():
                            pm25_found = True
                        if 'pm10' in param_name.lower() and '2.5' not in param_name.lower():
                            pm10_found = True
                
                print(f"\n✅ PM2.5 data available: {pm25_found}")
                print(f"✅ PM10 data available: {pm10_found}")
            else:
                print(f"Error getting location details: {r2.status_code}")
                
    else:
        print(f"Error: {r.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")

# Test removed - focus on locations endpoint only
