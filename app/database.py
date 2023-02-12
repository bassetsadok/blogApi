from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL='postgresql://postgres:basseT_2000@localhost/blogApiFastApi'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn=psycopg2.connect(host="localhost",database="blogApiFastApi",user="postgres",password="basseT_2000",cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("database connection was successfull ✅")
#         break
#     except Exception as error:
#         print("connection to database was failed")
#         print("error was ",error)
#         time.sleep(3)
