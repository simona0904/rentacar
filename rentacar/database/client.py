from dataclasses import dataclass
import sqlite3


@dataclass
class ClientCreateData:
    first_name: str
    last_name: str
    cnp: int
    address: str
    phone: int
    email: str

@dataclass
class Client:
    id: int
    first_name: str
    last_name: str
    address: str
    phone: int
    email: str


class EmailExists(Exception):
    pass    

class ClientDatabase:

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def create_client(self, data: ClientCreateData) -> None:
        """adauga in baza de date un client nou."""
        cursor = self._connection.cursor()
        try:
            cursor.execute("""
            INSERT INTO clients (first_name, last_name, address, phone, email) 
            VALUES (?, ?, ?, ?, ?);
            """, (data.first_name, data.last_name, data.address, data.phone, data.email))
            self._connection.commit()
        except sqlite3.IntegrityError:
            raise EmailExists()  

    def list_clients(self) -> list[Client]:    
        cursor = self._connection.cursor()
        result = cursor.execute("""
        SELECT id, first_name, last_name, address, phone, email FROM clients""")
        rows = result.fetchall()
        return [Client(row[0],row[1],row[2],row[3],row[4],row[5]) for row in rows]

               