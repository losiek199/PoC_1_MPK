import sqlalchemy as db
from sqlalchemy.orm import declarative_base
import pandas
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy as fsdb

#creating db connection and getting db metadata
eng = db.create_engine('sqlite:///mpk.db', echo=False)
connection = eng.connect()
meta = db.MetaData(bind=connection)
ins = db.inspect(eng)
Base = declarative_base()

#tables schemas:
cities = db.Table('cities', meta,
                          db.Column('city_id', db.Integer, primary_key=True),
                          db.Column('city_name', db.String)
                          )


logs = db.Table('logs', meta,
                        db.Column('row_id', db.Integer, primary_key=True),
                        db.Column('log_dt', db.String),
                        db.Column('action', db.String)
                        )

# agency table
agency = db.Table('agency', meta,
                          db.Column('agency_id', db.Integer),
                          db.Column('agency_name', db.String),
                          db.Column('agency_url', db.String),
                          db.Column('agency_timezone', db.String),
                          db.Column('agency_phone', db.String),
                          db.Column('agency_lang', db.String),
                          db.Column('city_id', db.Integer)
                          )

# calendar table
calendar = db.Table('calendar', meta,
                            db.Column('service_id', db.Integer),
                            db.Column('monday', db.Integer),
                            db.Column('tuesday', db.Integer),
                            db.Column('wednesday', db.Integer),
                            db.Column('thursday', db.Integer),
                            db.Column('friday', db.Integer),
                            db.Column('saturday', db.Integer),
                            db.Column('sunday', db.Integer),
                            db.Column('start_date', db.Integer),
                            db.Column('end_date', db.Integer),
                            db.Column('city_id', db.Integer)
                            )

# calendar_dates table
calendar_dates = db.Table('calendar_dates', meta,
                                  db.Column('service_id', db.Integer),
                                  db.Column('date', db.Integer),
                                  db.Column('exception_type', db.Integer),
                                  db.Column('city_id', db.Integer)
                                  )

# control_stops table
control_stops = db.Table('control_stops', meta,
                                 db.Column('variant_id', db.Integer),
                                 db.Column('stop_id', db.Integer),
                                 db.Column('city_id', db.Integer)
                                 )

# feed_info table
feed_info = db.Table('feed_info', meta,
                             db.Column('feed_publisher_name', db.String),
                             db.Column('feed_publisher_url', db.String),
                             db.Column('feed_lang', db.String),
                             db.Column('feed_start_date', db.Integer),
                             db.Column('feed_end_date', db.Integer),
                             db.Column('city_id', db.Integer)
                             )

# route_types table
route_types = db.Table('route_types', meta,
                               db.Column('route_type2_id', db.Integer),
                               db.Column('route_type2_name', db.String),
                               db.Column('city_id', db.Integer)
                               )

# routes table
routes = db.Table('routes', meta,
                          db.Column('route_id', db.String),
                          db.Column('agency_id', db.Integer),
                          db.Column('route_short_name', db.String),
                          db.Column('route_long_name', db.String),
                          db.Column('route_desc', db.String),
                          db.Column('route_type', db.Integer),
                          db.Column('route_type2_id', db.Integer),
                          db.Column('valid_from', db.String),
                          db.Column('valid_until', db.String),
                          db.Column('city_id', db.Integer)
                          )

# shapes table
shapes = db.Table('shapes', meta,
                          db.Column('shape_id', db.Integer),
                          db.Column('shape_pt_lat', db.Float),
                          db.Column('shape_pt_lon', db.Float),
                          db.Column('shape_pt_sequence', db.Integer),
                          db.Column('city_id', db.Integer)
                          )

# stop_times table
stop_times = db.Table('stop_times', meta,
                              db.Column('trip_id', db.String),
                              db.Column('arrival_time', db.String),
                              db.Column('departure_time', db.String),
                              db.Column('stop_id', db.Integer),
                              db.Column('stop_sequence', db.Integer),
                              db.Column('pickup_type', db.Integer),
                              db.Column('drop_off_type', db.Integer),
                              db.Column('city_id', db.Integer)
                              )

# stops table
stops = db.Table('stops', meta,
                         db.Column('stop_id', db.String),
                         db.Column('stop_code', db.Integer),
                         db.Column('stop_name', db.String),
                         db.Column('stop_lat', db.Float),
                         db.Column('stop_lon', db.Float),
                         db.Column('city_id', db.Integer)
                         )

# trips table
trips = db.Table('trips', meta,
                         db.Column('route_id', db.Integer),
                         db.Column('service_id', db.Integer),
                         db.Column('trip_id', db.String),
                         db.Column('trip_headsign', db.Float),
                         db.Column('direction_id', db.Integer),
                         db.Column('shape_id', db.Integer),
                         db.Column('brigade_id', db.Integer),
                         db.Column('vehicle_id', db.Integer),
                         db.Column('variant_id', db.Integer),
                         db.Column('city_id', db.Integer)
                         )

