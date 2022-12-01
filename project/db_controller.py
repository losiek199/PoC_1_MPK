import sqlalchemy
import pandas

#creating db connection and getting db metadata
eng = sqlalchemy.create_engine('sqlite:///mpk.db', echo=False)
conn = eng.connect()
meta = sqlalchemy.MetaData()

#Setting up database schema - using sqlAlchemy to protect against sqlInjection
#cities
cities = sqlalchemy.Table('cities', meta,
                          sqlalchemy.Column('city_id', sqlalchemy.Integer),
                          sqlalchemy.Column('city_name', sqlalchemy.String)
                          )

logs = sqlalchemy.Table('logs', meta,
                          sqlalchemy.Column('log_dt', sqlalchemy.String),
                          sqlalchemy.Column('action', sqlalchemy.String)
                          )

#agency table
agency = sqlalchemy.Table('agency', meta, 
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('agency_id', sqlalchemy.Integer),
            sqlalchemy.Column('agency_name', sqlalchemy.String),
            sqlalchemy.Column('agency_url', sqlalchemy.String),
            sqlalchemy.Column('agency_timezone', sqlalchemy.String),
            sqlalchemy.Column('agency_phone', sqlalchemy.String),
            sqlalchemy.Column('agency_lang', sqlalchemy.String)
            )


#calendar table
calendar = sqlalchemy.Table('calendar', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('service_id', sqlalchemy.Integer),
            sqlalchemy.Column('monday', sqlalchemy.Integer),
            sqlalchemy.Column('tuesday', sqlalchemy.Integer),
            sqlalchemy.Column('wednesday', sqlalchemy.Integer),
            sqlalchemy.Column('thursday', sqlalchemy.Integer),
            sqlalchemy.Column('friday', sqlalchemy.Integer),
            sqlalchemy.Column('saturday', sqlalchemy.Integer),
            sqlalchemy.Column('sunday', sqlalchemy.Integer),
            sqlalchemy.Column('start_date', sqlalchemy.Integer),
            sqlalchemy.Column('end_date', sqlalchemy.Integer)
            )

#calendar_dates table
calendar_dates = sqlalchemy.Table('calendar_dates', meta,
                sqlalchemy.Column('city_id', sqlalchemy.Integer),
                sqlalchemy.Column('service_id', sqlalchemy.Integer),
                sqlalchemy.Column('date', sqlalchemy.Integer),
                sqlalchemy.Column('exception_type', sqlalchemy.Integer)
                )

#control_stops table
control_stops = sqlalchemy.Table('control_stops', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('variant_id', sqlalchemy.Integer),
            sqlalchemy.Column('stop_id', sqlalchemy.Integer)
            )

#feed_info table
feed_info = sqlalchemy.Table('feed_info', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('feed_publisher_name', sqlalchemy.String),
            sqlalchemy.Column('feed_publisher_url', sqlalchemy.String),
            sqlalchemy.Column('feed_lang', sqlalchemy.String),
            sqlalchemy.Column('feed_start_date', sqlalchemy.Integer),
            sqlalchemy.Column('feed_end_date', sqlalchemy.Integer)
            )


#route_types table
route_types = sqlalchemy.Table('route_types', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('route_type2_id', sqlalchemy.Integer),
            sqlalchemy.Column('route_type2_name', sqlalchemy.String)
            )

#routes table
routes = sqlalchemy.Table('routes',meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('route_id', sqlalchemy.String),
            sqlalchemy.Column('agency_id', sqlalchemy.Integer),
            sqlalchemy.Column('route_short_name', sqlalchemy.String),
            sqlalchemy.Column('route_long_name', sqlalchemy.String),
            sqlalchemy.Column('route_desc', sqlalchemy.String),
            sqlalchemy.Column('route_type', sqlalchemy.Integer),
            sqlalchemy.Column('route_type2_id', sqlalchemy.Integer),
            sqlalchemy.Column('valid_from', sqlalchemy.String),
            sqlalchemy.Column('valid_until', sqlalchemy.String)
            )


#shapes table
shapes = sqlalchemy.Table('shapes', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('shape_id', sqlalchemy.Integer),
            sqlalchemy.Column('shape_pt_lat', sqlalchemy.Float),
            sqlalchemy.Column('shape_pt_lon', sqlalchemy.Float),
            sqlalchemy.Column('shape_pt_sequence', sqlalchemy.Integer)
            )


#stop_times table
stop_times = sqlalchemy.Table('stop_times', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('trip_id', sqlalchemy.String),
            sqlalchemy.Column('arrival_time', sqlalchemy.String),
            sqlalchemy.Column('departure_time', sqlalchemy.String),
            sqlalchemy.Column('stop_id', sqlalchemy.Integer),
            sqlalchemy.Column('stop_sequence', sqlalchemy.Integer),
            sqlalchemy.Column('pickup_type', sqlalchemy.Integer),
            sqlalchemy.Column('drop_off_type', sqlalchemy.Integer)
            )

