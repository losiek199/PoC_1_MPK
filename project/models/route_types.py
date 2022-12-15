from sqlalchemy import Column, Integer, String
from db_controller import Base

class Route_types(Base):
    __tablename__ = 'route_types'
    
    route_type2_id = Column(Integer)
    route_type2_name = Column(String)
    city_id = Column(Integer)