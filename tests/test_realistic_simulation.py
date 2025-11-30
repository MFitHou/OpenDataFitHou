# -*- coding: utf-8 -*-
"""
@File    : test_realistic_simulation.py
@Project : OpenDataFitHou
@Date    : 2025-11-30
@Author  : MFitHou Team

Script test mô phỏng thực tế với 10 trạm quan trắc và logic theo địa điểm cụ thể

Copyright (C) 2025 FITHOU
Licensed under GNU GPL v3.0
"""

from iot_collector import (
    STATIONS, 
    STATION_FLOOD_STATES,
    simulate_traffic_flow, 
    simulate_noise_level, 
    simulate_flood_depth
)


def test_station_configuration():
    """Kiểm tra cấu hình 10 trạm quan trắc."""
    print("=" * 80)
    print("📍 TEST 1: STATION CONFIGURATION (10 Monitoring Stations)")
    print("=" * 80)
    print(f"\nTotal Stations: {len(STATIONS)}")
    print(f"{'#':<3} {'Name':<20} {'Location':<25} {'Traffic':<8} {'Drainage':<8}")
    print("-" * 80)
    
    for idx, station in enumerate(STATIONS, 1):
        location = f"({station['lat']:.3f}, {station['lon']:.3f})"
        traffic = f"{station['traffic_factor']:.1f}x"
        drainage = f"{station['drainage_rate']:.1f}cm"
        print(f"{idx:<3} {station['name']:<20} {location:<25} {traffic:<8} {drainage:<8}")
    
    print()


def test_traffic_by_location():
    """Test logic giao thông theo địa điểm khác nhau."""
    print("=" * 80)
    print("🚗 TEST 2: TRAFFIC SIMULATION BY LOCATION (Rush Hour 8AM)")
    print("=" * 80)
    
    current_hour = 8  # Rush hour
    
    print(f"\nBase Time: {current_hour}:00 (Rush Hour)")
    print(f"{'Station':<20} {'Factor':<8} {'Intensity':<10} {'Speed':<10} {'Status':<15}")
    print("-" * 80)
    
    for station in STATIONS:
        intensity, speed = simulate_traffic_flow(current_hour, station['traffic_factor'])
        
        # Determine status
        if intensity >= 80:
            status = "🔴 Jam"
        elif intensity >= 60:
            status = "🟡 Congested"
        elif intensity >= 40:
            status = "🟢 Moderate"
        else:
            status = "⚪ Light"
        
        print(f"{station['name']:<20} {station['traffic_factor']:.1f}x     {intensity:3d}/100    {speed:3d}km/h    {status:<15}")
    
    print()


def test_traffic_across_day():
    """Test giao thông qua các giờ trong ngày cho 1 trạm điển hình."""
    print("=" * 80)
    print("⏰ TEST 3: TRAFFIC PATTERN ACROSS 24 HOURS (Trạm Ngã Tư Sở)")
    print("=" * 80)
    
    test_station = STATIONS[2]  # Ngã Tư Sở - Extreme traffic (factor 1.5)
    
    print(f"\nStation: {test_station['name']} (traffic_factor: {test_station['traffic_factor']}x)")
    print(f"{'Hour':<6} {'Period':<15} {'Intensity':<12} {'Speed':<12} {'Noise':<10}")
    print("-" * 80)
    
    periods = {
        range(0, 6): "Night",
        range(6, 9): "Rush Hour AM",
        range(9, 17): "Busy Day",
        range(17, 19): "Rush Hour PM",
        range(19, 23): "Evening"
    }
    
    for hour in range(24):
        period = next((name for hours, name in periods.items() if hour in hours), "Night")
        intensity, speed = simulate_traffic_flow(hour, test_station['traffic_factor'])
        noise = simulate_noise_level(intensity)
        
        print(f"{hour:02d}:00  {period:<15} {intensity:3d}/100      {speed:3d}km/h       {noise:5.1f}dB")
    
    print()


def test_flood_by_drainage():
    """Test ngập lụt theo khả năng thoát nước khác nhau."""
    print("=" * 80)
    print("💧 TEST 4: FLOOD SIMULATION BY DRAINAGE CAPABILITY")
    print("=" * 80)
    
    # Test scenarios
    rain_scenarios = [
        (0.0, "No Rain"),
        (5.0, "Light Rain"),
        (15.0, "Heavy Rain"),
        (25.0, "Very Heavy Rain")
    ]
    
    initial_level = 20.0  # Start với 20cm nước
    
    for rain_1h, description in rain_scenarios:
        print(f"\n{'='*80}")
        print(f"Scenario: {description} ({rain_1h}mm/h) | Initial Level: {initial_level:.1f}cm")
        print(f"{'='*80}")
        print(f"{'Station':<20} {'Drainage':<12} {'Water In':<12} {'Water Out':<12} {'New Level':<12} {'Change':<10}")
        print("-" * 80)
        
        for station in STATIONS:
            new_level = simulate_flood_depth(rain_1h, initial_level, station['drainage_rate'])
            water_in = rain_1h * 0.5
            water_out = station['drainage_rate']
            change = new_level - initial_level
            sign = "+" if change >= 0 else ""
            
            print(f"{station['name']:<20} {station['drainage_rate']:.1f}cm/cycle  {water_in:5.1f}cm      {water_out:5.1f}cm      {new_level:5.1f}cm      {sign}{change:.1f}cm")
    
    print()


