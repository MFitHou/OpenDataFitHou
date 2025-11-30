# -*- coding: utf-8 -*-
"""
@File    : test_influxdb_connection.py
@Project : OpenDataFitHou
@Date    : 2025-11-30
@Author  : MFitHou Team

Script test kết nối InfluxDB và ghi dữ liệu thử nghiệm

Copyright (C) 2025 FITHOU
Licensed under GNU GPL v3.0
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Load environment variables
load_dotenv()

# InfluxDB Configuration
INFLUX_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUXDB_TOKEN", "opendata_fithou_token_secret")
INFLUX_ORG = os.getenv("INFLUXDB_ORG", "opendata_fithou")
INFLUX_BUCKET = os.getenv("INFLUXDB_BUCKET", "smartcity")


def test_connection():
    """Test kết nối đến InfluxDB."""
    print("=" * 80)
    print("🔌 TESTING INFLUXDB CONNECTION")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  URL: {INFLUX_URL}")
    print(f"  Org: {INFLUX_ORG}")
    print(f"  Bucket: {INFLUX_BUCKET}")
    print(f"  Token: {'*' * 20}... (hidden)")
    
    try:
        # Tạo client
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )
        
        # Test health check
        health = client.health()
        
        if health.status == "pass":
            print(f"\n✅ Connection successful!")
            print(f"   InfluxDB Status: {health.status}")
            print(f"   Message: {health.message}")
            client.close()
            return True
        else:
            print(f"\n❌ Connection failed!")
            print(f"   Status: {health.status}")
            client.close()
            return False
            
    except Exception as e:
        print(f"\n❌ Error connecting to InfluxDB:")
        print(f"   {e}")
        return False


def test_write_sample_data():
    """Test ghi dữ liệu mẫu vào InfluxDB."""
    print("\n" + "=" * 80)
    print("📝 TESTING WRITE SAMPLE DATA")
    print("=" * 80)
    
    try:
        # Tạo client
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )
        
        # Tạo write API
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # Tạo sample data points
        test_data = [
            {
                "measurement": "test_weather",
                "tags": {"station": "test_station_1", "location": "Hanoi"},
                "fields": {"temperature": 25.5, "humidity": 80, "wind_speed": 3.2}
            },
            {
                "measurement": "test_air_quality",
                "tags": {"station": "test_station_1", "location": "Hanoi"},
                "fields": {"pm25": 45.2, "pm10": 78.5, "aqi": 112}
            },
            {
                "measurement": "test_traffic",
                "tags": {"station": "test_station_1", "location": "Hanoi"},
                "fields": {"intensity": 75, "avg_speed": 25, "noise_level": 72.5}
            }
        ]
        
        print(f"\nWriting {len(test_data)} sample data points...\n")
        
        for idx, data in enumerate(test_data, 1):
            # Tạo Point
            point = Point(data["measurement"])
            
            # Thêm tags
            for tag_key, tag_value in data["tags"].items():
                point = point.tag(tag_key, tag_value)
            
            # Thêm fields
            for field_key, field_value in data["fields"].items():
                point = point.field(field_key, field_value)
            
            # Ghi vào InfluxDB
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
            
            print(f"  ✅ [{idx}] {data['measurement']}: {data['fields']}")
        
        print(f"\n✅ Successfully wrote {len(test_data)} data points to InfluxDB!")
        print(f"   Bucket: {INFLUX_BUCKET}")
        print(f"   Timestamp: {datetime.now().isoformat()}")
        
        # Đóng client
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error writing to InfluxDB:")
        print(f"   {e}")
        return False


def test_query_data():
    """Test đọc dữ liệu từ InfluxDB."""
    print("\n" + "=" * 80)
    print("🔍 TESTING QUERY DATA")
    print("=" * 80)
    
    try:
        # Tạo client
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )
        
        # Tạo query API
        query_api = client.query_api()
        
        # Flux query để lấy dữ liệu test
        query = f'''
        from(bucket: "{INFLUX_BUCKET}")
            |> range(start: -1h)
            |> filter(fn: (r) => r["_measurement"] =~ /^test_/)
            |> limit(n: 10)
        '''
        
        print(f"\nQuerying last 1 hour of test data...\n")
        
        # Thực hiện query
        tables = query_api.query(query, org=INFLUX_ORG)
        
        record_count = 0
        for table in tables:
            for record in table.records:
                record_count += 1
                measurement = record.get_measurement()
                field = record.get_field()
                value = record.get_value()
                time = record.get_time()
                
                print(f"  📊 {measurement}.{field} = {value} @ {time}")
        
        if record_count > 0:
            print(f"\n✅ Successfully queried {record_count} records from InfluxDB!")
        else:
            print(f"\n⚠️  No data found in the last hour.")
            print(f"   This is normal if you just started collecting data.")
        
        # Đóng client
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error querying from InfluxDB:")
        print(f"   {e}")
        return False


def main():
    """Entry point."""
    print("\n🧪 INFLUXDB CONNECTION & WRITE TEST\n")
    
    # Test 1: Connection
    connection_ok = test_connection()
    
    if not connection_ok:
        print("\n❌ Connection failed. Please check:")
        print("   1. Docker containers are running (docker compose up -d)")
        print("   2. InfluxDB is accessible at http://localhost:8086")
        print("   3. .env file has correct credentials")
        return
    
    # Test 2: Write sample data
    write_ok = test_write_sample_data()
    
    if not write_ok:
        print("\n❌ Write test failed. Skipping query test.")
        return
    
    # Test 3: Query data
    query_ok = test_query_data()
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 TEST SUMMARY")
    print("=" * 80)
    print(f"  Connection Test: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"  Write Test:      {'✅ PASS' if write_ok else '❌ FAIL'}")
    print(f"  Query Test:      {'✅ PASS' if query_ok else '❌ FAIL'}")
    print("=" * 80 + "\n")
    
    if connection_ok and write_ok and query_ok:
        print("🎉 All tests passed! InfluxDB is ready for production use.\n")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running production.\n")


if __name__ == "__main__":
    main()
