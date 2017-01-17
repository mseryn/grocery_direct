#***
#*  GroceryDirect - Unit Tests for Orders
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

import order
import person
import product
import address

import datetime

#************************************************************************************************#
#** DEFAULTS FOR TESTS
#************************************************************************************************#

# Default strings for test ship_address
SHIP_STREET         = "123 Shipping St."
SHIP_APT_NO         = "Apt No. 1"
SHIP_CITY           = "Shipping City"
SHIP_STATE_CODE     = "AZ"
SHIP_ZIP_CODE       = 12345
SHIP_TYPE_STRING    = "shipping"

# Default strings for test bill_address
BILL_STREET         = "654 Billing St."
BILL_CITY           = "Billing City"
BILL_STATE_CODE     = "MI"
BILL_ZIP_CODE       = 98765
BILL_TYPE_STRING    = "billing"

# Test objects (avoid cluttering db)
SHIP_ADDRESS = address.Address.new_address(SHIP_STREET, SHIP_CITY, SHIP_STATE_CODE, \
                SHIP_ZIP_CODE, SHIP_TYPE_STRING)
BILL_ADDRESS = address.Address.new_address(BILL_STREET, BILL_CITY, BILL_STATE_CODE, \
                BILL_ZIP_CODE, BILL_TYPE_STRING)
PRODUCT      = product.Product.new_product("test product", "food", \
                description = "test product for order tests")
CUSTOMER     = person.Person.new_person() #TODO once person implemented

#**************************************************************************************************
#**  ORDERS: TESTING CUSTOMER
#**************************************************************************************************

def test_order_get_customer():
    # successfully retrieve customer
    pass
    order = order.Order(CUSTOMER)
    assert_true(order.get_customer_id(), 1, \
        "get_customer_id() did not return correct customer ID for order")

#**************************************************************************************************
#**  ORDERS: TESTING PRODUCTS
#**************************************************************************************************

def test_order_add_product():
    # successfully add product 
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    assert(order.get_product_list()[0].get_id() == PRODUCT.get_id()), \
        "add_product did not correctly add a product"
        
def test_order_add_null_product():
    # unsuccessfully add null product 
    order = order.Order(CUSTOMER)
    order.add_product(None)
    assert(order.get_product_list() == []), \
        "add_product incorrectly added a null product"

def test_order_remove_product():
    # remove product 
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    order.remove_product(PRODUCT)
    assert(order.get_product_list() == []), \
        "remove_product did not correctly remove a product"

def test_order_remove_nonexistant_product():
    # successfully return after attempt to remove product not in order
    # does NOT return an error
    order = order.Order(CUSTOMER)
    order.remove_product(PRODUCT)
    assert(order.get_product_list() == []), \
        "remove_product incorrectly returned removing invalid product"

def test_order_remove_invalid_product():
    # unsuccessfully remove nonexistant product 
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    order.remove_product(PRODUCT)
    assert(order.get_product_list() == []), \
        "remove_product incorrectly returned removing nonexistant product"

def test_order_remove_null_product():
    # unsuccessfully remove null product 
    order = order.Order(CUSTOMER)
    order.remove_product(None)
    assert(order.get_product_list() == []), \
        "remove_product incorrectly returned removing null product"

def test_order_change_product_quantity():
    # successfully change quantity of product in order
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    order.modify_product_quantity(PRODUCT, 2)
    assert_equals(order.get_product_quantity(PRODUCT), 2), \
        "modify_product_quantity() and get_product_quantity() failed to modify and retrieve \
        new quantity"

def test_order_modify_quantity_to_zero():
    # Successfully modify quantity to zero
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    order.modify_product_quantity(PRODUCT, 0)
    assert(order.get_products == []), \
        "modify quantity failed to remove product when quantity changed to zero"

#**************************************************************************************************
#** TOTAL COST
#**************************************************************************************************

