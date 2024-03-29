from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class Control_stops(Base):
    __tablename__ = 'control_stops'

    variant_id = Column(Integer,  ForeignKey('variants.variant_id'), primary_key=True)
    stop_id = Column(Integer, ForeignKey('stops.stop_id'), primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
