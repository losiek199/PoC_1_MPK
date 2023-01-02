from sqlalchemy.orm import declarative_base
Base = declarative_base()

from project.models.agency import Agency
from project.models.calendar import Calendar
from project.models.calendar_dates import Calendar_dates
from project.models.cities import Cities, Cities_schema
from project.models.city_trips import City_trips, City_trips_schema
from project.models.control_stops import Control_stops
from project.models.feed_info import Feed_info
from project.models.routes import Routes, Routes_schema
from project.models.route_types import Route_types
from project.models.shapes import Shapes
from project.models.stop_times import Stop_times
from project.models.stops import Stops
from project.models.trips import Trips
from project.models.variants import Variants
from project.models.vehicle_types import Vehicle_types
