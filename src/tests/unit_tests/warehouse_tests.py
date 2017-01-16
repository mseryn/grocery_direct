#***
#*  GroceryDirect - Warehouse Unit Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Warehouse Description:
#*  - has:
#*      -- id
#*      -- address (id)
#*      -- capacity
#*      -- stock (with prices set by state)
#*  - get:
#*      -- address (id)
#*      -- capacity
#*  - modify:
#*      -- address (id)
#*      -- capacity
#***

import warehouse
import address
import product

# String defaults
STREET       = "test warehouse street"
APT_NO       = "test warehouse apt"
CITY         = "test warehouse city"
STATE        = "TN"
ZIP_CODE     = 33445
FULL_STRING  = ", ".join((STREET, APT_NO, CITY, " ".join((STATE, str(ZIP_CODE)))))

#**************************************************************************************************
#**  ADDRESS
#**************************************************************************************************

def test_warehouse_get_address():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE, \
        apartment_no = APT_NO)
    assert(isinstance(test_warehouse.get_address(), address.Address)), \
        "get_address() did not return full address string for warehouse"

#**************************************************************************************************
#**  CAPACITY
#**************************************************************************************************

def test_warehouse_get_capacity():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_capacity() == 150), \
        "get_capacity() failed to return capacity for warehouse"

def test_warehouse_modify_capacity():
    new_capacity = 55500
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_capacity(new_capacity)
    assert(test_warehouse.get_capacity() == new_capacity), \
        "modify_capacity() failed to modify and return capacity for warehouse"

def test_warehouse_modify_capacity_invalid_type():
    new_capacity = "invalid capacity"
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_capacity(new_capacity)
    assert(test_warehouse.get_capacity() == 150), \
        "modify_capacity() failed handling attempt to modifiy capacity to string for warehouse"

def test_warehouse_modify_capacity_non_int():
    new_capacity = 400.5
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_capacity(new_capacity)
    assert(test_warehouse.get_capacity() == 400), \
        "modify_capacity() failed handling attempt to modifiy capacity to float for warehouse"

def test_warehouse_modify_capacity_invalid_amount():
    new_capacity = -15
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_capacity(new_capacity)
    assert(test_warehouse.get_capacity() == 150), \
        "modify_capacity() failed handle attempt to modify capacity to negative number for warehouse"


#**************************************************************************************************
#**  STOCK
#**************************************************************************************************

# Adding/Removing products from stock

def test_warehouse_get_stock_empty():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_stock() == []), \
        "get_stock() did not return initial empty list for warehouse"

def test_warehouse_add_product():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    print(test_product.get_id())
    print(test_warehouse.get_stock()[0].get_id())
    assert(len(test_warehouse.get_stock()) == 1 \
        and test_warehouse.get_stock()[0].get_id() == test_product.get_id()), \
        "add_product() did not successfully add product to warehouse stock"

def test_warehouse_remove_product():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    test_warehouse.remove_product(test_product)
    assert(test_warehouse.get_stock() == []), \
        "remove_product() did not successfully remove product from warehouse stock"

def test_warehouse_remove_nonexistant_product():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.remove_product(test_product)
    assert(test_warehouse.get_stock() == []), \
        "remove_product() did not behave correctly when removing product not in warehouse stock"

def test_warehouse_get_product_quantity():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    assert(test_warehouse.get_product_quantity(test_product) == 1), \
        "get_product_quantity(product) did not correctly return product quantity for warehouse stock"

def test_warehouse_get_quantity_multiple_add():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    test_warehouse.add_product(test_product)
    assert(test_warehouse.get_product_quantity(test_product) == 2), \
        "get_product_quantity(product) did not correctly get product quantity for product added twice \
         for warehouse stock"

def test_warehouse_modify_quantity_lower():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    test_warehouse.add_product(test_product)
    test_warehouse.modify_quantity(test_product, 1)
    assert(test_warehouse.get_product_quantity(test_product) == 1), \
        "modify_quantity(product) did not correctly modify product quantity for warehouse stock"

def test_warehouse_modify_quantity_higher():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    test_warehouse.modify_quantity(test_product, 7)
    assert(test_warehouse.get_product_quantity(test_product) == 7), \
        "modify_quantity(product) did not correctly modify product quantity for warehouse stock"

# Retrieving changing remaining capacity

def test_warehouse_get_remaining_capacity_empty_stock():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_remaining_capacity() == 150), \
        "get_remaining_capacity() did not correctly return full capacity for warehouse with empty \
         stock"

def test_warehouse_get_remaining_capacity():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_warehouse.add_product(test_product)
    assert(test_warehouse.get_remaining_capacity() == 147), \
        "get_remaining_capacity() did not correctly return capacity once product was added to \
         warehouse stock"

# Changing state, verify products change price

def test_warehouse_modify_state_verify_product_prices():
# remember - hard one, if change state, must EITHER change all products to new state's price or if state does not list product add old price to new state
    pass

# Attempting to change capacity to value less than remaining capacity

def test_warehouse_modify_capacity_invalid():
    test_warehouse = warehouse.Warehouse.new_warehouse(150, STREET, CITY, STATE, ZIP_CODE)
    test_product = product.Product.new_product("test product", "non-food", size = 120)
    test_warehouse.add_product(test_product)
    test_warehouse.modify_capacity(100)
    assert(test_warehouse.get_capacity() == 150), \
        "get_capacity() did not correctly behave when attempt was made to change capacity to value \
         less than remaining capacity"
