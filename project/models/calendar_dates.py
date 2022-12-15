from sqlalchemy import Column, Integer, String
from db_controller import Base


class Calendar_dates(Base):
    __tablename__ = 'calendar_dates'

    service_id = Column(Integer)
    date = Column(Integer)
    exception_type = Column(Integer)
    city_id = Column(Integer)

