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
  category = Column(String(100))
  date = Column(DateTime)
  user_id = Column(Integer, ForeignKey('users.id'))

  purchased_items = relationship("PurchasedItem", 
                      order_by="PurchasedItem.id", 
                      backref="receipt")

  def __init__(self, store_name, category, total_transaction, date):
    self.store_name = store_name
    self.category = category
    # self.tax_rate = tax_rate
    self.total_transaction = total_transaction
    self.date = date

  def serialize(self):
    return {
      "receipt_id" : self.id,
      "category" : self.category,
      "store_name" : self.store_name,
      # "tax_rate" : self.tax_rate,
      "total_transaction" : self.total_transaction,
      "date" : str(self.date)
      #"purchased_items" : [pi.serialize() for pi in self.purchased_items]
    }

  def serialize_with_items(self):
    return {
      "receipt_id" : self.id,
      "category" : self.category,
      "store_name" : self.store_name,
      # "tax_rate" : self.tax_rate,
      "total_transaction" : self.total_transaction,
      "date" : str(self.date),
      "items" : [pi.serialize() for pi in self.purchased_items]
    }

  def __repr__(self):
    return "<Receipt (id: {0}, shop_name: {1}, amount: {2})>".format(
              self.id,
              self.store_name,
              self.total_transaction
            )