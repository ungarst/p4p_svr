from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship, backref

from models import Base

class PurchasedItem(Base):
  """docstring for PurchasedItem"""

  __tablename__ = 'purchaseditems'
  id = Column(Integer, primary_key=True)
  item_name = Column(String(200))
  quantity = Column(Integer)
  price_per_unit = Column(Float)
  category = Column(String(100))
  receipt_id = Column(Integer, ForeignKey('receipts.id'))

  #receipt = relationship("Receipt", 
  #          backref=backref('purchased_items', order_by=id))

  def __init__(self, item_name, category, price_per_unit, quantity):
    self.item_name = item_name
    self.category = category
    self.price_per_unit = price_per_unit
    self.quantity = quantity

  def serialize(self):
    return {
      "purchased_item_id" : self.id,
      "item_name" : self.item_name,
      "category" : self.category,
      "price_per_unit" : self.price_per_unit,
      "quantity" : self.quantity
    }

  def __repr__(self):
    return "<PurchasedItem (id: {0}, item_name: {1}, quantity: {2})>".format(
              self.id,
              self.item_name,
              self.quantity
            )
    