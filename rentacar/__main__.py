import argparse
import sqlite3
from pathlib import Path
from rentacar.database.bookings import BookingCreateData, BookingDatabase
from rentacar.database.car import CarCreateData, ChassisOrRegistrationNrExists, CarDatabase
from rentacar.database.client import ClientCreateData, ClientDatabase, EmailExists


DB_FILE = Path(__file__).parent.parent/"rentacar.db"


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command",required=True)
    create_car_parser = subparsers.add_parser("create-car")
    create_car_parser.add_argument("--brand", required=True)
    create_car_parser.add_argument("--model", required=True )
    create_car_parser.add_argument("--year", required=True, type=int)
    create_car_parser.add_argument("--doors", required=True, type=int, help="Number of doors.")
    create_car_parser.add_argument("--chassis-series", required=True)
    create_car_parser.add_argument("--registration-nr", required=True)

    create_client_parser = subparsers.add_parser("create-client")
    create_client_parser.add_argument("--first-name", required=True)
    create_client_parser.add_argument("--last-name", required=True)
    create_client_parser.add_argument("--cnp", required=True, type=int)
    create_client_parser.add_argument("--address", required=True)
    create_client_parser.add_argument("--phone", required=True)
    create_client_parser.add_argument("--email", required=True)

    _ = subparsers.add_parser("list-clients")
    _ = subparsers.add_parser("list-cars")

    book_car_parser = subparsers.add_parser("book-car")
    book_car_parser.add_argument("--start-date", required=True)
    book_car_parser.add_argument("--end-date", required=True)
    book_car_parser.add_argument("--client-id", required=True, type=int)
    book_car_parser.add_argument("--car-id", required=True, type=int)

    _ = subparsers.add_parser("view-bookings")

    view_car_bookings_parser = subparsers.add_parser("view-car-bookings")
    view_car_bookings_parser.add_argument("--registration-nr", required=True)

    cancel_booking_parser = subparsers.add_parser("cancel-booking")
    cancel_booking_parser.add_argument("--booking-id", required=True, type=int)



    return parser.parse_args()


def main(): 
    with sqlite3.connect(DB_FILE) as connection:
        car_database = CarDatabase(connection)
        client_database = ClientDatabase(connection)
        booking_database = BookingDatabase(connection)
        args = parse_arguments()

        if args.command == "create-car":
            car_create_data = CarCreateData(args.brand, args.model, args.year, args.doors, args.chassis_series, args.registration_nr)
            try:   
                car_database.create_car(car_create_data)
            except ChassisOrRegistrationNrExists:
                print("Chassis or registration nr. already exists.")   
            else:
                print("Car successfully created.") 

        elif args.command == "create-client":
            client_create_data = ClientCreateData(args.first_name, args.last_name, args.cnp, args.address, args.phone, args.email)
            try:   
                client_database.create_client(client_create_data)
            except EmailExists:
                print("Email already already exists.")   
            else:
                print("Client successfully created.") 
             
        elif args.command == "list-clients":
            clients = client_database.list_clients()
            for client in clients:
                print(client.id, client.first_name, client.last_name, client.address, client.phone, client.email)

        elif args.command == "list-cars":
            cars = car_database.list_cars()
            for car in cars:
                print(car.id, car.brand, car.model, car.year, car.doors, car.chassis_series, car.registration_nr)
 
        elif args.command == "book-car": 
            if booking_database.is_car_booked(args.car_id, args.start_date, args.end_date):
                print("Car unavailable.")
            else:
                booking_create_data = BookingCreateData(args.start_date, args.end_date, args.client_id, args.car_id)
                booking_database.book_car(booking_create_data)
                print("Car booked.")    

        elif args.command == "view-bookings": 
            bookings = booking_database.view_bookings()
            for booking in bookings:
                print(booking.id, booking.start_date, booking.end_date, booking.first_name, booking.last_name, booking.phone, 
                booking.email, booking.brand, booking.model, booking.registration_nr)

           

        elif args.command == "view-car-bookings": 
            print("Lista rezervari")  
        elif args.command == "cancel-booking":  
            print("Rezervare anulata")      



if __name__ == "__main__": 
    main()          
