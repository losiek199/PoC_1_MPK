from sqlalchemy import Column, Integer, ForeignKey
from . import Base

class Calendar(Base):
    __tablename__ = 'calendar'

    service_id = Column(Integer, ForeignKey('calendar_dates.service_id'), primary_key=True)
    monday = Column(Integer)
    tuesday = Column(Integer)
    wednesday = Column(Integer)
    thursday = Column(Integer)
    friday = Column(Integer)
    saturday = Column(Integer)
    sunday = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
