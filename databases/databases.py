from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    locale = Column(Text, default="ru")
    count_of_order = Column(Integer, default=0)
    all_sum = Column(Float, default=0)


class City(Base):
    __tablename__ = "citys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    is_enabled = Column(Boolean)


class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer)
    name = Column(Text)
    is_enabled = Column(Boolean)


class PaymentSystem(Base):
    __tablename__ = "payment_system"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)


class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer)
    district_id = Column(Integer)
    payment_system_id = Column(Integer)
    currency_id = Column(Integer)
    sum = Column(Float)
    longitude = Column(Float)
    latitude = Column(Float)
