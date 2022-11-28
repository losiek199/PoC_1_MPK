# PoC_1_MPK

TASK DESCRIPTION
CSV files 

https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data

Tasks:

-Create a cities.csv files with the structure and data in the picture above.
-Create a python backend app that import the routes.csv and cities.csv data into tables in SQLite database file.
-By using Flask implement two REST endpoints that return in json format a list of cities and routes for a given city respectively.




###
TODO:
1. Create project
2. start project files
3. write code to download data from endpoint: https://www.wroclaw.pl/open-data/dataset/rozkladjazdytransportupublicznegoplik_data
4. create local database client (PostgresSQL)
5. write proces to load data into db 
5a. write pipeline to load data into db and prepare needed transformations
6. Create REST Endpoints that returns all enpoints in JSON format list 
