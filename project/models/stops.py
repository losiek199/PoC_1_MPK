from sqlalchemy import Column, Integer, String, Float
from db_controller import Base

class Stops(Base):
    __tablename__ = 'stops'

    stop_id = Column(String)
    stop_code = Column(Integer)
    stop_name = Column(String)
    stop_lat = Column(Float)
    stop_lon = Column(Float)
    city_id = Column(Integer)