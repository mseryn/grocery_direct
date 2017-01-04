#***
#*  GroceryDirect - Product Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Order Description:
#*  - has:
#*      -- id
#*      -- product list
#*      -- shipping address
#*      -- status
#*      -- placement date -- TODO, how implement?
#*      -- customer (owner) -- TODO, how implement? Very vital.
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
    def __init__(self):
        # init new row in table
        # ORACLE: insert into orders ()
        _id = self.get_id()

    def get_id(self):
        # 
"""
Implementing order:
Options:
    -- customer makes order instance, order retrieves instance data
        -- fairly clean but very interdependent between customer and order - not good

    -- order instances exist separately from customers entirely and only reference the owning customer
        -- less clean -- ensuring valid customer owns each order will get messy
        -- much less interdependency
            -- not sure if interdependency is actually bad - possible customer is really only user of orders

Examining...

Order making process:
1 - customer starts new order (cart)
    -- order starts with empty cart and default addresses from customer, status = "pending", palacement date = None
2 - customer manipulates items in cart
3 - customer goes to checkout; customer has option to change quantities/addresses
4 - customer places order. order status = "shipping". placement date = current date.
5 - customer's cart set to Null/None. Customer can now make new cart.

Customer order viewing process:
1 - customer enters account management page, selects order history
2 - customer sees chronological list of all orders placed on their account (status, items, total cost, etc)
3 - customer can select an order to see further details (addresses, card details, etc)
4 - customer can press "repeat order" button to replace cart with clone of products in viewed order
5 - no user can change product data once order moves out of "pending" status
        -- this can potentially be changed but will stand for now

Staff/Admin order viewing process:
1 - staff enters order viewing page
2 - staff either looks at a date range for orders or enters customer data to see customer's order history
3 - if staff uses customer, identical view as customer (minus button to repeat order)
4 - if staff uses chronological date range for orders, sees list of order details (when placed, customer, status, items, cost, etc)
5 - staff cannot change order details except to change status between "shipped", "delivered", and "canceled" - all referencing specific customer
        -- IE, cannot change order back to "pending" to protect cart integrity

Notes from processes:
- customer controls everything. makes sense to separate functionality into customer at the cart level at minimum.
- staff/administrators viewing orders will do so via two sort mechanisms:
        - date
            -- use custom select statement from order table related to placement date
        - customer
            -- use custom select statement from customer table and then use commands in customer class to retrieve order history
-- possibly (possibly) relevant to make order a subclass of customer?
    - pros:
        -- much cleaner
        -- zero interdependency - all one class
        -- since orders only ever come directly from orders table or in reference to a customer, this is acceptable 
    - cons:
        -- violates single purpose class goal for OO paradigm
            --- doesn't necessarially violate it more than making order its own class (major interdependency nastyness)

Decision: order is to be a subclass of customer.

"""
