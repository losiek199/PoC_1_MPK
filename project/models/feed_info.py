from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Feed_info(Base):
    __tablename__ = 'feed_info'

    feed_publisher_name = Column(String, primary_key=True)
    feed_publisher_url = Column(String)
    feed_lang = Column(String)
    feed_start_date = Column(Integer)
    feed_end_date = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.city_id'))

