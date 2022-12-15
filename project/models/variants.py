from sqlalchemy import Column, Integer, String, Float
from db_controller import Base

class Variants(Base):
    __tablename__ = 'variants'


    variant_id = Column(Integer)
    is_main = Column(Integer)
    equiv_main_variant_id = Column(Integer)
    join_stop_id = Column(Integer)
    disjoin_stop_id = Column(Integer)
    city_id = Column(Integer)