import os

from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.env'), override=True)

POSTGRES_USER = os.environ.get('POSTGRES_USER', os.environ.get('USER'))
POSTGRES_PASS = os.environ.get('POSTGRES_PASS', '')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'tweet_db')
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(POSTGRES_USER, POSTGRES_PASS,
                                                            POSTGRES_HOST, POSTGRES_DB)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base(engine)

conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER,
                        password=POSTGRES_PASS, host=POSTGRES_HOST)
