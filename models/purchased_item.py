from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship, backref

from models import Base

class PurchasedItem(Base):
  """docstring for PurchasedItem"""

  __tablename__ = 'purchaseditems'
  id = Column(Integer, primary_key=True)
  item_name = Column(String(200))
  quantity = Column(Integer)
  receipt_id = Column(Integer, ForeignKey('receipts.id'))

  #receipt = relationship("Receipt", 
  #          backref=backref('purchased_items', order_by=id))

  def __init__(self, item_name, quantity):
    self.item_name = item_name
    self.quantity = quantity

  def serialize(self):
    return {
      "purchased_item_id" : self.id,
      "item_name" : self.item_name,
      "quantity" : self.quantity
    }
    