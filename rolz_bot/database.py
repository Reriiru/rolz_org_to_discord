import settings

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(settings.DATABASE_STRING)
 