from sqlalchemy import Column, Integer, String
from db_controller import Base


class Control_stops(Base):
    __tablesname__ = 'control_stops'
    variant_id = Column(Integer)
    stop_id = Column(Integer)
    city_id = Column(Integer)
