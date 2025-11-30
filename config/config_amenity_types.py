
"""
@File    : config_amenity_types.py
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

# Complete list of amenity types organized by category
AMENITY_TYPES = [
    # --- NHÓM TÀI CHÍNH & DỊCH VỤ CƠ BẢN ---
    ("atm", "amenity", "atm", "schema:FinancialService"),
    ("bank", "amenity", "bank", "schema:BankOrCreditUnion"),
    ("post_office", "amenity", "post_office", "schema:PostOffice"),

    # --- NHÓM GIAO THÔNG & VẬN TẢI ---
    ("bus_stop", "highway", "bus_stop", "schema:BusStop"),
    ("parking", "amenity", "parking", "schema:ParkingFacility"),
    ("fuel_station", "amenity", "fuel", "schema:GasStation"),
    ("charging_station", "amenity", "charging_station", "schema:AutomotiveBusiness"),

    # --- NHÓM Y TẾ & KHẨN CẤP ---
    ("hospital", "amenity", "hospital", "schema:Hospital"),
    ("clinic", "amenity", "clinic", "schema:MedicalClinic"),
    ("pharmacy", "amenity", "pharmacy", "schema:Pharmacy"),
    ("police", "amenity", "police", "schema:PoliceStation"),
    ("fire_station", "amenity", "fire_station", "schema:FireStation"),

    # --- NHÓM TIỆN ÍCH CÔNG CỘNG & VỆ SINH ---
    ("drinking_water", "amenity", "drinking_water", "schema:DrinkingWaterDispenser"),
    ("public_toilet", "amenity", "toilets", "schema:PublicToilet"),
    ("waste_basket", "amenity", "waste_basket", "schema:WasteContainer"),

    # --- NHÓM GIÁO DỤC ---
    ("school", "amenity", "school", "schema:School"),
    ("kindergarten", "amenity", "kindergarten", "schema:Preschool"),
    ("university", "amenity", "university", "schema:CollegeOrUniversity"),
    ("library", "amenity", "library", "schema:Library"),

    # --- NHÓM GIẢI TRÍ & CÔNG VIÊN ---
    ("park", "leisure", "park", "schema:Park"),
    ("playground", "leisure", "playground", "schema:Playground"),
    ("community_centre", "amenity", "community_centre", "schema:CommunityCenter"),

    # --- NHÓM MUA SẮM & THỰC PHẨM ---
    ("marketplace", "amenity", "marketplace", "schema:Market"),
    ("supermarket", "shop", "supermarket", "schema:GroceryStore"),
    ("convenience_store", "shop", "convenience", "schema:ConvenienceStore"),
    ("cafe", "amenity", "cafe", "schema:CafeOrCoffeeShop"),
    ("restaurant", "amenity", "restaurant", "schema:Restaurant"),

    # --- NHÓM HẠ TẦNG KHÁC ---
    ("warehouse", "building", "warehouse", "schema:Warehouse"),
]

# Batch configuration for processing
BATCH_CONFIG = {
    'delay_between_categories': 3,  # Seconds to wait between processing different categories
    'delay_between_api_calls': 2,   # Seconds to wait between Overpass API calls
    'max_retries': 3,                # Maximum retries for failed API calls
    'timeout': 120,                  # Request timeout in seconds
}
