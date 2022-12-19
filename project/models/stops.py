from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db_controller import Base

class Stops(Base):
    __tablename__ = 'stops'

    stop_id = Column(String(128), primary_key=True)
    stop_code = Column(Integer)
    stop_name = Column(String(128))
    stop_lat = Column(Float)
    stop_lon = Column(Float)
    city_id = Column(Integer, ForeignKey('cities.city_id'))