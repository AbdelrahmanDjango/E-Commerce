from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
         # __init__ => Called when a new Cart object is created. and make seesion for user.
         # request => acsses seesion data by it.
     def __init__(self, request) -> None:
        # Store data by this line.
        # This is user's session -Generally- not just for cart.
        self.session = request.session
        # Retrieve the cart data from the user's session
        # CART_SESSION_ID => the key to identify the cart data in the session.
        cart = self.session.get(settings.CART_SESSION_ID)
     
        if not cart:
            # Save an empty cart in the session by create empty Dictionary.
            cart = self.session[settings.CART_SESSION_ID] = {}
            # self.cart => data 
        self.cart = cart
     def add (self, product, quantity=1, override_quantity=False):
        # converts the product id 
        # to a string to use it as a key in the self.cart dictionary.
        product_id = str(product.id)
        if product_id not in self.cart:
        # Check if there is product or not, if not.. inti the product
        # and give it a 0 quantity, and price.
              self.cart[product_id] = {'quantity':0, 
                                       'price' : str(product.price)}
        # If True, it sets the product's quantity to the given quantity.
        # override quantity mean => الكمية الحالية للمنتج داخل عربة التسوق هل هتزيد ولا لا؟
        if override_quantity: # False by default.
             self.cart[product_id]['quantity'] = quantity
        # If False it increments the existing quantity by the given quantity.
        else: # override quantity = True (حرفيًا).
             self.cart[product_id]['quantity'] += quantity
        self.save()


     def save(self):
        # Tell Django that session has been edited.
         self.session.modified = True


     def remove(self, product):
         product_id = str(product.id)

         if product_id in self.cart:
              del self.cart[product_id]
              self.save()

     def __iter__(self):
         
         # Fetch the keys -produbcts id- from the cart and put it in variable.
         products_ids = self.cart.keys()
         # Fetch all products in DB that equal products in cart.
         products = Product.objects.filter(id__in=products_ids)
         cart = self.cart.copy()
         # (for loop) for connenct products (DB) with the products that in cart.
         for product in products:
         # And make sure the product equal the produnct in dict (cart).
              cart [str(product.id)]['product'] = product


         # (for loop) to fetch values that equal data product in cart (to each product).
         for item in cart.values():
              # Convert the price to Decimal value.
              item['price'] = Decimal(item['price'])
              item['total_price'] = item['price'] * item ['quantity']
              # To return each item in every single time loop is did.
              yield item\
     
     def __len__(self):
          # Fetch quantitiy for each item, and sum it.
              return sum(item['quantity'] for item in self.cart.values())
     def get_total_price(self):
          return sum(Decimal(item['price']) * item ['quantity'] for item in self.cart.values())
     
     def clear(self):
          del self.session[settings.CART_SESSION_ID]
          self.save()



# class Cart:
#     def __init__(self, request):
#         """
#         Initialize the cart.
#         """
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             # save an empty cart in the session
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart

#     def __iter__(self):
#         """
#         Iterate over the items in the cart and get the products
#         from the database.
#         """
#         product_ids = self.cart.keys()
#         # get the product objects and add them to the cart
#         products = Product.objects.filter(id__in=product_ids)
#         cart = self.cart.copy()
#         for product in products:
#             cart[str(product.id)]['product'] = product
#         for item in cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item

#     def __len__(self):
#         """
#         Count all items in the cart.
#         """
#         return sum(item['quantity'] for item in self.cart.values())

#     def add(self, product, quantity=1, override_quantity=False):
#         """
#         Add a product to the cart or update its quantity.
#         """
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 0,
#                                      'price': str(product.price)}
#         if override_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#         self.save()

#     def save(self):
#         # mark the session as "modified" to make sure it gets saved
#         self.session.modified = True

#     def remove(self, product):
#         """
#         Remove a product from the cart.
#         """
#         product_id = str(product.id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()

#     def clear(self):
#         # remove cart from session
#         del self.session[settings.CART_SESSION_ID]
#         self.save()

#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())