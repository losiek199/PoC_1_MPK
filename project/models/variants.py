from sqlalchemy import Column, Integer, ForeignKey
from . import Base

class Variants(Base):
    __tablename__ = 'variants'

    variant_id = Column(Integer, primary_key=True)
    is_main = Column(Integer)
    equiv_main_variant_id = Column(Integer)
    join_stop_id = Column(Integer)
    disjoin_stop_id = Column(Integer)
    city_id = Column(Integer, ForeignKey('cities.city_id'))