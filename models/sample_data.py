import os 
from random import choice, randint
import datetime

from models import db, User, Receipt, PurchasedItem

with open("models/sample_files/first_names.txt") as f:
  first_names = [first_name.strip() for first_name in f.read().split("\n")]

with open("models/sample_files/last_names.txt") as f:
  last_names = [last_name.strip()[0] + last_name.strip()[1:].lower() \
               for last_name in f.read().split("\n")]

with open("models/sample_files/stores.txt") as f:
  # print f.read()
  store_names = [store_name.strip() for store_name in f.read().split("\n")]


def rand_user():
  f = open("./users.txt", "a")

  first_name = choice(first_names)
  last_name = choice(last_names)
  email = "{}.{}@example.com".format(first_name, last_name)

  f.write("{} - {}\n".format(email, first_name))
  f.close()

  return User(email, first_name, first_name, last_name)

def rand_receipt():
  store = choice(store_names)
  print store
  store_name = store.split("-")[0].strip()
  category = store.split("-")[1].strip()

  tax_rate = randint(100, 150)/1000.0

  items = rand_items(store_name, category, randint(1, 7))

  total_transaction = 0.0
  for item in items:
    total_transaction += item.price_per_unit * item.quantity

  total_transaction = round(total_transaction, 2)

  receipt = Receipt(store_name, category, tax_rate, total_transaction, datetime.datetime.now())
  receipt.purchased_items = items

  return receipt

def rand_items(store_name, category, num_items):
  with open("models/sample_files/shop_items/" + store_name + ".txt") as f:
    items = [item.strip() for item in f.read().split("\n")]

  print len(items)
  print store_name

  purchased_items = []
  for i in xrange(num_items):
    item = items.pop(randint(0, len(items)-1))
    print item
    item_name, item_price = item.rsplit(" ", 1)
    purchased_items.append(PurchasedItem(item_name, category, float(item_price), randint(1, 7)))

  return purchased_items


def populate_database(num_users, min_receipts, max_receipts):
  # delete the old users file 
  try:
    os.remove("./users.txt")
  except OSError:
    print "no users.txt exists"

  # create each user and write their info to the users file 
  for i in xrange(num_users):
    user = rand_user()
    num_receipts = randint(min_receipts, max_receipts)

    for j in range(num_receipts):
      user.receipts.append(rand_receipt())    

    db.add(user)
    db.commit()
  # rand generate a random number of receipts to create for them
  # create those receipts
  # get a number of items to aput in the receipt 
  # generate them with a quantity
  # save to the db
  

