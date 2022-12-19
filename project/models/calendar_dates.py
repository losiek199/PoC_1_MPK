from sqlalchemy import Column, Integer, String, ForeignKey
from db_controller import Base


class Calendar_dates(Base):
    __tablename__ = 'calendar_dates'

    service_id = Column(Integer, ForeignKey('calendar_dates.service_id'), primary_key=True)
    date = Column(Integer)
    exception_type = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.city_id'))

