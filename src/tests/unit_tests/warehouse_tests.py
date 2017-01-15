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

# String defaults
STREET       = "test warehouse street"
APT_NO       = "test warehouse apt"
CITY         = "test warehouse city"
STATE        = "TN"
ZIP_CODE     = 33445
FULL_STRING  = ", ".join(STREET, APT_NO, CITY, (" ".join(STATE, ZIP_CODE)))

#**************************************************************************************************
#**  ADDRESS
#**************************************************************************************************

def test_warehouse_get_address():
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_address() == FULL_STRING), \
        "get_address() did not return full address string for warehouse"

def test_warehouse_modify_street():
    new_street = "new street"
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_street(new_street)
    assert(test_warehouse.get_street() == new_street), \
        "modify_street() failed to modify and return address street for warehouse"

def test_warehouse_modify_apartment_no():
    new_apt = "new apt no"
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_apartment_no(new_apt)
    assert(test_warehouse.get_apartment_no() == new_apt), \
        "modify_apartment_no() failed to modify and return address apartment for warehouse"

def test_warehouse_modify_apartment_no_to_null():
    new_apt = None
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_apartment_no(new_apt)
    assert(test_warehouse.get_apartment_no() == new_apt), \
        "modify_apartment_no() failed to modify and return Null address apartment for warehouse"

def test_warehouse_modify_city():
    new_city = "new city"
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_city(new_city)
    assert(test_warehouse.get_city() == new_city), \
        "modify_city() failed to modify and return address city for warehouse"

def test_warehouse_modify_zip_code():
    new_zip = 11122
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_zip_code(new_zip)
    assert(test_warehouse.get_zip_code() == new_zip), \
        "modify_zip_code() failed to modify and return address zip code for warehouse"

def test_warehouse_modify_state():
    new_state = "NY"
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_state(new_state)
    assert(test_warehouse.get_state() == new_state), \
        "modify_state() failed to modify and return address state for warehouse"

#**************************************************************************************************
#**  CAPACITY
#**************************************************************************************************

def test_warehouse_get_capacity():
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_capacity() == 150), \
        "get_capacity() failed to return capacity for warehouse"

def test_warehouse_modify_capacity():
    new_capacity = 55500
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    test_warehouse.modify_capacity()
    assert(test_warehouse.get_capacity() == new_capacity), \
        "modify_capacity() failed to modify and return capacity for warehouse"

def test_warehouse_modify_capacity_invalid_type():
    new_capacity = "invalid capacity"
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_capacity() == 150), \
        "modify_capacity() failed handling attempt to modifiy capacity to string for warehouse"

def test_warehouse_modify_capacity_non_int():
    new_capacity = 400.5
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_capacity() == 400), \
        "modify_capacity() failed handling attempt to modifiy capacity to float for warehouse"

def test_warehouse_modify_capacity_invalid_amount():
    new_capacity = -15
    test_warehouse = warehouse.Warehouse(150, STREET, apartment_no = APT_NO, CITY, STATE, ZIP_CODE)
    assert(test_warehouse.get_capacity() == 150), \
        "modify_capacity() failed handle attempt to modify capacity to negative number for warehouse"


#**************************************************************************************************
#**  STOCK
#**************************************************************************************************

# Adding/Removing products from stock

def test_warehouse_get_stock_empty():
    pass
def test_warehouse_get_stock():
    pass
def test_warehouse_add_product():
    pass
def test_warehouse_remove_product():
    pass
def test_warehouse_modify_quantity_lower():
    pass
def test_warehouse_modify_quantity_higher():
    pass

# Retrieving changing remaining capacity

def test_warehouse_get_remaining_capacity():
    pass

# Changing state, verify products change price

def test_warehouse_modify_state_verify_product_prices():
    pass

# Attempting to change capacity to value less than remaining capacity

def test_warehouse_modify_capacity_invalid():
    pass

# remember - hard one, if change state, must EITHER change all products to new state's price or if state does not list product add old price to new state
# also must handle modification of capacity -- kick out items? just fail? just fail.
