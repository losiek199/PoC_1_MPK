from sqlalchemy import Column, Integer, String, ForeignKey
from db_controller import Base

class Stop_times(Base):
    __tablename__ = 'stop_times'

    trip_id = Column(String(128), ForeignKey('trips.trip_id'))
    arrival_time = Column(String(128))
    departure_time = Column(String(128))
    stop_id = Column(Integer, ForeignKey('stops.stop_id'), primary_key=True)
    stop_sequence = Column(Integer)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.city_id'))