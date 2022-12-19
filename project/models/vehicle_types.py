from sqlalchemy import Column, Integer, String, ForeignKey
from db_controller import Base

class Vehicle_types(Base):
    __tablename__ = 'vehicle_types'

    vehicle_type_id = Column(Integer, primary_key=True)
    vehicle_type_name = Column(String)
    vehicle_type_description = Column(String)
    vehicle_type_symbol = Column(String)
    city_id = Column(Integer, ForeignKey('cities.city_id'))


