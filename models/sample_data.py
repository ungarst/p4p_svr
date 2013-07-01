import os 
from random import choice

from models import db, User, Receipt, PurchasedItem

with open("models/sample_files/first_names.txt") as f:
  first_names = [first_name.strip() for first_name in f.read().split("\n")]

with open("models/sample_files/last_names.txt") as f:
  last_names = [last_name.strip()[0] + last_name.strip()[1:].lower() \
               for last_name in f.read().split("\n")]

def rand_user():
  f = open("./users.txt", "a")

  first_name = choice(first_names)
  last_name = choice(last_names)
  email = "{}.{}@example.com".format(first_name, last_name)

  f.write("{} - {}\n".format(email, first_name))
  f.close()

  return User(email, first_name, first_name, last_name)


def populate_database(num_users, min_receipts, max_receipts):
  # delete the old users file 
  try:
    os.remove("./users.txt")
  except OSError:
    print "no users.txt exists"

  # create each user and write their info to the users file 
  for i in xrange(num_users):
    user = rand_user()
    
    db.add(user)
    db.commit()
  # rand generate a random number of receipts to create for them
  # create those receipts
  # get a number of items to aput in the receipt 
  # generate them with a quantity
  # save to the db
  

