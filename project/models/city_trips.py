from db_controller import Base
from sqlalchemy import Column, Integer, Float, String

class City_trips(Base):
    __tablename__ = 'city_trips'

    city_id = Column(Integer)
    trip_id = Column(String(128), primary_key=True)
    trip_headsign = Column(String)
    route_id = Column(String(128), primary_key=True)
    arrival_time = Column(String(128), primary_key=True)
    stop_id = Column(String(128), primary_key=True)
    stop_code = Column(Integer)
    stop_name = Column(String(128))
    vehicle_type_id = Column(Integer, primary_key=True)


