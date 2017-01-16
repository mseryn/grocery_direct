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

TEST_CUSTOMER   = person.Person.new_person()
TEST_PRODUCT    = product.Product.new_product()
TEST_ADDRESS    = address.Address.new_address()

#**************************************************************************************************
#**  ORDERS: TESTING CUSTOMER
#**************************************************************************************************

def order_get_customer():
    # successfully retrieve customer
    order = order.Order()
    assert_true(order.get_customer_id(), 1, /
        "get_customer_id() did not return correct customer ID for order")

#**************************************************************************************************
#**  ORDERS: TESTING PRODUCTS
#**************************************************************************************************

def order_add_product():
    # successfully add product 
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product.get_id())
    assert(order.get_product_list() = [product]), "add_product did not correctly add a product"

def order_add_invalid_product():
    # unsuccessfully add nonexistant product
    order = order.Order()
    product = "this is not a valid product"
    order.add_product(product.get_id())
    assert(order.get_product_list() = [product]), "add_product incorrectly added invalid product"

def order_add_null_product():
    # unsuccessfully add null product 
    order = order.Order()
    order.add_product(null)
    assert(order.get_product_list() = []), "add_product incorrectly added a null product"

def order_remove_product():
    # remove product 
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product.get_id())
    order.remove_product(product.get_id())
    assert(order.get_product_list() = []), "remove_product did not correctly remove a product"

def order_remove_nonexistant_product():
    # successfully return after attempt to remove product not in order
    # does NOT return an error
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.remove_product(product.get_id())
    assert(order.get_product_list() = []), "remove_product incorrectly returned removing invalid product"

def order_remove_invalid_product():
    # unsuccessfully remove nonexistant product 
    order = order.Order()
    product = "this is not a valid product"
    order.add_product(product.get_id())
    order.remove_product(product.get_id())
    assert(order.get_product_list() = []), /
        "remove_product incorrectly returned removing nonexistant product"

def order_remove_null_product():
    # unsuccessfully remove null product 
    order = order.Order()
    order.remove_product(null)
    assert(order.get_product_list() = []), "remove_product incorrectly returned removing null product"

def order_get_product_list():
    # get list of all product s
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product.get_id())
    assert(order.get_product_list() = [product]), "get_products did not correctly list products"

def order_get_products_empty_list():
    # get empty list from products
    order = order.Order()
    assert(order.get_product_list() = []), "get_products did not correctly list empty list of products"

def order_get_total_cost():
    # successfully retrieve total cost for items in product list
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product.get_id())
    assert_equals(order.get_total_cost(),  1.00, "get_total_cost did not correctly retrieve cost")

def order_get_total_cost_two_same_item():
    # successfully retrieve total cost for items in product list
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product.get_id())
    order.add_product(product.get_id())
    assert_equals(order.get_total_cost(),  2.00, "get_total_cost did not correctly retrieve cost")

def order_get_total_cost_empty_list():
    # successfully retrieve total cost of $0 for products in order
    order = order.Order()
    assert_equals(order.get_total_cost(),  0, /
    "get_products did not correctly retrieve cost of zero")

def order_change_product_quantity():
    # successfully change quantity of product in order
    order = order.Order()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    order.add_product(product.get_id())
    order.change_quantity(product.get_id(), 2)
    assert_equals(order.get_product_quantity(product.get_id()), 2, "
    


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
    assert(order_address.get_street() = "5555 test st."), /
        "modify_billing_address failed to modify street"
    assert(order_address.get_city() = "test city"), / 
        "modify_billing_address failed to modify city"
    assert(order_address.get_state() = "AL"), /
        "modify_billing_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), /
        "modify_billing_address failed to modify zip code"

def order_get_shipping_address():
    # successfully retrieve shipping address with get_address
    order = order.Order()
    order.modify_shipping_address("5555 test st.", "test city", "AL", 55555)
    order_address = order.get_shipping_address()
    assert(order_address.get_street() = "5555 test st."), /
        "modify_shipping_address failed to modify street"
    assert(order_address.get_city() = "test city"), /
        "modify_shipping_address failed to modify city"
    assert(order_address.get_state() = "AL"), /
        "modify_shipping_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), /
        "modify_shipping_address failed to modify zip code"

def order_get_billing_address():
    # successfully retrieve billing address with get_address
    order = order.Order()
    order.modify_billing_address("5555 test st.", "test city", "AL", 55555)
    order_address = order.get_billing_address()
    assert(order_address.get_street() = "5555 test st."), /
        "modify_billing_address failed to modify street"
    assert(order_address.get_city() = "test city"), /
        "modify_billing_address failed to modify city"
    assert(order_address.get_state() = "AL"), /
        "modify_billing_address failed to modify state code"
    assert(order_address.get_zip_code() = 55555), /
        "modify_billing_address failed to modify zip code"

#**************************************************************************************************
#**  ORDER: TESTING STATUS
#**************************************************************************************************

def order_get_initial_status():
    # successfully retrieve order status of "pending" (cart) prior to any changes to status
    order = order.Order()
    assert(order.get_status(), "pending", "get_status() failed to retrieve pending status"

def order_get_shipped_status():
    # successfully retrieve order status of "shipped" following change of status to "shipped"
    order = order.Order()
    order.mark_as_shipped()
    assert(order.get_status(), "shipped", "get_status() failed to retrieve shipped status"
    
def order_get_delivered_status():
    # successfully retrieve order status of "delivered" following change of status to "delivered"
    order = order.Order()
    order.mark_as_delivered()
    assert(order.get_status(), "delivered", "get_status() failed to retrieve delivered status"

def order_get_canceled_status():
    # successfully retrieve order status of "canceled" following change of status to "canceled"
    order = order.Order()
    order.mark_as_canceled()
    assert(order.get_status(), "canceled", "get_status() failed to retrieve canceled status"

#**************************************************************************************************
#**  ORDERS: TESTING PLACEMENT DATE
#**************************************************************************************************
