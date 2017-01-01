#***
#*  GroceryDirect - Unit Tests for Orders
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*  
#*  Order Description:
#*  - has:
#*      -- product list
#*      -- shipping address
#*      -- status
#*      -- placement date
#*      -- customer (owner)
#*  - get:
#*      -- product list
#*      -- total cost of products
#*      -- shipping address
#*      -- shipping state (for ease)
#*      -- order placement date
#*      -- order status
#*      -- customer ID
#*  - modify:
#*      -- shipping address
#*      -- order placement date
#*      -- order status
#*  - add/remove:
#*      -- products from list
#***

#**************************************************************************************************
#**  ORDERS: TESTING PRODUCTS
#**************************************************************************************************

def order_add_product():
    # successfully add product 
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product)
    assert(order._products = [product]), "add_product did not correctly add a product"

def order_add_invalid_product():
    # unsuccessfully add nonexistant product
    order = order.Order()
    product = "this is not a valid product"
    order.add_product(product)
    assert(order._products = [product]), "add_product incorrectly added invalid product"

def order_add_null_product():
    # unsuccessfully add null product 
    order = order.Order()
    order.add_product(null)
    assert(order._products = []), "add_product incorrectly added a null product"

def order_remove_product():
    # remove product 
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product)
    order.remove_product(product)
    assert(order._products = []), "remove_product did not correctly remove a product"

def order_remove_nonexistant_product():
    # successfully return after attempt to remove product not in order
    # does NOT return an error
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.remove_product(product)
    assert(order._products = []), "remove_product incorrectly returned removing invalid product"

def order_remove_invalid_product():
    # unsuccessfully remove nonexistant product 
    order = order.Order()
    product = "this is not a valid product"
    order.add_product(product)
    order.remove_product(product)
    assert(order._products = []), 
        "remove_product incorrectly returned removing nonexistant product"

def order_remove_null_product():
    # unsuccessfully remove null product 
    order = order.Order()
    order.remove_product(null)
    assert(order._products = []), "remove_product incorrectly returned removing null product"

def order_get_products():
    # get list of all product s
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product)
    assert(order.get_products() = [product]), "get_products did not correctly list products"

def order_get_products_empty_list():
    # get empty list from products
    order = order.Order()
    assert(order.get_products() = []), "get_products did not correctly list empty list of products"



#**************************************************************************************************
#**  ORDERS: TESTING ADDRESSES
#**************************************************************************************************

def modify_order_shipping_address():
    # successfully modify order shipping address
    order = order.Order()
    order.modify_shipping_address("5555 test st.", "test city", "AL", 55555)
    order_address = order._shipping_address
    assert(order_address.get_street() = "5555 test st."), 
        "modify_shipping_address failed to modify street"
    assert(order_address.get_city() = "test city"), 
        "modify_shipping_address failed to modify city"
    assert(order_address.get_state() = "AL"), 
        "modify_shipping_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), 
        "modify_shipping_address failed to modify zip code"

def modify_order_billing_address():
    # successfully modify order billing address
    order = order.Order()
    order.modify_billing_address("5555 test st.", "test city", "AL", 55555)
    order_address = order._billing_address
    assert(order_address.get_street() = "5555 test st."), 
        "modify_billing_address failed to modify street"
    assert(order_address.get_city() = "test city"), 
        "modify_billing_address failed to modify city"
    assert(order_address.get_state() = "AL"), 
        "modify_billing_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), 
        "modify_billing_address failed to modify zip code"

def order_get_shipping_address():
    # successfully retrieve shipping address with get_address
    order = order.Order()
    order.modify_shipping_address("5555 test st.", "test city", "AL", 55555)
    order_address = order.get_shipping_address()
    assert(order_address.get_street() = "5555 test st."), 
        "modify_shipping_address failed to modify street"
    assert(order_address.get_city() = "test city"), 
        "modify_shipping_address failed to modify city"
    assert(order_address.get_state() = "AL"), 
        "modify_shipping_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), 
        "modify_shipping_address failed to modify zip code"

def order_get_billing_address():
    # successfully retrieve billing address with get_address
    order = order.Order()
    order.modify_billing_address("5555 test st.", "test city", "AL", 55555)
    order_address = order.get_billing_address()
    assert(order_address.get_street() = "5555 test st."), 
        "modify_billing_address failed to modify street"
    assert(order_address.get_city() = "test city"), 
        "modify_billing_address failed to modify city"
    assert(order_address.get_state() = "AL"), 
        "modify_billing_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), 
        "modify_billing_address failed to modify zip code"

#**************************************************************************************************
#**  TESTING ADDRESSES
#**************************************************************************************************

