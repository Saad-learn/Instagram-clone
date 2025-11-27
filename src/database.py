from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:saadkhan@127.0.0.1:5432/clone_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# T44Sm_Wtp7UngbAtWolk0ZmczEE api secret
# 985451642451868 api key
# Cloud name: dfnqxqxhh



