import sqlite3
from dataclasses import dataclass
from rentacar.database.car import Car
from rentacar.database.client import Client

@dataclass
class BookingCreateData:
    start_date: int
    end_date: int
    client_id: int
    car_id: int 

@dataclass
class Booking:
    id: int
    start_date: int
    end_date: int
    first_name: str
    last_name: str
    phone: int
    email: str
    brand: str
    model: str
    registration_nr: int      


class BookingDatabase:

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def book_car(self, data: BookingCreateData) -> None:
        """adauga in baza de date o rezervare noua."""
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO bookings (start_date, end_date, client_id, car_id) 
            VALUES (?, ?, ?, ?);
            """, (data.start_date, data.end_date, data.client_id, data.car_id))
        self._connection.commit()

    # verifica daca o masina e rezervata pt o anumita perioada, daca exista un row at. masina e ocupata.
    def is_car_booked(self, car_id: int, start_date: str, end_date: str) -> bool:
        cursor = self._connection.cursor()
        result = cursor.execute("""
        SELECT id FROM bookings WHERE car_id = ? AND start_date <= ? AND end_date >=?;""", (car_id, start_date, end_date))
        rows = result.fetchall() 
        if len(rows ) == 0:
            return False
        else:
            return True   

    def view_bookings(self) -> list[Booking]:
        cursor = self._connection.cursor()
        result = cursor.execute("""
        SELECT 
            bookings.id,
            bookings.start_date, 
            bookings.end_date, 
            clients.first_name, 
            clients.last_name, 
            clients.phone, 
            clients.email,
            cars.brand, 
            cars.model, 
            cars.registration_nr 
        FROM bookings 
        JOIN clients ON clients.id = bookings.client_id 
        JOIN cars ON cars.id = bookings.car_id;""")
        rows = result.fetchall()
        return [Booking(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]          
        