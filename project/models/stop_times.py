from sqlalchemy import Column, Integer, String
from db_controller import Base

class Stop_times(Base):
    __tablename__ = 'stop_times'

    trip_id = Column(String)
    arrival_time = Column(String)
    departure_time = Column(String)
    stop_id = Column(Integer)
    stop_sequence = Column(Integer)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    city_id = Column(Integer)