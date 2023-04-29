
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Config


SQLALCHEMY_URI = (
    Config.database_uri 
    if Config.database_uri
    else "sqlite://"
)

engine = create_engine(SQLALCHEMY_URI, echo=True)

session = Session(engine)