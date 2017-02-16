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

# Default strings for test person
FNAME       = "FirstName"
LNAME       = "LastName"
MIDDLE_INIT = "M"
USERNAME    = "testaccount"
PASSWORD    = "testpassword"


# Test objects (avoid cluttering db)
SHIP_ADDRESS = address.Address.new_address(SHIP_STREET, SHIP_CITY, SHIP_STATE_CODE, \
                SHIP_ZIP_CODE, SHIP_TYPE_STRING)
BILL_ADDRESS = address.Address.new_address(BILL_STREET, BILL_CITY, BILL_STATE_CODE, \
                BILL_ZIP_CODE, BILL_TYPE_STRING)
PRODUCT      = product.Product.new_product("test product", "food", \
                description = "test product for order tests")
PRODUCT.set_price_for_all_states(3)

CUSTOMER = person.check_credentials(USERNAME, PASSWORD)
if not CUSTOMER:
    CUSTOMER  = person.Person.new_person(USERNAME, PASSWORD, FNAME, LNAME, "customer", \
                   middle_initial = MIDDLE_INIT)


#**************************************************************************************************
#**  ORDERS: TESTING CUSTOMER
#**************************************************************************************************

def test_order_get_customer():
    # successfully retrieve customer
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    assert(TEST_ORDER.get_customer().get_id() == CUSTOMER.get_id()), \
        "get_customer_id() did not return correct customer ID for order"

#**************************************************************************************************
#**  ORDERS: TESTING PRODUCTS
#**************************************************************************************************

def test_order_add_product():
    # successfully add product 
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.add_product(PRODUCT)
    assert(TEST_ORDER.get_products()[0].get_id() == PRODUCT.get_id()), \
        "add_product did not correctly add a product"
        
def test_order_add_null_product():
    # unsuccessfully add null product 
    caught = False
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    try:
        TEST_ORDER.add_product(None)
    except:
        caught = True
    assert(caught == True and TEST_ORDER.get_products() == []), \
        "add_product incorrectly added a null product"

def test_order_remove_product():
    # remove product 
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.add_product(PRODUCT)
    TEST_ORDER.remove_product(PRODUCT)
    assert(TEST_ORDER.get_products() == []), \
        "remove_product did not correctly remove a product"

def test_order_remove_nonexistant_product():
    # successfully return after attempt to remove product not in order
    # does NOT return an error
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.remove_product(PRODUCT)
    assert(TEST_ORDER.get_products() == []), \
        "remove_product incorrectly returned removing invalid product"

def test_order_remove_null_product():
    # unsuccessfully remove null product 
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    try:
        TEST_ORDER.remove_product(None)
    except:
        pass
    assert(TEST_ORDER.get_products() == []), \
        "remove_product incorrectly returned removing null product"

def test_order_change_product_quantity():
    # successfully change quantity of product in order
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.add_product(PRODUCT)
    TEST_ORDER.modify_product_quantity(PRODUCT, 2)
    assert(TEST_ORDER.get_product_quantity(PRODUCT) == 2), \
        "modify_product_quantity() and get_product_quantity() failed to modify and retrieve \
        new quantity"

def test_order_modify_quantity_to_zero():
    # Successfully modify quantity to zero
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.add_product(PRODUCT)
    TEST_ORDER.modify_product_quantity(PRODUCT, 0)
    assert(TEST_ORDER.get_products() == []), \
        "modify quantity failed to remove product when quantity changed to zero"

#**************************************************************************************************
#** TOTAL COST
#**************************************************************************************************

def test_order_get_total_cost():
    # successfully retrieve total cost for items in product list
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_shipping_address(SHIP_ADDRESS)
    TEST_ORDER.add_product(PRODUCT)
    assert(TEST_ORDER.get_total_cost() ==  PRODUCT.get_price_per_state(SHIP_STATE_CODE)), \
        "get_total_cost did not correctly retrieve cost"

