
"""
@File    : test_geocoding.py
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
import time
import requests

def test_reverse_geocode(lat: float, lon: float):
    """Test reverse geocoding with a sample coordinate."""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=vi"
        headers = {
            'User-Agent': 'OpenDataFitHou/1.0 (educational project)'
        }
        
        print(f"\nTesting coordinates: {lat}, {lon}")
        print(f"URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"\nFull response:")
        print(f"  Display name: {data.get('display_name')}")
        
        address = data.get('address', {})
        print(f"\nAddress components:")
        for key, value in address.items():
            print(f"  {key}: {value}")
        
        # Priority: road > suburb > district > city
        location_name = (
            address.get('road') or
            address.get('suburb') or
            address.get('district') or
            address.get('city') or
            address.get('town') or
            address.get('village')
        )
        
        print(f"\nExtracted location name: {location_name}")
        return location_name
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 80)
    print("Testing Nominatim Reverse Geocoding")
    print("=" * 80)
    
    # Test case 1: Bus stop (POINT(105.8061717 21.0023477))
    test_reverse_geocode(21.0023477, 105.8061717)
    
    time.sleep(1.5)  # Rate limiting
    
    # Test case 2: Waste basket (POINT(105.851378 21.0282315))
    test_reverse_geocode(21.0282315, 105.851378)
    
    time.sleep(1.5)
    
    # Test case 3: Parking (POINT(105.8456789 21.0234567))
    test_reverse_geocode(21.0234567, 105.8456789)
    
    print("\n" + "=" * 80)
    print("Test complete")
    print("=" * 80)
