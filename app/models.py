from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Listing(Base):
    __tablename__ = "listings"

    product_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, server_default='1', nullable=False)
    condition = Column(String, nullable=False) 
    date_posted = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    class_year = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.user_id'))
    seller_id = Column(Integer, ForeignKey('users.user_id'))
    product_id = Column(Integer, ForeignKey('listings.product_id'))
    quantity = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    status = Column(String, nullable=False, default='pending')