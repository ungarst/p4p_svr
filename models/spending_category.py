from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship, backref

from models import Base, db

class SpendingCategory(Base):
  """docstring for SpendingCategory"""
  
  __tablename__ = 'spendingcategories'
  id = Column(Integer, primary_key=True)
  category_name = Column(String(100))
  monthly_allowance = Column(Float)
  monthly_spend = Column(Float)
  user_id = Column(Integer, ForeignKey('users.id'))

  def __init__(self, category_name, monthly_allowance):
    self.category_name = category_name
    self.monthly_allowance = monthly_allowance

  def serialize(self):
    return {
      "spending_category_id" : self.id,
      "category_name" : self.category_name,
      "monthly_allowance" : self.monthly_allowance,
      "monthly_spend": self.monthly_spend
    }


def __repr__(self):
  return "<SpendingCategory (id: {0}, name: {1})>".format(
            self.id,
            self.category_name
          )