#stops table
stops = sqlalchemy.Table('stops',meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('stop_id', sqlalchemy.String),
            sqlalchemy.Column('stop_code', sqlalchemy.Integer),
            sqlalchemy.Column('stop_name', sqlalchemy.String),
            sqlalchemy.Column('stop_lat', sqlalchemy.Float),
            sqlalchemy.Column('stop_lon', sqlalchemy.Float)
            )

#trips table
trips = sqlalchemy.Table('trips',meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('route_id', sqlalchemy.Integer),
            sqlalchemy.Column('service_id', sqlalchemy.Integer),
            sqlalchemy.Column('trip_id', sqlalchemy.String),
            sqlalchemy.Column('trip_headsign' , sqlalchemy.Float),
            sqlalchemy.Column('direction_id' , sqlalchemy.Integer),
            sqlalchemy.Column('shape_id' , sqlalchemy.Integer),
            sqlalchemy.Column('brigade_id' , sqlalchemy.Integer),
            sqlalchemy.Column('vehicle_id' , sqlalchemy.Integer),
            sqlalchemy.Column('variant_id' , sqlalchemy.Integer)
            )

#variants table
variants = sqlalchemy.Table('variants', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('variant_id', sqlalchemy.Integer),
            sqlalchemy.Column('is_main', sqlalchemy.Integer),
            sqlalchemy.Column('equiv_main_variant_id', sqlalchemy.Integer),
            sqlalchemy.Column('join_stop_id', sqlalchemy.Integer),
            sqlalchemy.Column('disjoin_stop_id', sqlalchemy.Integer)
            )

#vehicle_types table
vehicle_types = sqlalchemy.Table('vehicle_types', meta,
            sqlalchemy.Column('city_id', sqlalchemy.Integer),
            sqlalchemy.Column('vehicle_type_id', sqlalchemy.Integer),
            sqlalchemy.Column('vehicle_type_name', sqlalchemy.String),
            sqlalchemy.Column('vehicle_type_description', sqlalchemy.String),
            sqlalchemy.Column('vehicle_type_symbol', sqlalchemy.String)
            )


#commiting creation of tables only if tables are not existend within DB
meta.create_all(eng, checkfirst=True)

def insert_data_row(table_name: str, data: tuple):
    """insert single data row into specified table"""
    table = sqlalchemy.Table(table_name, meta)
    insert = sqlalchemy.insert(table, data)
    query = conn.execute(insert)
    return query.rowcount

def truncate_load_table(table_name: str, source_path: str, city_name:str ='Wrocław'):
    """truncate table and load data based on source file with structure matching table structure"""
    #truncate table
    target_table = sqlalchemy.Table(table_name, meta)
    query = conn.execute(sqlalchemy.delete(target_table))
    print('Truncated table: {}, deleted: {} rows'.format(table_name, query.rowcount))
    #load data table
    df = pandas.read_csv(source_path)
    #inserting provided city_name to easier match data
    city_id = get_city_id(city_name)
    df.insert(0, 'city_id', city_id)
    #actual insert of data to DB
    df.to_sql(table_name, con=eng, if_exists='append', index=False)
    print('Rows inserted:', select_count_data(target_table))


def select_count_data(table_name):
    target_table = sqlalchemy.Table(table_name, meta)
    cnt = sqlalchemy.select([sqlalchemy.func.count()]).select_from(target_table)
    query = conn.execute(cnt)
    return query.fetchone()[0]


def select_from_table(table_name: str, columns_list:tuple = None):
    target_table = sqlalchemy.Table(table_name, meta)
    table_columns = meta.tables[table_name].c
    if columns_list is not None:
        chosen_columns = [element for element in table_columns if str(element.name) in columns_list]
        q = sqlalchemy.select(chosen_columns)
    else:
        q = sqlalchemy.select(target_table)
    return conn.execute(q).fetchall()

def get_city_id(filter_value: str):
    q = sqlalchemy.select(cities.c.city_id).where(cities.c.city_name == filter_value)
    return conn.execute(q).fetchone()[0]

def select_data_as_json(table_name):
    target_table = sqlalchemy.Table(table_name, meta)
    select = sqlalchemy.select(target_table)
    data = conn.execute(select).fetchall()
    df = pandas.DataFrame.from_records(data=data, columns=target_table.columns)
    return df.to_json(orient='index')


def parse_data_to_json(data_collection, column_list):
    target_table = sqlalchemy.Table(table_name, meta)
    df = pandas.DataFrame.from_records(data=data_collection, columns=column_list)
    return df.to_json(orient='index')


def get_routes_in_city(city_name):
    pass


def delete_data(table_name, column_name, filter_expression):
    pass


def update_data(table_name, column_name, new_column_value, filter_expression):
    pass