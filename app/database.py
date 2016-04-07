"""This module initialises database transactions."""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import Config

engine = create_engine(Config.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """initialises database."""
    import app.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
