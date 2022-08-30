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

    # metoda privata, care listeaza toate rezervarile pt un nr de inamtriculare sau daca nu primeste nr de inmatriculare
    # listeaza toate rezervarile.
    def _view_bookings(self, registration_nr: str | None) -> list[Booking]:
        where = ""
        params = ()
        if registration_nr is not None:
            where = "WHERE cars.registration_nr = ?"
            params = (registration_nr,)
        cursor = self._connection.cursor()
        result = cursor.execute(f"""
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
        JOIN cars ON cars.id = bookings.car_id
        {where};""", params)
        rows = result.fetchall()
        return [Booking(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows] 

    # doua metode publice, una listeaza rezervarile pt un nr de inmatriculare si cealalta listeaza toate rez. existente.
    def view_bookings_for_car_for_registration_nr(self, registration_nr: str) -> list[Booking]: 
        return self._view_bookings(registration_nr)

    def view_bookings(self) -> list[Booking]:
        return self._view_bookings(None)
        
    def cancel_booking(self, booking_id: int):
        cursor = self._connection.cursor()
        cursor.execute("""DELETE FROM bookings WHERE id = ?;""", (booking_id,))
        self._connection.commit()
        
        