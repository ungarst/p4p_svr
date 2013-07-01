from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship, backref

from models import Base

class Receipt(Base):
  """docstring for Receipt"""
  
  __tablename__ = 'receipts'
  id = Column(Integer, primary_key=True)
  store_name = Column(String(100))
  tax_rate = Column(Float)
  total_transaction = Column(Float)
  user_id = Column(Integer, ForeignKey('users.id'))

  purchased_items = relationship("PurchasedItem", 
                      order_by="PurchasedItem.id", 
                      backref="receipt")

  def __init__(self, store_name, tax_rate, total_transaction):
    self.store_name = store_name
    self.tax_rate = tax_rate
    self.total_transaction = total_transaction

  def serialize(self):
    return {
      "receipt_id" : self.id,
      "store_name" : self.store_name,
      "tax_rate" : self.tax_rate,
      "total_transaction" : self.total_transaction
      #"purchased_items" : [pi.serialize() for pi in self.purchased_items]
    }

  def serialize_with_items(self):
    return {
      "receipt_id" : self.id,
      "store_name" : self.store_name,
      "tax_rate" : self.tax_rate,
      "total_transaction" : self.total_transaction,
      "purchased_items" : [pi.serialize() for pi in self.purchased_items]
    }