def test_integrated_24h_simulation():
    """Test tích hợp: Mô phỏng 24h cho 3 trạm điển hình."""
    print("=" * 80)
    print("🌆 TEST 5: INTEGRATED 24H SIMULATION (3 Representative Stations)")
    print("=" * 80)
    
    # Chọn 3 trạm đại diện
    test_stations = [
        STATIONS[2],  # Ngã Tư Sở - Extreme traffic & poor drainage
        STATIONS[5],  # Hà Đông - Moderate traffic & drainage
        STATIONS[6],  # Long Biên - Light traffic & excellent drainage
    ]
    
    # Rain pattern trong 24h
    rain_pattern = (
        [0.5] * 6 +      # 0-5h: No rain
        [2.0] * 3 +      # 6-8h: Light rain
        [8.0] * 4 +      # 9-12h: Medium rain
        [18.0] * 3 +     # 13-15h: Heavy rain
        [12.0] * 2 +     # 16-17h: Medium rain
        [5.0] * 3 +      # 18-20h: Light rain
        [1.0] * 3        # 21-23h: Very light rain
    )
    
    # Initialize flood states
    flood_states = {station['id']: 0.0 for station in test_stations}
    
    for station in test_stations:
        print(f"\n{'='*80}")
        print(f"Station: {station['name']} (Traffic: {station['traffic_factor']}x, Drainage: {station['drainage_rate']}cm)")
        print(f"{'='*80}")
        print(f"{'Hour':<6} {'Rain':<8} {'Traffic':<10} {'Speed':<8} {'Noise':<8} {'Flood':<10}")
        print("-" * 80)
        
        for hour in range(24):
            rain = rain_pattern[hour]
            
            # Traffic & Noise
            intensity, speed = simulate_traffic_flow(hour, station['traffic_factor'])
            noise = simulate_noise_level(intensity)
            
            # Flood
            current_flood = flood_states[station['id']]
            new_flood = simulate_flood_depth(rain, current_flood, station['drainage_rate'])
            flood_states[station['id']] = new_flood
            
            print(f"{hour:02d}:00  {rain:5.1f}mm  {intensity:3d}/100   {speed:3d}km/h  {noise:5.1f}dB  {new_flood:5.1f}cm")
    
    print()


def test_comparison_extreme_vs_good():
    """So sánh 2 trạm đối lập: Ngã Tư Sở vs Long Biên."""
    print("=" * 80)
    print("⚖️  TEST 6: COMPARISON - EXTREME vs GOOD STATION")
    print("=" * 80)
    
    extreme_station = STATIONS[2]  # Ngã Tư Sở
    good_station = STATIONS[6]     # Long Biên
    
    print(f"\n🔴 Extreme: {extreme_station['name']} (Traffic {extreme_station['traffic_factor']}x, Drainage {extreme_station['drainage_rate']}cm)")
    print(f"🟢 Good:    {good_station['name']} (Traffic {good_station['traffic_factor']}x, Drainage {good_station['drainage_rate']}cm)")
    
    print(f"\n{'Metric':<25} {'Extreme (Ngã Tư Sở)':<25} {'Good (Long Biên)':<25}")
    print("-" * 80)
    
    # Rush Hour Traffic
    ext_intensity, ext_speed = simulate_traffic_flow(8, extreme_station['traffic_factor'])
    good_intensity, good_speed = simulate_traffic_flow(8, good_station['traffic_factor'])
    print(f"{'Rush Hour Intensity':<25} {ext_intensity:3d}/100                  {good_intensity:3d}/100")
    print(f"{'Rush Hour Speed':<25} {ext_speed:3d}km/h                  {good_speed:3d}km/h")
    
    # Noise
    ext_noise = simulate_noise_level(ext_intensity)
    good_noise = simulate_noise_level(good_intensity)
    print(f"{'Noise Level':<25} {ext_noise:5.1f}dB                  {good_noise:5.1f}dB")
    
    # Flood after heavy rain
    rain = 20.0
    ext_flood = simulate_flood_depth(rain, 10.0, extreme_station['drainage_rate'])
    good_flood = simulate_flood_depth(rain, 10.0, good_station['drainage_rate'])
    print(f"{'Flood (20mm rain)':<25} {ext_flood:5.1f}cm                  {good_flood:5.1f}cm")
    
    print()


def main():
    """Entry point."""
    print("\n" + "=" * 80)
    print("🧪 REALISTIC SIMULATION TEST - 10 MONITORING STATIONS")
    print("=" * 80 + "\n")
    
    test_station_configuration()
    test_traffic_by_location()
    test_traffic_across_day()
    test_flood_by_drainage()
    test_integrated_24h_simulation()
    test_comparison_extreme_vs_good()
    
    print("=" * 80)
    print("✅ ALL REALISTIC SIMULATION TESTS COMPLETED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