def test_order_get_total_cost_two_same_item():
    # successfully retrieve total cost for items in product list
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_shipping_address(SHIP_ADDRESS)
    TEST_ORDER.add_product(PRODUCT)
    TEST_ORDER.add_product(PRODUCT)
    assert(TEST_ORDER.get_total_cost() ==  (2 * PRODUCT.get_price_per_state(SHIP_STATE_CODE))), \
        "get_total_cost did not correctly retrieve cost"

def test_order_get_total_cost_empty_list():
    # successfully retrieve total cost of $0 for products in order
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_shipping_address(SHIP_ADDRESS)
    assert(TEST_ORDER.get_total_cost() ==  0), \
        "get_products did not correctly retrieve cost of zero"

#**************************************************************************************************
#**  ORDERS: TESTING ADDRESSES
#**************************************************************************************************

def test_get_order_shipping_address():
    # Successfully retrieve Null addresse
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    assert(TEST_ORDER.get_shipping_address() == None), \
        "get_shipping_address() failed to retrieve Null address for order"

def test_get_order_billing_address():
    # Successfully retrieve Null addresse
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    assert(TEST_ORDER.get_billing_address() == None), \
        "get_billing_address() failed to retrieve Null address for order"

def modify_order_shipping_address():
    # successfully modify order shipping address
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_shipping_address(SHIP_ADDRESS)
    TEST_ORDER_address = TEST_ORDER.get_shipping_address()
    assert(TEST_ORDER_address.get_id() == SHIP_ADDRESS.get_id()), \
        "modify_shipping_address failed to modify street"

def modify_order_billing_address():
    # successfully modify order billing address
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_billing_address(BILL_ADDRESS)
    TEST_ORDER_address = TEST_ORDER.get_billing_address()
    assert(TEST_ORDER_address.get_id() == BILL_ADDRESS.get_id()), \
        "modify_billing_address failed to  street"


#**************************************************************************************************
#**  ORDER: TESTING STATUS
#**************************************************************************************************

def test_order_get_initial_status():
    # successfully retrieve order status of "pending" (cart) prior to any changes to status
    new_status = "pending"
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    assert(TEST_ORDER.get_status() == new_status), \
        "get_status() failed to retrieve pending status"

def test_order_get_shipped_status():
    # successfully retrieve order status of "shipped" following change of status to "shipped"
    new_status = "shipping"
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_status(new_status)
    assert(TEST_ORDER.get_status() == new_status), \
        "modify_status() failed to modify and retrieve %s status" %(new_status)
    
def test_order_get_delivered_status():
    # successfully retrieve order status of "delivered" following change of status to "delivered"
    new_status = "delivered"
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_status(new_status)
    assert(TEST_ORDER.get_status() == new_status), \
        "modify_status() failed to modify and retrieve %s status" %(new_status)

def test_order_get_canceled_status():
    # successfully retrieve order status of "canceled" following change of status to "canceled"
    new_status = "canceled"
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_status(new_status)
    assert(TEST_ORDER.get_status() == new_status), \
        "modify_status() failed to modify and retrieve %s status" %(new_status)

def test_order_modify_invalid_string():
    # Successfully return from attempt to modify status to invalid status
    new_status = "invalid"
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    TEST_ORDER.modify_status(new_status)
    assert(TEST_ORDER.get_status() == "pending"), \
        "modify_status() failed to return from attempt to modify status to invalid string for \
        order"

#**************************************************************************************************
#**  ORDERS: TESTING PLACEMENT DATE
#**************************************************************************************************

def test_order_set_submission_date():
    TEST_ORDER = order.Order.new_order(CUSTOMER)
    now = datetime.datetime.now()
    TEST_ORDER.submit()
    sub_date = TEST_ORDER.get_submission_date()
    assert(now.date() == sub_date.date()), \
        "get_submission_date() and set_submission_date() failed to return datetime.datetime \
        object"
