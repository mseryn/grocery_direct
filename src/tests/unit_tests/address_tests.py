#***
#*  GroceryDirect - Address Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Addresses:
#*  have:
#*      -- street
#*      -- apt (optional)
#*      -- city
#*      -- state
#*      -- zip code
#*      -- type
#*  get:
#*      -- street
#*      -- apt (if exists)
#*      -- city
#*      -- state
#*      -- zip code
#*      -- full address string?
#*      -- type
#*  modify:
#*      -- street
#*      -- apt
#*      -- city
#*      -- state
#*      -- zip code
#*      -- type
#***

import address
import person

# Default strings for tests
TEST_STREET         = "123 Test St."
TEST_APT_NO         = "Test Apt No. 1"
TEST_CITY           = "Test City"
TEST_STATE_CODE     = "AZ"
TEST_ZIP_CODE       = 12345
TEST_TYPE_STRING    = "shipping"

# Default strings for test person
FNAME       = "FirstName"
LNAME       = "LastName"
MIDDLE_INIT = "M" 
USERNAME    = "testaccount"
PASSWORD    = "testpassword"

# Test objects (avoid cluttering db)
CUSTOMER = person.check_credentials(USERNAME, PASSWORD)
if not CUSTOMER:
        CUSTOMER  = person.Person.new_person(USERNAME, PASSWORD, FNAME, LNAME, "customer", \
                           middle_initial = MIDDLE_INIT)

#**************************************************************************************************
#**  ADDRESS: PERSON
#**************************************************************************************************

def test_address_get_null_person():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_person().get_id() == None), "get_person did not correctly return \
        null for default for address"

def test_address_add_person():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.add_person(CUSTOMER)
    assert(test_address.get_person().get_id() == CUSTOMER.get_id()), "get and add person did \
        not correctly function for address"

#**************************************************************************************************
#**  ADDRESS: DEFAULT FLAG
#**************************************************************************************************

def test_address_get_default_flag():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_default_flag() == False), \
        "default flag did not return False for unmodified address"

def test_address_set_default():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.set_default_flag(True)
    assert(test_address.get_default_flag() == True), \
        "set default flag failed to modify flag to True for address without person"

def test_address_remove_default():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.set_default_flag(True)
    test_address.set_default_flag(False)
    assert(test_address.get_default_flag() == False), \
        "set default flag failed to modify flag to False for address without person"

#**************************************************************************************************
#**  ADDRESS: STREET
#**************************************************************************************************

def test_address_get_street():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_street() == TEST_STREET), \
        "get_street() did not return street name for address"

def test_address_modify_street():
    new_street_string = "321 New Test Street"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_street(new_street_string)
    assert(test_address.get_street() == new_street_string), \
        "modify_street() did not modify and return street name for address"

#**************************************************************************************************
#**  ADDRESS: APARTPEMNT NUMBER
#**************************************************************************************************

def test_address_get_apt():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING, apt_no = TEST_APT_NO)
    assert(test_address.get_apartment_no() == TEST_APT_NO), \
        "get_apartment_no() did not return apartment no. line for address"

def test_address_get_apt_none():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_apartment_no() == ""), \
        "get_apartment_no() did not return None for nonexistant apartment no. line for address"

def test_address_modify_apt():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_apartment_no(TEST_APT_NO)
    assert(test_address.get_apartment_no() == TEST_APT_NO), \
        "modify_apartment_no() did not modify and return apartment no. line for address"

#**************************************************************************************************
#**  ADDRESS: APARTPEMNT NUMBER
#**************************************************************************************************

def test_address_get_city():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_city() == TEST_CITY), "get_city() did not return city for address"

def test_address_modify_city():
    new_city_string = "New Test City"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_city(new_city_string)
    assert(test_address.get_city() == new_city_string), \
        "modify_city() did not modify and return city for address"

#**************************************************************************************************
#**  ADDRESS: ZIP_CODE
#**************************************************************************************************

def test_address_get_zip_code():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_zip_code() == TEST_ZIP_CODE), \
        "get_zip_code() did not return zipcode for address"

def test_address_modify_zip_code():
    new_zipcode = 99999
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_zip_code(new_zipcode)
    assert(test_address.get_zip_code() == new_zipcode), \
        "modify_zip_code() did not modify and return zipcode for address"

def test_address_modify_zip_invalid_type():
    new_zipcode = "invalid string"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_zip_code(new_zipcode)
    assert(test_address.get_zip_code() == TEST_ZIP_CODE), \
        "modify_zip_code() did not appropriatly handle invalid zip code for address"

def test_address_modify_zip_invalid_number():
    new_zipcode = 999999
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_zip_code(new_zipcode)
    assert(test_address.get_zip_code() == TEST_ZIP_CODE), \
        "modify_zip_code() did not appropriatly handle invalid numeric zip code for address"


#**************************************************************************************************
#**  ADDRESS: STATE
#**************************************************************************************************

def test_address_get_state():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_state() == TEST_STATE_CODE), \
        "get_state() did not return state for address"

def test_address_modify_state():
    new_state_code = "MN"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_state(new_state_code)
    assert(test_address.get_state() == new_state_code), \
        "modify_state() did not modify and return state for address"

def test_address_modify_state_invalid():
    new_state_code = "LL"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_state(new_state_code)
    assert(test_address.get_state() == TEST_STATE_CODE), \
        "modify_state() did not appropriatly handle invalid state code for address"


#**************************************************************************************************
#**  ADDRESS: TYPE
#**************************************************************************************************

def test_address_get_type():
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    assert(test_address.get_type() == TEST_TYPE_STRING), \
        "get_type() did not return type for address"

def test_address_modify_type_to_warehouse():
    new_type_string = "warehouse"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_type(new_type_string)
    assert(test_address.get_type() == new_type_string), \
        "modify_type() did not modify and return type for change to %s type address" \
        %(new_type_string)

def test_address_modify_type_to_billing():
    new_type_string = "billing"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_type(new_type_string)
    assert(test_address.get_type() == new_type_string), \
        "modify_type() did not modify and return type for change to %s type address" \
        %(new_type_string)

def test_address_modify_type_to_supplier():
    new_type_string = "supplier"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_type(new_type_string)
    assert(test_address.get_type() == new_type_string), \
        "modify_type() did not modify and return type for change to %s type address" \
        %(new_type_string)

def test_address_modify_type_invalid():
    new_type_string = "invalid string"
    test_address = address.Address.new_address(TEST_STREET, TEST_CITY, TEST_STATE_CODE, TEST_ZIP_CODE, \
        TEST_TYPE_STRING)
    test_address.modify_type(new_type_string)
    assert(test_address.get_type() == TEST_TYPE_STRING), \
        "modify_type() did appropriatly handle invalid type for address" \

