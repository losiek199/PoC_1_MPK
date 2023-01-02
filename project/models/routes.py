from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Routes(Base):
    __tablename__ = 'routes'

    route_id = Column(String(128), primary_key=True)
    agency_id = Column(Integer, ForeignKey('agency.agency_id'))
    route_short_name = Column(String(512))
    route_long_name = Column(String(512))
    route_desc = Column(String(512))
    route_type = Column(Integer)
    route_type2_id = Column(Integer)
    valid_from = Column(String(128))
    valid_until = Column(String(128))
    city_id = Column(Integer, ForeignKey('cities.city_id'))


class Routes_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Routes
        include_relationships = True
        load_instance = True