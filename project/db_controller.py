import sqlite3
import sqlalchemy
import pandas

conn = sqlite3.connect('mpk.db')
c = conn.cursor()

#Setting up database schema
#agency table
c.execute("""CREATE TABLE IF NOT EXISTS agency (
            agency_id INTEGER,
            agency_name TEXT,
            agency_url TEXT,
            agency_timezone TEXT,
            agency_phone TEXT,
            agency_lang TEXT
            )""")

#calendar table
c.execute("""CREATE TABLE IF NOT EXISTS calendar (
            service_id INTEGER,
            monday INTEGER,
            tuesday INTEGER,
            wednesday INTEGER,
            thursday INTEGER,
            friday INTEGER,
            saturday INTEGER,
            sunday INTEGER,
            start_date INTEGER,
            end_date INTEGER
            )""")

#calendar_dates table
c.execute("""CREATE TABLE IF NOT EXISTS calendar_dates (
            service_id INTEGER,
            date INTEGER,
            exception_type INTEGER
            )""")

#control_stops table
c.execute("""CREATE TABLE IF NOT EXISTS control_stops (
            variant_id INTEGER,
            stop_id INTEGER
            )""")

#feed_info table
c.execute("""CREATE TABLE IF NOT EXISTS feed_info (
            feed_publisher_name TEXT,
            feed_publisher_url TEXT,
            feed_lang TEXT,
            feed_start_date INTEGER,
            feed_end_date INTEGER
            )""")


#route_types table
c.execute("""CREATE TABLE IF NOT EXISTS route_types (
            route_type2_id INTEGER,
            route_type2_name TEXT
            )""")

#routes table
c.execute("""CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT,
            agency_id INTEGER,
            route_short_name TEXT,
            route_long_name TEXT,
            route_desc TEXT,
            route_type INTEGER,
            route_type2_id INTEGER,
            valid_from TEXT,
            valid_until TEXT
            )""")


#shapes table
c.execute("""CREATE TABLE IF NOT EXISTS shapes (
            shape_id INTEGER,
            shape_pt_lat REAL,
            shape_pt_lon REAL,
            shape_pt_sequence INTEGER
            )""")


#stop_times table
c.execute("""CREATE TABLE IF NOT EXISTS stop_times (
            trip_id TEXT
            arrival_time TEXT,
            departure_time TEXT,
            stop_id INTEGER,
            stop_sequence INTEGER,
            pickup_type INTEGER,
            drop_off_type INTEGER
            )""")

#stops table
c.execute("""CREATE TABLE IF NOT EXISTS stops (
            stop_id TEXT
            stop_code INTEGER,
            stop_name TEXT,
            stop_lat REAL,
            stop_lon REAL
            )""")

#trips table
c.execute("""CREATE TABLE IF NOT EXISTS trips (
            route_id INTEGER
            service_id INTEGER,
            trip_id TEXT,
            trip_headsign REAL,
            direction_id REAL
            )""")

#variants table
c.execute("""CREATE TABLE IF NOT EXISTS variants (
            variant_id INTEGER,
            is_main INTEGER,
            equiv_main_variant_id INTEGER,
            join_stop_id INTEGER,
            disjoin_stop_id INTEGER
            )""")

#vehicle_types table
c.execute("""CREATE TABLE IF NOT EXISTS vehicle_types (
            vehicle_type_id INTEGER,
            vehicle_type_name TEXT,
            vehicle_type_description TEXT,
            vehicle_type_symbol TEXT
            )""")

conn.commit()

def insert_data_row(table, data:tuple):
    pass

def truncate_load_table(table_name, source_path):
    #truncate table
    c.execute("DELETE FROM :table", {'table': table_name})
    conn.commit()
    print('Truncated table: ', table_name)
    #load table
    df = pandas.read_csv(source_path, header=1)
    df.to_sql(table_name, conn)
    print('Rows inserted: ',select_count_data(table_name))

def select_count_data(table):
    c.execute("SELECT COUNT(*) FROM ?", (table,))
    return c.fetchall()


def select_data(table, rows=1000):
    return c.execute("SELECT * FROM ?", (table,))

def delete_data(table, column_name, filter_expression):
    pass

def update_data(table, column_name, new_column_value, filter_expression):
    pass