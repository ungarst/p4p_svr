from models import db, User, Receipt, PurchasedItem
from datetime import datetime

def add_receipt(num_receipts=1):
	user = User.query.first()
	for x in range(num_receipts):
		SHOP_NAME = "Countdown Birkenhead"
		SHOP_CATEGORY = "Groceries"
		TOTAL = 123.81
		r = Receipt(SHOP_NAME, SHOP_CATEGORY, TOTAL, datetime.now())
		r.purchased_items = [
			    PurchasedItem("Chocolate Milk", SHOP_CATEGORY, 3.99, 2),
			    PurchasedItem("Garlic Pita Breads", SHOP_CATEGORY, 4.50, 1),
			    PurchasedItem("Old Spice Deoderant", SHOP_CATEGORY, 6.21, 4),
			    PurchasedItem("Eye Fillet Steak", SHOP_CATEGORY, 21.4, 1),
			    PurchasedItem("Obikwa Wine 750mL", SHOP_CATEGORY, 6.99, 4),
			    PurchasedItem("North Shore Rubbish Sack", SHOP_CATEGORY, 4.99, 5),
			    PurchasedItem("Nutri-Grain 700g", SHOP_CATEGORY, 6.23, 1),
			    PurchasedItem("Olivio Butter", SHOP_CATEGORY, 5.95, 1)
       					 	]
		user.receipts.append(r)
		print len(user.receipts)

	db.add(user)
	db.commit()

def create_database():
	u = User("dave@ungarst.com", "dave", "Dave", "Carpenter")
	db.add(u)
	db.commit()

