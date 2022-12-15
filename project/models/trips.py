from sqlalchemy import Column, Integer, String, Float
from db_controller import Base

class Trips(Base):
    __tablename__ = 'trips'

    route_id = Column(Integer)
    service_id = Column(Integer)
    trip_id = Column(String)
    trip_headsign = Column(Float)
    direction_id = Column(Integer)
    shape_id = Column(Integer)
    brigade_id = Column(Integer)
    vehicle_id = Column(Integer)
    variant_id = Column(Integer)
    city_id = Column(Integer)