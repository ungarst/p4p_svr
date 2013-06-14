from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship
from werkzeug import generate_password_hash, check_password_hash

from models import Base

class User(Base):
  
  __tablename__ = 'users'
  uid = Column(Integer, primary_key=True)
  username = Column(String(60))
  pwdhash = Column(String())
  email = Column(String(60))

  def __init__(self, username, password, email):
    self.username = username
    self.pwdhash = generate_password_hash(password)
    self.email = email


  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  def serialize(self):
    return {
      "user_id" : self.uid,
      "username" : self.username,
      "email" : self.email,
      "pwdhash" : self.pwdhash
    }
