from sqlalchemy import Column, Integer, String
from db_controller import Base

class Agency(Base):
    __tablename__='agency'

    agency_id = Column(Integer)
    agency_name = Column(String)
    agency_url = Column(String)
    agency_timezone= Column(String)
    agency_phone= Column(String)
    agency_lang= Column(String)
    city_id= Column(Integer)