class Floor:
    """
    This class represents a floor in the house.
    """

    def __init__(self, level):
        self.level = level
        self.rooms = []

class Room:
    """
    This class represents a room in the house.
    """

    def __init__(self, area, room_name=None):
        self.room_name = room_name
        self.area = area
        self.devices = []

class Device:
    """
    This class represents a smart device in the house.
    """

    def __init__(self, id, device_type, supplier, model_name=None, room=None):
        self.id = id
        self.device_type = device_type
        self.supplier = supplier
        self.model_name = model_name
        self.room = room

    def is_sensor(self):
        return False

    def is_actuator(self):
        return False

    def get_device_type(self):
        return self.device_type

class Sensor(Device):
    """
    This class represents a sensor device in the house.
    """

    def __init__(self, device_id, device_type, supplier, model_name=None, room=None):
        super().__init__(device_id, device_type, supplier, model_name, room)
        self.measurements = []

    def is_sensor(self):
        return True

    def add_measurement(self, value, unit, timestamp):
        measurement = Measurement(self, timestamp, value, unit)
        self.measurements.append(measurement)
        return measurement

    def last_measurement(self):
        if self.measurements:
            return self.measurements[-1]
        return None

class Actuator(Device):
    """
    This class represents an actuator device in the house.
    """

    def __init__(self, device_id, device_type, supplier, model_name=None, room=None):
        super().__init__(device_id, device_type, supplier, model_name, room)
        self.state = False

    def is_actuator(self):
        return True

    def turn_on(self, value=None):
        self.state = True

    def turn_off(self):
        self.state = False

    def is_active(self):
        return self.state

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, sensor, timestamp, value, unit):
        self.sensor = sensor
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def __init__(self):
        self.floors = []

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        floor = Floor(level)
        self.floors.append(floor)
        return floor

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(room_size, room_name)
        floor.rooms.append(room)
        return room


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has
        registered a basement (level=0), a ground floor (level=1) and a first floor
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return sorted(self.floors, key=lambda f: f.level)


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        rooms = []
        for floor in self.floors:
            rooms.extend(floor.rooms)
        return rooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return sum(room.area for room in self.get_rooms())


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        if device.room is not None:
            device.room.devices.remove(device)
        device.room = room
        room.devices.append(device)


    def get_device_by_id(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        for room in self.get_rooms():
            for device in room.devices:
                if device.id == device_id:
                    return device
        return None
    
    def get_devices(self):
        """
        This method returns a list of all registered devices in the house.
        The resulting list has no particular order.
        """
        devices = []
        for room in self.get_rooms():
            devices.extend(room.devices)
        return devices

