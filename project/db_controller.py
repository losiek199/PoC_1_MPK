import pandas
import sqlalchemy as db
from sqlalchemy.exc import SQLAlchemyError
import os

eng = db.create_engine('sqlite:///mpk.db', echo=False)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=eng)

#importing models after declarative Base object is created to not couse dependency errors
from project.models import Base, Cities, Cities_schema, City_trips, City_trips_schema, Routes, Routes_schema, Stops, Stop_times, Trips, Vehicle_types
base_tables = {}
Base.metadata.bind = eng
Base.metadata.create_all()

def insert_city_row(session, data):
    """insert single data row into cities table"""
    #check if city exists within table
    city = session.query(Cities).filter_by(city_name=data['city_name']).all()
    if len(city) == 0:
        new_city = Cities(city_name=data['city_name'])
        session.add(new_city)
        return 1
    else:
        return 0

def get_city_id(session, filter_value: str = 'Wrocław'):
    """returns city_id based on city_name"""
    try:
        result = session.query(Cities.city_id).where(Cities.city_name == filter_value).one()
    except db.exc.NoResultFound:
        return -1
    else:
        return result[0]

def get_class_from_model(table_name):
    # search for valid table in metadata
    table = None
    # extract table class from model
    for table_class in Base.__subclasses__():
        if hasattr(table_class, '__tablename__') and table_class.__tablename__ == table_name:
            print(f'found match {table_name}, matching class {table_class}')
            table = table_class
    if table == None:
        print('didn''t found any match' )
        raise db.exc.NoSuchTableError(table_name)
    return table

def select_columns(model_class, columns):
    """returns columns available on that model builded on class"""
    if len(columns) == 0:
        return None
    else:
        print(columns)
        columns_meta = [model_class for col in columns]
        return columns_meta

def load_city_trips():
    """Function preloads city trips based on prepared query to speed up data handling between db and API"""
    session = Session()
    #clean current data
    del_query = db.delete(City_trips)
    session.execute(del_query)

    #Loading query
    sel_query = session.query(Trips) \
        .join(Routes) \
        .join(Stop_times) \
        .join(Stops) \
        .join(Vehicle_types) \
        .with_entities(Trips.city_id,
                       Trips.trip_id,
                       Trips.trip_headsign,
                       Routes.route_id,
                       Stop_times.arrival_time,
                       Stops.stop_id,
                       Stops.stop_code,
                       Stops.stop_name,
                       Vehicle_types.vehicle_type_id) \
        .where(Trips.city_id == 1) \
        .distinct() \
        .all()

    #creating list of objects to laod into City_trips table
    city_trips = []
    for obj in sel_query:
        city_trips.append(City_trips(city_id=obj['city_id'],
                                     trip_id=obj['trip_id'],
                                     trip_headsign=obj['trip_headsign'],
                                     route_id=obj['route_id'],
                                     arrival_time=obj['arrival_time'],
                                     stop_id=obj['stop_id'],
                                     stop_code=obj['stop_code'],
                                     stop_name=obj['stop_name'],
                                     vehicle_type_id=obj['vehicle_type_id'])
                          )
    session.add_all(city_trips)
    session.commit()


def truncate_load_table(session, table_name: str, source_path: str, city_name: str ='Wrocław'):
    """truncate table and load data based on source file with structure matching table structure"""

    #search for valid table in metadata
    table = get_class_from_model(table_name)
    #truncate table
    query = db.delete(table)
    session.execute(query)

    #validation of city existance
    if city_name not in [city.city_name for city in session.query(Cities)]:
        print(f'inserting city {city_name}')
        insert_city_row(session, {"city_name": city_name})

    # # load data into pandas dataframe
    df = pandas.read_csv(source_path)

    # # getting city_id to insert it into pandas DF, city ID extract from DB by using city_name
    city_id = get_city_id(session, city_name)
    if city_id < 0:
        return 'Provided city does not exist in DB'
    else:
        df.insert(0, 'city_id', city_id)

    #deduplication of data
    df.drop_duplicates(inplace=True)
    #actual insert of data to DB
    df.to_sql(table_name, con=eng, if_exists='replace', index=False)


def select_from_table(session, table_name: str, columns_list: tuple = None):
    """queries db to return data from given table, returns tuple of dicts"""
    table = get_class_from_model(table_name)
    if columns_list is not None:
        columns = select_columns(table, columns_list)
        result = session.query(table).with_entities(columns)
    else:
        result = session.query(table)
    ret = ([val.__dict__ for val in result])
    return ret


def select_routes_for_city(session, city_name: str = 'Wrocław'):
    """queries DB to extract data about available routes in given city"""
    routes_schema = Routes_schema(many=True)
    try:
        city_id = get_city_id(session, city_name)
    except db.exc.NoResultFound as e:
        raise e
    result = routes_schema.dump(session.query(Routes).where(Routes.city_id == city_id).all())
    return result


def select_city_trips(session, page, page_size, filter_value: str = 'Wrocław'):
    """queries DB to extract data regarding available city trips and returns json"""
    city_trips_schema = City_trips_schema(many=True)
    try:
        city_id = get_city_id(session, filter_value)
    except db.exc.NoResultFound as e:
        raise e
    #buidling select query
    query = session.query(City_trips).where(City_trips.city_id == city_id)
    query = query.limit(page_size)
    query = query.offset(page*page_size)
    result = city_trips_schema.dump(query.all())
    return result

def select_cities(session):
    """returns cities extracted from DB Cities table"""
    cities_schema = Cities_schema(many=True)
    result = cities_schema.dump(session.query(Cities).all())
    print(result)
    return result

def select_count_from_table(session, table_name):
    table_class = get_class_from_model(table_name)
    cnt = session.query.count(table_class)
    return cnt


def select_count_from_city_trips(session, filter_value):
    try:
        city_id = get_city_id(session, filter_value)
    except db.exc.NoResultFound as e:
        raise e
    cnt = session.query(City_trips).where(City_trips.city_id == city_id).count()
    return cnt