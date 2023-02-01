from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Establish connections
SQLACLCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
# SQLACLCHEMY_DATABASE_URL = "postgresql://postgres:postgres123@localhost/FastAPITutorial"
engine = create_engine(SQLACLCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Try connect to postgreSQL until it connects successfully
# Not needed anymore (Manual connection)
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastAPITutorial', user='postgres', 
                                password='postgres123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was a success")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"Error: {error}")
        sleep(2)
