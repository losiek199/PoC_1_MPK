from sqlalchemy import Column, Integer, Float, ForeignKey
from db_controller import Base

class Shapes(Base):
    __tablename__ = 'shapes'

    shape_id = Column(Integer, primary_key=True)
    shape_pt_lat = Column(Float)
    shape_pt_lon = Column(Float)
    shape_pt_sequence = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.city_id'))