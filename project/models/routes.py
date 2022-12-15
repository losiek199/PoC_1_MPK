from sqlalchemy import Column, Integer, String
from db_controller import Base

class Routes(Base):
    __tablename__ = 'routes'

    route_id = Column(String)
    agency_id = Column(Integer)
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_desc = Column(String)
    route_type = Column(Integer)
    route_type2_id = Column(Integer)
    valid_from = Column(String)
    valid_until = Column(String)
    city_id = Column(Integer)
