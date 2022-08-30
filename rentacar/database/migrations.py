
MIGRATIONS = ["""CREATE TABLE "cars" (
	"id"	INTEGER NOT NULL,
	"brand"	TEXT NOT NULL,
	"model"	TEXT NOT NULL,
	"year"	REAL NOT NULL,
	"doors"	INTEGER NOT NULL,
	"chassis_series"	TEXT NOT NULL UNIQUE,
	"registration_nr"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT));
""",
"""CREATE TABLE "clients" (
	"id"	INTEGER NOT NULL,
	"first_name"	TEXT NOT NULL,
	"last_name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"phone"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);""",
"""CREATE TABLE "bookings" (
	"id"	INTEGER NOT NULL,
	"start_date"	TEXT NOT NULL,
	"end_date"	TEXT NOT NULL,
	"client_id"	INTEGER NOT NULL,
	"car_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""]