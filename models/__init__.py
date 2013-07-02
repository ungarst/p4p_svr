import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.getenv(
    'DATABASE_URL', 'sqlite:///./test.db'), convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))
Base = declarative_base()
Base.query = db.query_property()

from models.user import User
from models.receipt import Receipt
from models.purchased_item import PurchasedItem



def init_db(num_users=10, min_receipts=5, max_receipts=10):
    from models.sample_data import populate_database

    Base.metadata.create_all(bind=engine)

    populate_database(num_users, min_receipts, max_receipts)


def drop_db():
    from sqlalchemy import MetaData
    m = MetaData(engine)
    m.reflect()
    m.drop_all()
