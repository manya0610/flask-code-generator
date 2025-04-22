class DatabaseGenerator:
    def __init__(self):
        pass


    def database_generator(self):
        return """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from env import DATABASE_URL

engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
metadata = Base.metadata

"""