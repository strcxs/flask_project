import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


def get_engine():
    engine = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        os.environ["POSTGRES_PORT"],
        os.environ["POSTGRES_DB"],
    )
    return create_engine(engine, future=True)

Base = declarative_base()