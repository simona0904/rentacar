from dataclasses import dataclass
import sqlite3


@dataclass
class CarCreateData:
    brand: str
    model: str
    year: int
    doors: int
    chassis_series: str
    registration_nr: int

@dataclass
class Car:
    id: int
    brand: str
    model: str
    year: int
    doors: int
    chassis_series: str
    registration_nr: int    

class ChassisOrRegistrationNrExists(Exception):
    pass    


class CarDatabase:

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def create_car(self, data: CarCreateData) -> None:
        """adauga in baza de date o masina noua."""
        cursor = self._connection.cursor()
        try:
            cursor.execute("""
            INSERT INTO cars (brand, model, year, doors, chassis_series, registration_nr) 
            VALUES (?, ?, ?, ?, ?, ?);
            """, (data.brand, data.model, data.year, data.doors, data.chassis_series, data.registration_nr))
            self._connection.commit()
        except sqlite3.IntegrityError:
            raise ChassisOrRegistrationNrExists()

    def list_cars(self) -> list[Car]:    
        cursor = self._connection.cursor()
        result = cursor.execute("""
        SELECT id, brand, model, year, doors, chassis_series, registration_nr FROM cars""")
        rows = result.fetchall()
        return [Car(row[0],row[1],row[2],row[3],row[4],row[5], row[6]) for row in rows]

                       
            
                  