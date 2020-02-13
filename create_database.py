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
from sqlalchemy.orm import sessionmaker

from config import Base, engine


class Tweets(Base):
    # db schema
    __tablename__ = 'disaster_tweets'

    datetime = Column(DateTime(timezone=True), nullable=False)

    tweet_id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, nullable=True)
    keyword = Column(String, nullable=False)
    text = Column(String, nullable=False)
    url = Column(String, nullable=True)

    __table_args__ = (UniqueConstraint('datetime', 'tweet_id',
                                       name='tweet_id_datetime_uc'),)


def loadSession():
    """create session"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# creates db schema
Base.metadata.create_all(engine)
