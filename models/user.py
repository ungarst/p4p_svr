from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship
from werkzeug import generate_password_hash, check_password_hash
import urllib, hashlib

from models import Base

class User(Base):
  
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email_address = Column(String(100), unique=True)
  gravatar_url = Column(String(100))
  pwdhash = Column(String())
  first_name = Column(String(50))
  last_name = Column(String(50))

  receipts = relationship("Receipt", 
              order_by="Receipt.id",
              backref="user")

  def __init__(self, email_address, password, first_name, last_name):
    self.email_address = email_address
    self.pwdhash = generate_password_hash(password)
    self.generate_gravatar_url()
    self.first_name = first_name
    self.last_name = last_name


  def generate_gravatar_url(self):
    email = self.email_address
    default = "mm"
    size=300
    base_gravatar_url = "http://www.gravatar.com/avatar/"

    self.gravatar_url = base_gravatar_url + \
                  hashlib.md5(email.lower()).hexdigest() + "?" + \
                  urllib.urlencode({'d':default, 's':str(size)}) 


  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  def serialize(self):
    return {
      "user_id" : self.id,
      "email_address" : self.email_address,
      "gravatar_url" : self.gravatar_url,
      "first_name" : self.first_name,
      "last_name" : self.last_name,
      "receipts" : [r.serialize() for r in self.receipts]
    }
