class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



# TODO: Add your own classes here!

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

    def __init__(self, device_id, device_type, supplier, model=None, room=None):
        self.device_id = device_id
        self.device_type = device_type
        self.supplier = supplier
        self.model = model
        self.room = room
        self.isSensor = False
        self.isActuator = False

class Sensor(Device):
    """
    This class represents a sensor device in the house.
    """

    def __init__(self, device_id, device_type, supplier, model=None, room=None):
        super().__init__(device_id, device_type, supplier, model, room)
        self.measurements = []  # list of measurements produced by this sensor
        self.isSensor = True

    def add_measurement(self, value, unit, timestamp):
        """
        Create a new measurement and store it.
        """
        measurement = Measurement(self, timestamp, value, unit)
        self.measurements.append(measurement)
        return measurement

class Actuator(Device):
    """
    This class represents an actuator device in the house.
    """

    def __init__(self, device_id, device_type, supplier, model=None, room=None):
        super().__init__(device_id, device_type, supplier, model, room)
        self.state = False
        self.isActuator = True

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False

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

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        pass


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        pass


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        pass


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        pass

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass

