
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
WIKIDATA_SPARQL_URL = os.getenv("WIKIDATA_SPARQL_URL", "https://query.wikidata.org/sparql")


def test_openweathermap():
    print("[OpenWeatherMap] Kiểm tra kết nối...")
    assert OPENWEATHER_API_KEY, "OPENWEATHER_API_KEY not set"
    url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={OPENWEATHER_API_KEY}"
    r = requests.get(url)
    assert r.status_code == 200, f"OpenWeatherMap failed: {r.text}"
    print("[OpenWeatherMap] Thành công!")

def test_openaq():
    print("[OpenAQ] Kiểm tra kết nối...")
    assert OPENAQ_API_KEY, "OPENAQ_API_KEY not set"
    url = "https://api.openaq.org/v3/locations"
    headers = {"x-api-key": OPENAQ_API_KEY}
    r = requests.get(url, headers=headers)
    assert r.status_code == 200, f"OpenAQ failed: {r.text}"
    print("[OpenAQ] Thành công!")

def test_overpass():
    print("[Overpass API] Kiểm tra kết nối...")
    headers = {"User-Agent": "OpenDataFitHou/1.0 (contact@example.com)"}
    r = requests.get(OVERPASS_URL, params={"data": "[out:json];node[amenity=school](50.6,7.0,50.8,7.3);out;"}, headers=headers)
    assert r.status_code == 200, f"Overpass failed: {r.text}"
    print("[Overpass API] Thành công!")

def test_wikidata_sparql():
    print("[Wikidata SPARQL] Kiểm tra kết nối...")
    query = "SELECT * WHERE { ?item wdt:P31 wd:Q3918. } LIMIT 1"
    r = requests.get(WIKIDATA_SPARQL_URL, params={"query": query, "format": "json"})
    assert r.status_code == 200, f"Wikidata SPARQL failed: {r.text}"
    print("[Wikidata SPARQL] Thành công!")

def test_gtfs():
    print("[GTFS] Kiểm tra tải dữ liệu mẫu...")
    url = "https://transitfeeds.com/p/mta/79/latest/download"
    r = requests.get(url, stream=True)
    assert r.status_code == 200, f"GTFS download failed: {r.text}"
    print("[GTFS] Thành công!")

if __name__ == "__main__":
    try:
        test_openweathermap()
        test_openaq()
        test_overpass()
        test_wikidata_sparql()
        test_gtfs()
        print("\n✅ Tất cả kết nối thành công!")
    except AssertionError as e:
        print(f"\n❌ Lỗi: {e}")
        exit(1)
    except Exception as ex:
        print(f"\n❌ Lỗi không xác định: {ex}")
        exit(2)
