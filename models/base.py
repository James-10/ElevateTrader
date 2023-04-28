from sqlalchemy import Column, Enum, Integer, Time, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from schemas.schemas import SymbolsEnum, OrderTypes

Base = declarative_base()

def Symbols(Base):
    __tablename__ = "symbols"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol_code = Column(Enum(SymbolsEnum))

    orders = relationship("Order", back_populates="symbols")


def Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(OrderTypes), nullable=False)
    lot_size = Column(Float, nullable=False)
    time = Column(Time, nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.id"))
    
    symbols = relationship("Symbols", back_populates="orders")
    