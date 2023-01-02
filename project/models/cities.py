from sqlalchemy import Column, Integer, String
from . import Base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Cities(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(128), unique=True, nullable=True)

    def __repr__(self):
        return f"'city_id': {self.city_id}, 'city_name': {self.city_name}"


class Cities_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cities
        include_relationships = True
        load_instance = True
