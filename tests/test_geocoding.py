"""
Test script to verify reverse geocoding functionality.
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
