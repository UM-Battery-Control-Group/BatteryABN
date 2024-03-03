import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv(dotenv_path='dev.env')

# Get database URI from environment variable
DATABASE_URI = os.getenv('DATABASE_URI')

# Create engine
engine = create_engine(DATABASE_URI, echo=True)

# connection = engine.connect()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session
Session = scoped_session(SessionLocal)

# Declare a base
Base = declarative_base()
