import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Sensor, Actuator, Floor, Room

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        
        smarthouse = SmartHouse()
        cursor = self.cursor()

        # Query distinct floor levels and register them in the SmartHouse
        cursor.execute("SELECT DISTINCT floor FROM rooms ORDER BY floor")
        floors = {}
        for row in cursor.fetchall():
            floor = smarthouse.register_floor(row[0])
            floors[row[0]] = floor

        # Query all rooms, register each on its floor, and build a mapping from db id to Room object
        cursor.execute("SELECT id, floor, area, name FROM rooms")
        room_map = {}
        for row in cursor.fetchall():
            room_id, floor_level, area, name = row
            floor = floors[floor_level]
            room = smarthouse.register_room(floor, area, name)
            room.db_id = room_id  # store for later use in statistics methods
            room_map[room_id] = room
        
        # Query all devices, instantiate as Sensor or Actuator based on category, and register in their room
        cursor.execute("SELECT id, room, kind, category, supplier, product FROM devices")
        for row in cursor.fetchall():
            dev_id, room_id, kind, category, supplier, product = row
            if category == "sensor":
                device = Sensor(dev_id, kind, supplier, product)
            elif category == "actuator":
                device = Actuator(dev_id, kind, supplier, product)
            smarthouse.register_device(room_map[room_id], device)
        
        cursor.close()
        return smarthouse

    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        raise NotImplementedError


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.
        pass


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.
        raise NotImplementedError


    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement
        raise NotImplementedError
