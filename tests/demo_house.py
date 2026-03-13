from smarthouse.domain import SmartHouse, Sensor, Actuator

DEMO_HOUSE = SmartHouse()

# 1. floor: 6 rooms
ground_floor = DEMO_HOUSE.register_floor(1)
entrance     = DEMO_HOUSE.register_room(ground_floor, 13.5,  "Entrance")
living_room  = DEMO_HOUSE.register_room(ground_floor, 25.0,  "Living Room")
kitchen      = DEMO_HOUSE.register_room(ground_floor, 15.5,  "Kitchen")
bathroom_g   = DEMO_HOUSE.register_room(ground_floor,  8.0,  "Bathroom")
garage       = DEMO_HOUSE.register_room(ground_floor, 20.0,  "Garage")
utility      = DEMO_HOUSE.register_room(ground_floor, 10.0,  "Utility Room")

# 2. floor: 6 rooms
first_floor    = DEMO_HOUSE.register_floor(2)
master_bedroom = DEMO_HOUSE.register_room(first_floor, 18.0,  "Master Bedroom")
dressing_room  = DEMO_HOUSE.register_room(first_floor,  8.0,  "Dressing Room")
bedroom2       = DEMO_HOUSE.register_room(first_floor, 14.0,  "Bedroom 2")
bedroom3       = DEMO_HOUSE.register_room(first_floor, 12.0,  "Bedroom 3")
bathroom_f     = DEMO_HOUSE.register_room(first_floor,  7.55, "Bathroom")
office         = DEMO_HOUSE.register_room(first_floor,  5.0,  "Office")

# Devices

# entrance (1)
DEMO_HOUSE.register_device(entrance, Sensor("a1b2c3d4-0001-0001-0001-000000000001", "Door Sensor", "SecureHome", "DoorGuard 100"))

# living_room (3)
motion_sensor = Sensor("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", "Motion Sensor", "NebulaGuard Innovations", "MoveZ Detect 69")
DEMO_HOUSE.register_device(living_room, motion_sensor)
temp_sensor = Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e", "Temperature Sensor", "ClimateTech", "TempSense Pro")
temp_sensor.add_measurement(21.5, "°C", "2024-01-01T12:00:00")
DEMO_HOUSE.register_device(living_room, temp_sensor)
DEMO_HOUSE.register_device(living_room, Actuator("a1b2c3d4-0002-0002-0002-000000000002", "Smart TV", "MediaCorp", "Vision 55"))

# kitchen (2)
DEMO_HOUSE.register_device(kitchen, Sensor("a1b2c3d4-0003-0003-0003-000000000003", "Smoke Detector", "SafeGuard", "SmokeAlert X1"))
DEMO_HOUSE.register_device(kitchen, Actuator("a1b2c3d4-0004-0004-0004-000000000004", "Smart Oven", "KitchenPro", "OvenMaster 3000"))

# bathroom_g (1)
DEMO_HOUSE.register_device(bathroom_g, Sensor("a1b2c3d4-0005-0005-0005-000000000005", "Humidity Sensor", "ClimateTech", "HumidSense 200"))

# garage (1)
DEMO_HOUSE.register_device(garage, Actuator("a1b2c3d4-0006-0006-0006-000000000006", "Garage Door", "SecureHome", "AutoGate 500"))

# master_bedroom (2)
DEMO_HOUSE.register_device(master_bedroom, Actuator("5e13cabc-5c58-4bb3-82a2-3039e4480a6d", "Heat Pump", "ClimateControl", "HeatMaster 2000"))
DEMO_HOUSE.register_device(master_bedroom, Sensor("a1b2c3d4-0007-0007-0007-000000000007", "CO2 Sensor", "AirQuality Inc", "CO2Guard 300"))

# bedroom2 (1) — bulb is alone here so the move test works
DEMO_HOUSE.register_device(bedroom2, Actuator("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", "Light Bulp", "Elysian Tech", "Lumina Glow 4000"))

# bedroom3 (1)
DEMO_HOUSE.register_device(bedroom3, Actuator("a1b2c3d4-0008-0008-0008-000000000008", "Light Bulp", "Elysian Tech", "Lumina Glow 4000"))

# bathroom_f (1)
DEMO_HOUSE.register_device(bathroom_f, Sensor("a1b2c3d4-0009-0009-0009-000000000009", "Humidity Sensor", "ClimateTech", "HumidSense 200"))

# office (1)
DEMO_HOUSE.register_device(office, Sensor("a1b2c3d4-0010-0010-0010-000000000010", "Temperature Sensor", "ClimateTech", "TempSense Pro"))

