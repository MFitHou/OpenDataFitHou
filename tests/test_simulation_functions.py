# -*- coding: utf-8 -*-
"""
@File    : test_simulation_functions.py
@Project : OpenDataFitHou
@Date    : 2025-11-30
@Author  : MFitHou Team

Script để test các hàm mô phỏng: simulate_traffic_flow, simulate_noise_level, simulate_flood_depth

Copyright (C) 2025 FITHOU
Licensed under GNU GPL v3.0
"""

from iot_collector import simulate_traffic_flow, simulate_noise_level, simulate_flood_depth


def test_traffic_flow():
    """Test hàm simulate_traffic_flow với các giờ khác nhau."""
    print("=" * 70)
    print("🚗 TEST 1: simulate_traffic_flow(current_hour)")
    print("=" * 70)
    
    test_hours = [
        (7, "Rush Hour Morning"),
        (8, "Rush Hour Morning"),
        (12, "Normal Day"),
        (15, "Normal Day"),
        (18, "Rush Hour Evening"),
        (22, "Night"),
        (2, "Night")
    ]
    
    for hour, description in test_hours:
        intensity, speed = simulate_traffic_flow(hour)
        print(f"  {hour:02d}:00 ({description:20s}) → Intensity: {intensity:3d}, Speed: {speed:2d} km/h")
    
    print()


def test_noise_level():
    """Test hàm simulate_noise_level với các mức độ giao thông khác nhau."""
    print("=" * 70)
    print("🔊 TEST 2: simulate_noise_level(traffic_intensity)")
    print("=" * 70)
    
    test_intensities = [10, 30, 50, 70, 90, 95]
    
    for intensity in test_intensities:
        noise = simulate_noise_level(intensity)
        print(f"  Traffic Intensity: {intensity:3d} → Noise Level: {noise:5.1f} dB")
    
    print()


def test_flood_depth():
    """Test hàm simulate_flood_depth với các tình huống mưa khác nhau."""
    print("=" * 70)
    print("💧 TEST 3: simulate_flood_depth(rain_1h, current_level)")
    print("=" * 70)
    
    test_scenarios = [
        (0.5, 10.0, "No Rain - Drainage"),
        (1.5, 15.0, "Light Rain - Drainage"),
        (5.0, 20.0, "Medium Rain - Stable"),
        (12.0, 25.0, "Heavy Rain - Rising"),
        (20.0, 30.0, "Very Heavy Rain - Rising"),
        (0.0, 5.0, "No Rain - Draining to 0"),
        (15.0, 95.0, "Heavy Rain - Capped at 100"),
    ]
    
    for rain, current, description in test_scenarios:
        new_level = simulate_flood_depth(rain, current)
        change = new_level - current
        sign = "+" if change >= 0 else ""
        print(f"  Rain: {rain:5.1f}mm, Current: {current:5.1f}cm → New: {new_level:5.1f}cm ({sign}{change:.1f}) | {description}")
    
    print()


def test_integrated_scenario():
    """Test tích hợp: mô phỏng 1 ngày hoạt động."""
    print("=" * 70)
    print("🌆 TEST 4: Integrated Scenario - 24h Simulation")
    print("=" * 70)
    
    flood_level = 0.0  # Bắt đầu từ 0 cm
    rain_scenarios = [0.5] * 6 + [1.0] * 3 + [5.0] * 6 + [15.0] * 3 + [8.0] * 3 + [2.0] * 3
    
    print(f"{'Hour':>4} | {'Rain':>6} | {'Traffic':>7} | {'Speed':>6} | {'Noise':>6} | {'Flood':>6}")
    print("-" * 70)
    
    for hour in range(24):
        # Traffic simulation
        intensity, speed = simulate_traffic_flow(hour)
        
        # Noise simulation
        noise = simulate_noise_level(intensity)
        
        # Flood simulation
        rain = rain_scenarios[hour] if hour < len(rain_scenarios) else 1.0
        flood_level = simulate_flood_depth(rain, flood_level)
        
        print(f"{hour:2d}:00 | {rain:5.1f}mm | {intensity:3d}/100 | {speed:3d}km/h | {noise:5.1f}dB | {flood_level:5.1f}cm")
    
    print()


def main():
    """Entry point."""
    print("\n🧪 TESTING SIMULATION FUNCTIONS\n")
    
    test_traffic_flow()
    test_noise_level()
    test_flood_depth()
    test_integrated_scenario()
    
    print("=" * 70)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
