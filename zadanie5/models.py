from sqlalchemy import (
    Column,
    SmallInteger,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Shipper(Base):
    __tablename__ = "shippers"

    ShipperID = Column(SmallInteger, primary_key=True)
    CompanyName = Column(String(40), nullable=False)
    Phone = Column(String(24))
