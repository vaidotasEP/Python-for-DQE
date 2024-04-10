from dbconnection import DBConnection
from city import City
from route import Route


dbcon = DBConnection('cities.db')

A = City()
A.ask_name()
A.get_coordinates(dbcon)

B = City()
B.ask_name()
B.get_coordinates(dbcon)

route_ab = Route(A, B)
dist = route_ab.calculate_distance()

print(f"\nThe distance between {A.name} and {B.name} is %.2f km." % dist)

dbcon.close_db_connection()
