"""
Configuration file for OpenStreetMap amenity types
Contains all POI categories to fetch for Hanoi Smart City
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
