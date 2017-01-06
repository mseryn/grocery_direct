#***
#*  GroceryDirect - Order API
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Order Description:
#*  - has:
#*      -- customer (owner) 
#*      -- id
#*      -- product list
#*      -- shipping address
#*      -- status
#*      -- placement date -- TODO, how implement?
#*  - get:
#*      -- product list
#*      -- total cost of products
#*      -- shipping address
#*      -- shipping state (for ease) - TODO
#*      -- order placement date
#*      -- order status
#*      -- customer ID
#*  - modify:
#*      -- product quantity -- TODO, vital
#*      -- shipping address
#*      -- order placement date -- TODO, how implement?
#*      -- order status
#*  - add/remove:
#*      -- products from list
#***

class Order():
    def __init__(self, customer_id):
        # init new row in table
        # ORACLE: insert into orders ()
        _id = 
        _customer = customer_id # TODO: implement error check to ensure customer exists
        # Currently customer can never change.

    def get_id(self):
        # 

    def get_product_list(self):

    def get_product_dict(self): #TODO: implement as unit test

    def get_status(self):
