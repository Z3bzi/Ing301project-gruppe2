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
        
        # --- NY KODE FOR Å LASTE AKTUATOR-STATUS ---
        # 1. Sjekk om tabellen i det hele tatt finnes (så det ikke kræsjer første gang)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='actuator_states'")
        if cursor.fetchone():
            # 2. Hent ut alle lagrede statuser
            cursor.execute("SELECT device, state FROM actuator_states")
            for row in cursor.fetchall():
                dev_id, state = row
                
                # Finn aktuatoren i systemet (hvis den finnes)
                device = smarthouse.get_device_by_id(dev_id)
                
                # Hvis den er lagret som 'på' (1), skru den på i Python
                if device and state == 1:
                    device.turn_on()
        
        cursor.close()
        return smarthouse

    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here. 
        # You will need to issue a SQL query that retrieves the most recent measurement for the given sensor, 
        # e.g. by using `ORDER BY timestamp DESC LIMIT 1`. 
        # Then you can instantiate a Measurement object with the retrieved data and return it. 
        # If there is no measurement for the given sensor, return None.

        # 1. Check if the given device is a sensor
        if not sensor.is_sensor():
            return None

        # 2. Get a cursor
        cursor = self.cursor()

        # 3. Write the SQL
        query = """
            SELECT ts, value, unit
            FROM measurements
            WHERE device = ?
            ORDER BY ts DESC
            LIMIT 1
        """

        # 4. Execute the query with the sensor's id as parameter and fetch the result
        cursor.execute(query, (sensor.id,))
        row = cursor.fetchone()
        
        cursor.close()

        # 5. If there is a result, create and return a Measurement object, otherwise return None
        if row:
            return Measurement(sensor, row[0], row[1], row[2])
        
        return None


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        cursor = self.cursor()

        # 1. Lag tabellen hvis den ikke finnes fra før
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actuator_states (
                device TEXT PRIMARY KEY,
                state BOOLEAN NOT NULL
            );
        """)

        # 2. Sett inn eller oppdater statusen. 
        # 'INSERT OR REPLACE' fungerer som en "Upsert" i SQLite.
        # Vi gjør om True/False til 1/0 for SQLite sin BOOLEAN-type.
        state_value = 1 if actuator.is_active() else 0
        
        cursor.execute("""
            INSERT OR REPLACE INTO actuator_states (device, state)
            VALUES (?, ?);
        """, (actuator.id, state_value))

        # 3. VIKTIGSTE STEG: Commit endringene!
        # Hvis vi ikke gjør dette, rulles alt tilbake når testen kaller reconnect()
        self.conn.commit()
        
        cursor.close()


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
        cursor = self.cursor()

        # SQL Code for calculating average temperatures per day in the given room and time range
        query = """
            SELECT DATE(ts) as dato, AVG(value) as snitt 
            FROM measurements
            WHERE device IN (
                SELECT id FROM devices
                WHERE room = ? AND (kind LIKE '%Temperature%' OR kind LIKE '%Heat Pump%')
            )
            AND unit = '°C'
            AND (? IS NULL OR DATE(ts) >= ?)
            AND (? IS NULL OR DATE(ts) <= ?)
            GROUP BY DATE(ts)
            ORDER BY DATE(ts);
        """

        
        params = (room.db_id, from_date, from_date, until_date, until_date)

        cursor.execute(query, params) # Execute the query with the parameters
        rows = cursor.fetchall() # Fetch all results and store in a variable.
        cursor.close()

        # Lag ordboken (Dictionary) som testen forventer
        result = {}
        for row in rows:
            dato_streng = row[0]
            gjennomsnitt = float(row[1]) # Gjør om til float
            result[dato_streng] = gjennomsnitt

        return result
    


    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        cursor = self.cursor()


        query = """
            SELECT CAST(strftime('%H', ts) AS INTEGER) AS hour
            FROM measurements
            WHERE device IN (
                SELECT id FROM devices
                WHERE room = ? AND kind LIKE '%Humidity%'
            )
            AND DATE(ts) = ?
            AND value > (
                SELECT AVG(value)
                FROM measurements
                WHERE device IN (
                    SELECT id FROM devices
                    WHERE room = ? AND kind LIKE '%Humidity%'
                )
                AND DATE(ts) = ?
            )
            GROUP BY hour
            HAVING COUNT(*) > 3
            ORDER BY hour;
        """

        # Vi sender inn room.db_id og date to ganger hver
        cursor.execute(query, (room.db_id, date, room.db_id, date))
        rows = cursor.fetchall()
        cursor.close()

        # Legg timene inn i en liste
        result = []
        for row in rows:
            result.append(row[0]) # row[0] er allerede et heltall pga CAST i SQL-en!

        return result
