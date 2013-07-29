from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship

from models import Base

class Smartcard(Base):
	"""docstring for Smartcard"""
	__tablename__ = 'smartcards'
	id = Column(Integer, primary_key=True)
	smartcard_number = Column(String(20), unique=True)
	enabled = Column(Boolean)

	user_id = Column(Integer, ForeignKey('users.id'))

	def __init__(self, smartcard_number, enabled):
		self.smartcard_number = smartcard_number
		self.enabled = enabled

	def serialize(self):
		return {
			"smartcard_id" : self.id,
			"smartcard_number" : self.smartcard_number,
			"enabled" : self.enabled
		}
			
