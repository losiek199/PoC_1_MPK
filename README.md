# PoC_1_MPK

TASK DESCRIPTION
CSV files 

https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data

Tasks:

-Create a cities.csv files with the structure and data in the picture above.
-Create a python backend app that import the routes.csv and cities.csv data into tables in SQLite database file.
-By using Flask implement two REST endpoints that return in json format a list of cities and routes for a given city respectively.


PoC 1.b: Trips Denormalization

Tasks:
By using the data from the MPK and the files: trips, stops, stops_times_vehicle_types; create a new denormalized file, trips_denorm which the attributes indicated in the diagram. The new file shall contains the following columns: trip_id, route_id, trip_headsign, arrival_time, stop_id, stop_code, stop_name, vehicle_type_id.
