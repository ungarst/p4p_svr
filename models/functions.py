def category_spending(user):
  categories = {}
  for receipt in user.receipts:
    for item in receipt.purchased_items:
      categories[item.category] = categories.get(item.category, 0) + item.price_per_unit * item.quantity

  return categories
      