# variants table
variants = db.Table('variants', meta,
                            db.Column('variant_id', db.Integer),
                            db.Column('is_main', db.Integer),
                            db.Column('equiv_main_variant_id', db.Integer),
                            db.Column('join_stop_id', db.Integer),
                            db.Column('disjoin_stop_id', db.Integer),
                            db.Column('city_id', db.Integer)
                            )

# vehicle_types table
vehicle_types = db.Table('vehicle_types', meta,
                                 db.Column('vehicle_type_id', db.Integer),
                                 db.Column('vehicle_type_name', db.String),
                                 db.Column('vehicle_type_description', db.String),
                                 db.Column('vehicle_type_symbol', db.String),
                                 db.Column('city_id', db.Integer)
                                 )


def db_engine_inspection():
    """checks if tables exists in reflected db tables"""
    if [tab_name for tab_name in meta.tables if tab_name not in ins.get_table_names()]:
        print('Creating tables')
        meta.create_all(eng, checkfirst=True)

def initialize_connection(connection_string: str = 'sqlite:///mpk.db'):
    """creating db connection and getting db metadata"""
    try:
        eng = db.create_engine(connection_string, echo=False)
        conn = eng.connect()
        meta.reflect(bind=eng)
        return conn
    except dbError as e:
        print(f"Error while connecting to db")
        raise e


def insert_data_row(conn, table_name: str, data: tuple):
    """insert single data row into specified table"""
    table = db.Table(table_name, meta)
    insert = db.insert(table).values(data)
    query = conn.execute(insert)
    return query.rowcount


def truncate_load_table(conn, table_name: str, source_path: str, city_name: str ='Wrocław'):
    """truncate table and load data based on source file with structure matching table structure"""
    #truncate table
    target_table = db.Table(table_name, meta)

    #validation of city existance
    if city_name not in [city['city_name'] for city in select_from_table(connection, 'cities')]:
        print(f'inserting city {city_name}')
        insert_data_row(connection, 'cities', (None, city_name))

    # truncate table
    conn.execute(db.delete(target_table))

    # load data into pandas dataframe
    df = pandas.read_csv(source_path)

    # inserting provided city_name to easier match data later on
    city_id = get_city_id(conn, city_name)
    df.insert(0, 'city_id', city_id)

    #actual insert of data to DB
    df.to_sql(table_name, con=eng, if_exists='append', index=False)


def select_count_data(conn, table_name):
    target_table = db.Table(table_name, meta)
    cnt = db.select([db.func.count()]).select_from(target_table)
    query = conn.execute(cnt)
    return query.fetchone()[0]


def select_from_table(conn, table_name: str, columns_list: tuple = None):
    target_table = db.Table(table_name, meta)
    table_columns = meta.tables[table_name].c
    if columns_list is not None:
        chosen_columns = [element for element in table_columns if str(element.name) in columns_list]
        q = db.select(chosen_columns)
    else:
        q = db.select(target_table)
    result = conn.execute(q).fetchall()
    ret = ([dict(val) for val in result])
    return ret


def select_routes_for_city(conn, city_name: str = 'Wrocław'):
    table = meta.tables['routes']
    try:
        city_id = get_city_id(conn, city_name)
    except db.exc.NoResultFound as e:
        raise e
    q = db.select(table).where(meta.tables['routes'].c.city_id == city_id)
    result = conn.execute(q).fetchall()
    cnt = len(result)
    if not result:
        return {'count': cnt}
    else:
        return ({'count': cnt}, {'routes':[dict(val) for val in result]})


def select_city_trips(conn, filter_value: str = 'Wrocław'):
    try:
        city_id = get_city_id(conn, filter_value)
    except db.exc.NoResultFound as e:
        raise e
    #building join based on relations
    join_q = trips.join(routes, trips.c.route_id == routes.c.route_id)\
        .join(stop_times, trips.c.trip_id == stop_times.c.trip_id)\
        .join(stops, stop_times.c.stop_id == stops.c.stop_id)\
        .join(vehicle_types, trips.c.vehicle_id == vehicle_types.c.vehicle_type_id)
    #buidling select query
    q = db.select(trips.c.trip_id, trips.c.trip_headsign, routes.c.route_id, stop_times.c.arrival_time, stops.c.stop_id, stops.c.stop_code,stops.c.stop_name,vehicle_types.c.vehicle_type_id )\
        .select_from(join_q)\
        .filter(trips.c.city_id == city_id)\
        .order_by(trips.c.trip_id.asc(), stop_times.c.stop_sequence.asc())
    result = conn.execute(q).fetchall()
    cnt = len(result)
    if not result:
        return {'count': cnt}
    else:
        return ({'count': cnt}, {'routes':[dict(val) for val in result]})

def get_city_id(conn, filter_value: str = 'Wrocław'):
    table = meta.tables['cities']
    q = db.select(table.c.city_id).where(table.c.city_name == filter_value)
    ret_value = conn.execute(q).fetchone()
    if ret_value is None:
        raise db.exc.NoResultFound(f'No result for: \"{filter_value}\"')
    else:
        return ret_value[0]

def parse_data_to_json(data_collection, column_list):
    df = pandas.DataFrame.from_records(data=data_collection, columns=column_list)
    return df.to_json(orient='index', indent=2)
