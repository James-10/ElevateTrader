from sqlalchemy import Column, Enum, Integer, PrimaryKeyConstraint, ForeignKeyConstraint, String
from sqlalchemy.ext.declarative import declarative_base

from schemas.schemas import Symbols

Base = declarative_base()

def Symbols(Base):
    __tablename__ = "symbols"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol_code = Column(Enum(Symbols))