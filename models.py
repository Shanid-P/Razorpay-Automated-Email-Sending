from sqlalchemy import Column
from sqlalchemy import Integer, Boolean
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

from database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    
    payment_id = Column(String, unique=True)

    order_id = Column(String, unique=True)

    email = Column(String)

    contact = Column(String)
    
    amount = Column(String)
    
    status = Column(String)
    
    coupon_id = Column(String)
