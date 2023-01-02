from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Route_types(Base):
    __tablename__ = 'route_types'
    
    route_type2_id = Column(Integer, ForeignKey('routes.route_type2_id'), primary_key=True)
    route_type2_name = Column(String)
    city_id = Column(Integer, ForeignKey('cities.city_id'))