def test_order_get_total_cost():
    # successfully retrieve total cost for items in product list
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    assert_equals(order.get_total_cost(),  PRODUCT.get_cost(), \
        "get_total_cost did not correctly retrieve cost")

def test_order_get_total_cost_two_same_item():
    # successfully retrieve total cost for items in product list
    order = order.Order(CUSTOMER)
    order.add_product(PRODUCT)
    order.add_product(PRODUCT)
    assert_equals(order.get_total_cost(),  2 * PRODUCT.get_cost(), \
        "get_total_cost did not correctly retrieve cost")

def test_order_get_total_cost_empty_list():
    # successfully retrieve total cost of $0 for products in order
    order = order.Order(CUSTOMER)
    assert_equals(order.get_total_cost(),  0, \
        "get_products did not correctly retrieve cost of zero")



#**************************************************************************************************
#**  ORDERS: TESTING ADDRESSES
#**************************************************************************************************

def test_get_order_shipping_address():
    # Successfully retrieve Null addresse
    order = order.Order(CUSTOMER)
    assert(order.get_shipping_address() == Null), \
        "get_shipping_address() failed to retrieve Null address for order"

def test_get_order_billing_address():
    # Successfully retrieve Null addresse
    order = order.Order(CUSTOMER)
    assert(order.get_billing_address() == Null), \
        "get_billing_address() failed to retrieve Null address for order"

def modify_order_shipping_address():
    # successfully modify order shipping address
    order = order.Order(CUSTOMER)
    order.modify_shipping_address(SHIP_ADDRESS)
    order_address = order.get_shipping_address()
    assert(order_address.get_id() == SHIP_ADDRESS.get_id()), \
        "modify_shipping_address failed to modify street"

def modify_order_billing_address():
    # successfully modify order billing address
    order = order.Order(CUSTOMER)
    order.modify_billing_address(BILL_ADDRESS)
    order_address = order.get_billing_address()
    assert(order_address.get_id() == BILL_ADDRESS.get_id()), \
        "modify_billing_address failed to  street"


#**************************************************************************************************
#**  ORDER: TESTING STATUS
#**************************************************************************************************

def test_order_get_initial_status():
    # successfully retrieve order status of "pending" (cart) prior to any changes to status
    new_status = "pending"
    order = order.Order(CUSTOMER)
    assert(order.get_status() == new_status), \
        "get_status() failed to retrieve pending status"

def test_order_get_shipped_status():
    # successfully retrieve order status of "shipped" following change of status to "shipped"
    new_status = "shipping"
    order = order.Order(CUSTOMER)
    order.modify_status(new_status)
    assert(order.get_status() == new_status), \
        "modify_status() failed to modify and retrieve %s status" %(new_status)
    
def test_order_get_delivered_status():
    # successfully retrieve order status of "delivered" following change of status to "delivered"
    new_status = "delivered"
    order = order.Order(CUSTOMER)
    order.modify_status(new_status)
    assert(order.get_status() == new_status), \
        "modify_status() failed to modify and retrieve %s status" %(new_status)

def test_order_get_canceled_status():
    # successfully retrieve order status of "canceled" following change of status to "canceled"
    new_status = "canceled"
    order = order.Order(CUSTOMER)
    order.modify_status(new_status)
    assert(order.get_status() == new_status), \
        "modify_status() failed to modify and retrieve %s status" %(new_status)

def test_order_modify_invalid_string():
    # Successfully return from attempt to modify status to invalid status
    new_status = "invalid"
    order = order.Order(CUSTOMER)
    order.modify_status(new_status)
    assert(order.get_status() == "pending"), \
        "modify_status() failed to return from attempt to modify status to invalid string for \
        order"

#**************************************************************************************************
#**  ORDERS: TESTING PLACEMENT DATE
#**************************************************************************************************

def test_order_set_submission_date():
    order = order.Order(CUSTOMER)
    order.set_submission_date()
    assert(isinstance(order.get_submission_date(), datetime.datetime)), \
        "get_submission_date() and set_submission_date() failed to return datetime.datetime \
        object"
