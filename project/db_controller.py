from sqlalchemy.exc import SQLAlchemyError
import pandas

import sqlalchemy as db
eng = db.create_engine('sqlite:///mpk.db', echo=False)
connection = eng.connect()

from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base(bind=eng)
Session = sessionmaker(bind=eng)

#importing models after declarative Base object is created to not couse dependency errors
from project.models import Agency, Calendar_dates, Calendar, Cities, Control_stops, Feed_info, Route_types, Routes, Shapes, Stops, Stop_times, Trips, Variants, Vehicle_types

#medatadata and inspector for created DB
ins = db.inspect(eng)

#creating DB tables and metadatada schema
Base.metadata.create_all()
meta = Base.metadata


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
    except SQLAlchemyError as e:
        print(f"Error while connecting to db")
        raise e


def insert_city_row(data):
    """insert single data row into cities table"""
    session = Session()
    #check if city exists within table
    city = session.query(Cities).filter_by(city_name=data['city_name']).all()
    if len(city) == 0:
        new_city = Cities(city_name=data['city_name'])
        session.add(new_city)
        session.commit()
        print(new_city.city_name, new_city.city_id)
        return 1
    else:
        return 0
\
def get_city_id(filter_value: str = 'Wrocław'):
    try:
        session = Session()
        # result = session.query(Cities.city_id).where(Cities.city_name == filter_value).one()
        result = session.query(Cities.city_id).where(Cities.city_name == filter_value).one()
        print(result)
    except db.exc.NoResultFound:
        return -1
    else:
        return result


def truncate_load_table(table_name: str, source_path: str, city_name: str ='Wrocław'):
    """truncate table and load data based on source file with structure matching table structure"""
    session = Session()
    #truncate table
    session.query(text(table_name))
    # session.query(text(table_name)).delete()
    #validation of city existance
    if city_name not in [city.city_name for city in session.query(Cities)]:
        print(f'inserting city {city_name}')
        insert_city_row({"city_name": city_name})
    else:
        print(city_name)

    # load data into pandas dataframe
    df = pandas.read_csv(source_path)

    # getting city_id provided above
    city_id = get_city_id(city_name)
    if city_id < 0:
        return 'Provided city does not exist in DB'
    else:
        df.insert(0, 'city_id', city_id)

    print('before insert ')
    #actual insert of data to DB
    df.to_sql(table_name, con=eng, if_exists='append', index=False)

def select_columns(modelClass, columns):
    if len(columns) == 0:
        return None
    else:
        columnsMeta = [f'{modelClass.__name__}.{col}' for col in columns]
        return columnsMeta

def select_count_data(table_name):
    session = Session()
    cnt = session.query(table_name).count()
    return cnt


def select_from_table(table_name: str, columns_list: tuple = None):
    session = Session()
    if columns_list is not None:
        columns = select_columns(columns_list)
        result = session.query(meta.tables[table_name]).with_entities(columns)
    else:
        result = session.query(meta.tables[table_name])
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

    session = Session()

    result = session.query(Trips)\
        .join(Routes)\
        .join(Stop_times)\
        .join(Stops)\
        .join(Vehicle_types)\
        .filter_by(city_id=city_id)
    print(result)
    #building join based on relations
    # join_q = Trips.join(routes, trips.c.route_id == routes.c.route_id)\
    #     .join(stop_times, trips.c.trip_id == stop_times.c.trip_id)\
    #     .join(stops, stop_times.c.stop_id == stops.c.stop_id)\
    #     .join(vehicle_types, trips.c.vehicle_id == vehicle_types.c.vehicle_type_id)
    #buidling select query
    # q = db.select(trips.c.trip_id, trips.c.trip_headsign, routes.c.route_id, stop_times.c.arrival_time, stops.c.stop_id, stops.c.stop_code,stops.c.stop_name,vehicle_types.c.vehicle_type_id )\
    #     .select_from(join_q)\
    #     .filter(trips.c.city_id == city_id)\
    #     .order_by(trips.c.trip_id.asc(), stop_times.c.stop_sequence.asc())
    # result = conn.execute(q).fetchall()
    cnt = len(result)
    if not result:
        return {'count': cnt}
    else:
        return ({'count': cnt}, {'routes':[dict(val) for val in result]})


def parse_data_to_json(data_collection, column_list):
    df = pandas.DataFrame.from_records(data=data_collection, columns=column_list)
    return df.to_json(orient='index', indent=2)
