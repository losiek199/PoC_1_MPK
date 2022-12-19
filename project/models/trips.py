from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db_controller import Base

class Trips(Base):
    __tablename__ = 'trips'

    route_id = Column(Integer, ForeignKey('routes.route_id'))
    service_id = Column(Integer, ForeignKey('calendar_dates.service_id'))
    trip_id = Column(String(128), primary_key=True)
    trip_headsign = Column(Float)
    direction_id = Column(Integer)
    shape_id = Column(Integer, ForeignKey('shapes.shape_id'))
    brigade_id = Column(Integer)
    vehicle_id = Column(Integer, ForeignKey('vehicle_types.vehicle_type_id'))
    variant_id = Column(Integer, ForeignKey('variants.variant_id'))
    city_id = Column(Integer, ForeignKey('cities.city_id'))
