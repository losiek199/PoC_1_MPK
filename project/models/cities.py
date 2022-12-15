from sqlalchemy import Column, Integer, String
from db_controller import Base

class Cities(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(128), unique=True, nullable=True)