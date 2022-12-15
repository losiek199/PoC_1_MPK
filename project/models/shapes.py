from sqlalchemy import Column, Integer, Float
from db_controller import Base

class Shapes(Base):
    __tablename__ = 'shapes'

    shape_id = Column(Integer)
    shape_pt_lat = Column(Float)
    shape_pt_lon = Column(Float)
    shape_pt_sequence = Column(Integer)
    city_id = Column(Integer)