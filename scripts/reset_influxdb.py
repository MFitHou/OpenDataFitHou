# -*- coding: utf-8 -*-
"""
@File    : reset_influxdb.py
@Project : OpenDataFitHou
@Date    : 2025-12-01
@Author  : MFitHou Team

Script để xóa tất cả dữ liệu trong InfluxDB bucket (reset clean slate)

Copyright (C) 2025 FITHOU
Licensed under GNU GPL v3.0
"""

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
from influxdb_client.client.delete_api import DeleteApi

# Load environment variables
load_dotenv()

# InfluxDB Configuration
INFLUX_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUXDB_TOKEN", "opendata_fithou_token_secret")
INFLUX_ORG = os.getenv("INFLUXDB_ORG", "opendata_fithou")
INFLUX_BUCKET = os.getenv("INFLUXDB_BUCKET", "smartcity")


def delete_all_data():
    """
    Xóa tất cả dữ liệu trong bucket để tránh type conflict.
    """
    try:
        print("=" * 80)
        print("🗑️  RESET INFLUXDB BUCKET")
        print("=" * 80)
        print(f"\nConnecting to: {INFLUX_URL}")
        print(f"Organization: {INFLUX_ORG}")
        print(f"Bucket: {INFLUX_BUCKET}")
        
        # Tạo client
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )
        
        # Tạo delete API
        delete_api = client.delete_api()
        
        # Xóa tất cả dữ liệu từ thời điểm cũ nhất đến hiện tại
        # InfluxDB yêu cầu start và stop time cho delete operation
        start = "1970-01-01T00:00:00Z"
        stop = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        measurements_to_delete = ["weather", "air_quality", "traffic", "flood"]
        
        print(f"\n🔄 Deleting data from {start} to {stop}...")
        
        for measurement in measurements_to_delete:
            print(f"   Deleting measurement: {measurement}...", end="")
            try:
                delete_api.delete(
                    start=start,
                    stop=stop,
                    predicate=f'_measurement="{measurement}"',
                    bucket=INFLUX_BUCKET,
                    org=INFLUX_ORG
                )
                print(" ✅")
            except Exception as e:
                print(f" ⚠️  {e}")
        
        # Đóng client
        client.close()
        
        print("\n" + "=" * 80)
        print("✅ BUCKET RESET COMPLETE - Ready for fresh data")
        print("=" * 80)
        print("\nBây giờ bạn có thể chạy lại iot_collector.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error resetting bucket: {e}")
        return False


def main():
    """Entry point."""
    print("\n⚠️  WARNING: This will delete ALL data in the bucket!")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        delete_all_data()
    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    main()
