from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship
from werkzeug import generate_password_hash, check_password_hash

from models import Base

class User(Base):
  
  __tablename__ = 'users'
  uid = Column(Integer, primary_key=True)
  email_address = Column(String(10), unique=True)
  pwdhash = Column(String())
  first_name = Column(String(50))
  last_name = Column(String(50))

  def __init__(self, email_address, password, first_name, last_name):
    self.email_address = email_address
    self.pwdhash = generate_password_hash(password)
    self.first_name = first_name
    self.last_name = last_name


  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  def serialize(self):
    return {
      "user_id" : self.uid,
      "email_address" : self.email_address,
      "first_name" : self.first_name,
      "last_name" : last_name
    }
