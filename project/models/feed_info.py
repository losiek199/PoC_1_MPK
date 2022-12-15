from sqlalchemy import Column, Integer, String
from db_controller import Base

class Feed_info(Base):
    __tablename__ = 'feed_info'

    feed_publisher_name = Column(String)
    feed_publisher_url = Column(String)
    feed_lang = Column(String)
    feed_start_date = Column(Integer)
    feed_end_date = Column(Integer)
    city_id = Column(Integer)

