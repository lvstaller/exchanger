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
    is_enabled = Column(Boolean)


class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    is_enabled = Column(Boolean)


class OrderStatus(Base):
    __tablename__ = "order_status"
    id = Column(Integer, primary_key=True, autoincrement= True)
    name = Column(Text)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer)
    master_id = Column(Integer)
    city_id = Column(Integer, ForeignKey("citys.id"))
    city = relationship("City", backref="orders")
    district_id = Column(Integer, ForeignKey("districts.id"))
    district = relationship("District", backref="orders")
    payment_system_id = Column(Integer, ForeignKey("payment_system.id"))
    payment_system = relationship("PaymentSystem", backref="orders")
    currency_id = Column(Integer, ForeignKey("currency.id"))
    currency = relationship("Currency", backref="orders")
    sum = Column(Float)
    status_id = Column(Integer, ForeignKey("order_status.id"), default=1)
    status = relationship("OrderStatus", backref="orders_with_this_status")
    longitude = Column(Float)
    latitude = Column(Float)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    level = Column(Integer)
