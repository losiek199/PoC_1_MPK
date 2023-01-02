import pytest
from project.models import Base, Cities, Cities_schema, City_trips, City_trips_schema, Routes, Routes_schema, Stops, Stop_times, Trips, Vehicle_types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.db_controller import insert_city_row, get_city_id, select_columns, select_routes_for_city, select_from_table

eng = create_engine('sqlite://',  echo=False, )
Session = sessionmaker(eng)

@pytest.fixture(autouse=True)
def db_session():
    Base.metadata.create_all(eng)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(autouse=True)
def valid_city(cities_mocked_row):
    valid_city = Cities(city_name=cities_mocked_row[0]['city_name'])
    return valid_city

@pytest.fixture(autouse=True)
def valid_route(routes_mocked_row):
    valid_route = Routes(agency_id=routes_mocked_row[0]['agency_id'],
                         city_id=routes_mocked_row[0]['city_id'],
                         route_desc=routes_mocked_row[0]['route_desc'],
                         route_id=routes_mocked_row[0]['route_id'],
                         route_long_name=routes_mocked_row[0]['route_long_name'],
                         route_short_name=routes_mocked_row[0]['route_short_name'],
                         route_type=routes_mocked_row[0]['route_type'],
                         route_type2_id=routes_mocked_row[0]['route_type2_id'],
                         valid_from=routes_mocked_row[0]['valid_from'],
                         valid_until=routes_mocked_row[0]['valid_until'])
    return valid_route

@pytest.fixture(autouse=True)
def valid_city_trip(trips_mocked_row):
    valid_city_trip = City_trips(city_id=trips_mocked_row[0]['city_id'],
                       trip_id=trips_mocked_row[0]['trip_id'],
                       trip_headsign=trips_mocked_row[0]['trip_headsign'],
                       route_id=trips_mocked_row[0]['route_id'],
                       arrival_time=trips_mocked_row[0]['arrival_time'],
                       stop_id=trips_mocked_row[0]['stop_id'],
                       stop_code=trips_mocked_row[0]['stop_code'],
                       stop_name=trips_mocked_row[0]['stop_name'],
                       vehicle_type_id=trips_mocked_row[0]['vehicle_type_id'])
    return valid_city_trip


# ----tests----
def test_db_city_valid(db_session, valid_city):
    db_session.add(valid_city)
    db_session.commit()
    ret_city = db_session.query(Cities).where(Cities.city_id == 1).one()
    assert ret_city.city_id == 1
    assert ret_city.city_name == 'Wrocław'


def test_db_routes_valid(db_session, valid_route):
    db_session.add(valid_route)
    db_session.commit()
    ret_route = db_session.query(Routes).where(Routes.city_id == 1).one()
    assert ret_route.city_id == 1
    assert ret_route.route_type2_id == 35


def test_db_trips_valid(db_session, valid_city_trip):
    db_session.add(valid_city_trip)
    db_session.commit()
    ret_trip = db_session.query(City_trips).where(City_trips.trip_id == '8_11600331').one()
    assert ret_trip.trip_id == '8_11600331'
    assert ret_trip.route_id == '923'


def test_db_select_routes_for_city_function(db_session):
    response = select_routes_for_city(db_session, 'Wrocław')
    assert 'route_type2_id' in response[0].keys()
    assert response[0]['route_type2_id'] == 35


def test_db_select_from_table_function(db_session):
    response = select_from_table(db_session, 'cities')
    assert 'city_name' in response[0].keys()
    assert response[0]['city_name'] == 'Wrocław'


def test_db_insert_city_row_existing_function(db_session):
    response = insert_city_row(db_session, {'city_name': 'Wrocław'})
    assert response == 0

def test_db_insert_city_row_new_function(db_session):
    response = insert_city_row(db_session, {'city_name': 'TestCity'})
    assert response == 1
