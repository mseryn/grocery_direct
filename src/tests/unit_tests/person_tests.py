#***
#*  GroceryDirect - Customer Unit Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Person Description:
#*  - has:
#*      -- username
#*      -- PW (hashed)
#*      -- first name, last name, middle initial (optional)
#*      -- type
#*      -- addresses (via address table)
#*      -- orders (via order table) (customers only)
#*      -- salary (not customer)
#*      -- job title (not customer)
#*      -- balance (customer only)
#*  - get:
#*      -- username
#*      -- PW (hashed)
#*      -- first name, last name, middle initial (optional)
#*      -- type
#*      -- addresses (via address table)
#*      -- orders (via order table) (customers only)
#*      -- cart (customer only)
#*      -- salary (not customer)
#*      -- job title (not customer)
#*      -- balance (customer only)
#*  - modify:
#*      -- username
#*      -- PW (hashed)
#*      -- first name, last name, middle initial (optional)
#*      -- type
#*      -- addresses (via address table)
#*      -- orders (via order table) (customers only)
#*      -- cart (customer only)
#*      -- salary (only admin)
#*      -- job title (only admin)
#*      -- balance (customer only)
#***

import person


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
MIDDLE_INIT = "MI"
USERNAME    = "testaccount"
PASSWORD    = "testpassword"

TYPE_STRING = "customer"

# Test objects (avoid cluttering db)
SHIP_ADDRESS = address.Address.new_address(SHIP_STREET, SHIP_CITY, SHIP_STATE_CODE, \
                SHIP_ZIP_CODE, SHIP_TYPE_STRING)
BILL_ADDRESS = address.Address.new_address(BILL_STREET, BILL_CITY, BILL_STATE_CODE, \
                BILL_ZIP_CODE, BILL_TYPE_STRING)
PRODUCT      = product.Product.new_product("test product", "food", \
                description = "test product for person tests")
TEST_PERSON = person.new_person(USERNAME, PASSWORD, FNAME, LNAME, middle_initial = MIDDLE_INITIAL)

#**************************************************************************************************
#**  USERNAME/PASSWORD
#**************************************************************************************************

def person_check_user_pw():
    assert(test_person.test_credentials(USERNAME, PASSWORD) == True), \
        "test_credentials() did not correctly return True given valid inputs for person"

def person_get_username():
    assert(test_person.get_username() == USERNAME), \
        "get_username() did not return username for person"

def person_check_password():
    assert(test_person.check_password(PASSWORD) == True) \
        "check_password() did not return True when given correct password for person"

def person_check_password_invalid():
    assert(test_person.check_password("not valid password") == False) \
        "check_password() did not return False when given incorrect password for person"

# Manipulating username

def person_modify_username():
    # successfully modify own username with unique new username
    new_test_person = new_person("second test person", PASSWORD, FNAME, LNAME, \
        middle_initial = MIDDLE_INITIAL)
    test_person.modify_username("new user")
    assert(test_person.get_username() == "new user"), \
        "modify and get username did not modify and retrieve username for person"

def person_modify_username_with_nonunique_new_username():
    # unsuccessfully modify own username with non-unique new username
    test_person.modify_username("new user")
    assert(test_person.get_username() == 

def person_modify_unauthorized_username():
    # unsuccessfully modify another's username
    test_person = new_person(USERNAME, PASSWORD, FNAME, LNAME, middle_initial = MIDDLE_INITIAL)

# Manipulating password

def person_modify_password():
    # successfully modify own password
    test_person = new_person(USERNAME, PASSWORD, FNAME, LNAME, middle_initial = MIDDLE_INITIAL)

def person_modify_unauthorized_password():
    # unsuccessfully modify another's password
    test_person = new_person(USERNAME, PASSWORD, FNAME, LNAME, middle_initial = MIDDLE_INITIAL)
    pass

#**************************************************************************************************
# NAME
#**************************************************************************************************

def person_get_first_name():
    pass
def person_get_middle_initial():
    pass
def person_get_last_name():
    pass

def person_modify_first_name():
    # successfully modify first name
    pass

def person_modify_first_name_null():
    # unsuccessfully modify first name with null value
    pass

def person_modify_last_name():
    # successfully modify last name
    pass

def person_modify_last_name_null():
    # unsuccessfully modify last name with null value
    pass

def person_modify_middle_initial():
    # successfully modify middle initial
    pass

def person_modify_middle_initial_null():
    # successfully modify middle initial with null value
    pass


#**************************************************************************************************
# JOB TITLE
#**************************************************************************************************

def person_get_job_title():
    # successfully retrieve job title
    pass

def person_modify_job_title():
    # successfully modify staff member's job title (site administrator only)
    pass


#**************************************************************************************************
# SALARY
#**************************************************************************************************

def person_get_salary():
    # successfully retrieve salary
    pass

def person_modify_salary():
    # successfully modify staff member's salary (site administrator only)
    pass

#**************************************************************************************************
# CART and BALANCE
#**************************************************************************************************

def person_get_cart():
    # successfully retrieve cart instance
    pass

def person_get_balance():
    # successfully get balance (as a customer or site administrator only)
    pass

def person_modify_salary_unauthorized():
    # unsuccessfully modify staff member's salary as non-site administrator
    pass

def person_modify_non_staff_salary():
    # unsuccessfully modify non-staff member's salary
    pass

#**************************************************************************************************
# TYPE
#**************************************************************************************************

def person_get_type():
    # successfully retrieve type for person

#**************************************************************************************************
# ADDRESS
#**************************************************************************************************

def get_addresses():
    pass
def remove_address():
    pass
def add_address():
    pass

#**************************************************************************************************
# ORDERS
#**************************************************************************************************

def get_order_history():
    pass
