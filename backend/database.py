import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
database_path = os.getenv("DATABASE_FOLDER")
database_name = os.getenv("DATABASE_FILE")

# create database folder if not exists
if not os.path.exists(database_path):
    os.makedirs(database_path)

# get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# join current directory with database folder and database file
database_file = os.path.join(current_dir, database_path, database_name)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_file}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
