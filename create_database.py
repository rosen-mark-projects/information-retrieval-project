import os

from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    String,
    Integer,
    create_engine,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.env'), override=True)

POSTGRES_USER = os.environ.get('POSTGRES_USER', os.environ.get('USER'))
POSTGRES_PASS = os.environ.get('POSTGRES_PASS', '')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'tweet_db')
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(POSTGRES_USER, POSTGRES_PASS,
                                                            POSTGRES_HOST, POSTGRES_DB)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base(engine)


class Tweets(Base):
    # db schema
    __tablename__ = 'disaster_tweets'

    datetime = Column(DateTime(timezone=True), nullable=False)

    tweet_id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, nullable=True)
    keyword = Column(String, nullable=False)
    text = Column(String, nullable=False)
    url = Column(String, nullable=True)


def loadSession():
    """create session"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# creates db schema
Base.metadata.create_all(engine)
