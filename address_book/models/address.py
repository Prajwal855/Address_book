from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    #TableName
    __tablename__ = "addresses"
    #TableColumns
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
