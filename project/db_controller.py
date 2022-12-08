import sqlalchemy
import pandas

#creating db connection and getting db metadata
eng = sqlalchemy.create_engine('sqlite:///mpk.db', echo=False)
connection = eng.connect()
meta = sqlalchemy.MetaData(bind=connection)

#Setting up database schema - using sqlAlchemy to protect against sqlInjection
def create_db():
    cities = sqlalchemy.Table('cities', meta,
                              sqlalchemy.Column('city_id', sqlalchemy.Integer, primary_key=True),
                              sqlalchemy.Column('city_name', sqlalchemy.String)
                              )

    logs = sqlalchemy.Table('logs', meta,
                              sqlalchemy.Column('row_id', sqlalchemy.Integer, primary_key=True),
                              sqlalchemy.Column('log_dt', sqlalchemy.String),
                              sqlalchemy.Column('action', sqlalchemy.String)
                              )

    #agency table
    agency = sqlalchemy.Table('agency', meta,
                sqlalchemy.Column('agency_id', sqlalchemy.Integer),
                sqlalchemy.Column('agency_name', sqlalchemy.String),
                sqlalchemy.Column('agency_url', sqlalchemy.String),
                sqlalchemy.Column('agency_timezone', sqlalchemy.String),
                sqlalchemy.Column('agency_phone', sqlalchemy.String),
                sqlalchemy.Column('agency_lang', sqlalchemy.String),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
    )


    #calendar table
    calendar = sqlalchemy.Table('calendar', meta,
                sqlalchemy.Column('service_id', sqlalchemy.Integer),
                sqlalchemy.Column('monday', sqlalchemy.Integer),
                sqlalchemy.Column('tuesday', sqlalchemy.Integer),
                sqlalchemy.Column('wednesday', sqlalchemy.Integer),
                sqlalchemy.Column('thursday', sqlalchemy.Integer),
                sqlalchemy.Column('friday', sqlalchemy.Integer),
                sqlalchemy.Column('saturday', sqlalchemy.Integer),
                sqlalchemy.Column('sunday', sqlalchemy.Integer),
                sqlalchemy.Column('start_date', sqlalchemy.Integer),
                sqlalchemy.Column('end_date', sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                                )

    #calendar_dates table
    calendar_dates = sqlalchemy.Table('calendar_dates', meta,
                    sqlalchemy.Column('service_id', sqlalchemy.Integer),
                    sqlalchemy.Column('date', sqlalchemy.Integer),
                    sqlalchemy.Column('exception_type', sqlalchemy.Integer),
                    sqlalchemy.Column('city_id', sqlalchemy.Integer)
                    )

    #control_stops table
    control_stops = sqlalchemy.Table('control_stops', meta,
                sqlalchemy.Column('variant_id', sqlalchemy.Integer),
                sqlalchemy.Column('stop_id', sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )

    #feed_info table
    feed_info = sqlalchemy.Table('feed_info', meta,
                sqlalchemy.Column('feed_publisher_name', sqlalchemy.String),
                sqlalchemy.Column('feed_publisher_url', sqlalchemy.String),
                sqlalchemy.Column('feed_lang', sqlalchemy.String),
                sqlalchemy.Column('feed_start_date', sqlalchemy.Integer),
                sqlalchemy.Column('feed_end_date', sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )


    #route_types table
    route_types = sqlalchemy.Table('route_types', meta,
                sqlalchemy.Column('route_type2_id', sqlalchemy.Integer),
                sqlalchemy.Column('route_type2_name', sqlalchemy.String),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )

    #routes table
    routes = sqlalchemy.Table('routes',meta,
                sqlalchemy.Column('route_id', sqlalchemy.String),
                sqlalchemy.Column('agency_id', sqlalchemy.Integer),
                sqlalchemy.Column('route_short_name', sqlalchemy.String),
                sqlalchemy.Column('route_long_name', sqlalchemy.String),
                sqlalchemy.Column('route_desc', sqlalchemy.String),
                sqlalchemy.Column('route_type', sqlalchemy.Integer),
                sqlalchemy.Column('route_type2_id', sqlalchemy.Integer),
                sqlalchemy.Column('valid_from', sqlalchemy.String),
                sqlalchemy.Column('valid_until', sqlalchemy.String),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )


    #shapes table
    shapes = sqlalchemy.Table('shapes', meta,
                sqlalchemy.Column('shape_id', sqlalchemy.Integer),
                sqlalchemy.Column('shape_pt_lat', sqlalchemy.Float),
                sqlalchemy.Column('shape_pt_lon', sqlalchemy.Float),
                sqlalchemy.Column('shape_pt_sequence', sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )


    #stop_times table
    stop_times = sqlalchemy.Table('stop_times', meta,
                sqlalchemy.Column('trip_id', sqlalchemy.String),
                sqlalchemy.Column('arrival_time', sqlalchemy.String),
                sqlalchemy.Column('departure_time', sqlalchemy.String),
                sqlalchemy.Column('stop_id', sqlalchemy.Integer),
                sqlalchemy.Column('stop_sequence', sqlalchemy.Integer),
                sqlalchemy.Column('pickup_type', sqlalchemy.Integer),
                sqlalchemy.Column('drop_off_type', sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )

    #stops table
    stops = sqlalchemy.Table('stops',meta,
                sqlalchemy.Column('stop_id', sqlalchemy.String),
                sqlalchemy.Column('stop_code', sqlalchemy.Integer),
                sqlalchemy.Column('stop_name', sqlalchemy.String),
                sqlalchemy.Column('stop_lat', sqlalchemy.Float),
                sqlalchemy.Column('stop_lon', sqlalchemy.Float),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )

    #trips table
    trips = sqlalchemy.Table('trips',meta,
                sqlalchemy.Column('route_id', sqlalchemy.Integer),
                sqlalchemy.Column('service_id', sqlalchemy.Integer),
                sqlalchemy.Column('trip_id', sqlalchemy.String),
                sqlalchemy.Column('trip_headsign' , sqlalchemy.Float),
                sqlalchemy.Column('direction_id' , sqlalchemy.Integer),
                sqlalchemy.Column('shape_id' , sqlalchemy.Integer),
                sqlalchemy.Column('brigade_id' , sqlalchemy.Integer),
                sqlalchemy.Column('vehicle_id' , sqlalchemy.Integer),
                sqlalchemy.Column('variant_id' , sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )

    #variants table
    variants = sqlalchemy.Table('variants', meta,
                sqlalchemy.Column('variant_id', sqlalchemy.Integer),
                sqlalchemy.Column('is_main', sqlalchemy.Integer),
                sqlalchemy.Column('equiv_main_variant_id', sqlalchemy.Integer),
                sqlalchemy.Column('join_stop_id', sqlalchemy.Integer),
                sqlalchemy.Column('disjoin_stop_id', sqlalchemy.Integer),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )

    #vehicle_types table
    vehicle_types = sqlalchemy.Table('vehicle_types', meta,
                sqlalchemy.Column('vehicle_type_id', sqlalchemy.Integer),
                sqlalchemy.Column('vehicle_type_name', sqlalchemy.String),
                sqlalchemy.Column('vehicle_type_description', sqlalchemy.String),
                sqlalchemy.Column('vehicle_type_symbol', sqlalchemy.String),
                sqlalchemy.Column('city_id', sqlalchemy.Integer)
                )
    #commiting creation of tables only if tables are not existend within DB
    meta.create_all(eng, checkfirst=True)

    #validation of city existance
    if 'Wrocław' not in [city for id, city in select_from_table(connection, 'cities')]:
        insert_data_row(connection, 'cities', (None, 'Wrocław'))


def initialize_connection():
    """creating db connection and getting db metadata"""
    eng = sqlalchemy.create_engine('sqlite:///mpk.db', echo=False)
    conn = eng.connect()
    meta.reflect(bind=eng)
    return conn


def insert_data_row(conn, table_name: str, data: tuple):
    """insert single data row into specified table"""
    table = sqlalchemy.Table(table_name, meta)
    insert = sqlalchemy.insert(table).values(data)
    query = conn.execute(insert)
    return query.rowcount


def truncate_load_table(conn, table_name: str, source_path: str, city_name: str ='Wrocław'):
    """truncate table and load data based on source file with structure matching table structure"""
    #truncate table
    target_table = sqlalchemy.Table(table_name, meta)
    print(meta.tables)
    if table_name in meta.tables:
        print(table_name)
    else:
        print(table_name,' not in schema')
        create_db()
    query = conn.execute(sqlalchemy.delete(target_table))
    #load data table
    df = pandas.read_csv(source_path)
    #inserting provided city_name to easier match data
    city_id = get_city_id(conn, city_name)
    df.insert(0, 'city_id', city_id)
    #actual insert of data to DB
    df.to_sql(table_name, con=eng, if_exists='append', index=False)


def select_count_data(conn, table_name):
    target_table = sqlalchemy.Table(table_name, meta)
    cnt = sqlalchemy.select([sqlalchemy.func.count()]).select_from(target_table)
    query = conn.execute(cnt)
    return query.fetchone()[0]


def select_from_table(conn, table_name: str, columns_list:tuple = None):
    target_table = sqlalchemy.Table(table_name, meta)
    table_columns = meta.tables[table_name].c
    if columns_list is not None:
        chosen_columns = [element for element in table_columns if str(element.name) in columns_list]
        q = sqlalchemy.select(chosen_columns)
    else:
        q = sqlalchemy.select(target_table)
    return conn.execute(q).fetchall()


def select_routes_for_city(conn, city_name: str):
    table = meta.tables['routes']
    try:
        city_id = get_city_id(conn, city_name)
    except sqlalchemy.exc.NoResultFound as e:
        raise e
    q = sqlalchemy.select(table).where(meta.tables['routes'].c.city_id == city_id)
    ret = conn.execute(q).fetchall()
    cnt = len(ret)
    if not ret:
        return {'count': cnt}
    else:
        return ({'count': cnt}, {'routes':[dict(val) for val in ret]})


def select_city_trips(conn, filter_value):
    try:
        city_id = get_city_id(conn, filter_value)
    except sqlalchemy.exc.NoResultFound as e:
        raise e
    pass


def get_city_id(conn, filter_value: str):
    table = meta.tables['cities']
    q = sqlalchemy.select(table.c.city_id).where(table.c.city_name == filter_value)
    ret_value = conn.execute(q).fetchone()
    if ret_value is None:
        raise sqlalchemy.exc.NoResultFound(f'No result for: \"{filter_value}\"')
    else:
        return ret_value[0]



def parse_data_to_csv(data_collection, column_list):
    pass

def parse_data_to_json(data_collection, column_list):
    df = pandas.DataFrame.from_records(data=data_collection, columns=column_list)
    return df.to_json(orient='index', indent=2)
