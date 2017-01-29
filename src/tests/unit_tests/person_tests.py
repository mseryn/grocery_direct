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

import address
import person
import order

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

STAFF_USER  = "staffuser"
SALARY      = 45000
JOB_TITLE   = "sales engineer"

# Test objects (avoid cluttering db)
SHIP_ADDRESS = address.Address.new_address(SHIP_STREET, SHIP_CITY, SHIP_STATE_CODE, \
                SHIP_ZIP_CODE, SHIP_TYPE_STRING)
BILL_ADDRESS = address.Address.new_address(BILL_STREET, BILL_CITY, BILL_STATE_CODE, \
                BILL_ZIP_CODE, BILL_TYPE_STRING)
TEST_PERSON  = person.Person.new_person(USERNAME, PASSWORD, FNAME, LNAME, "customer", \
                    middle_initial = MIDDLE_INIT)
TEST_STAFF   = person.Person.new_person("teststaff", PASSWORD, FNAME, LNAME, "staff", \
                    salary = SALARY, job_title = JOB_TITLE)

#**************************************************************************************************
#**  USERNAME/PASSWORD
#**************************************************************************************************

def person_check_user_pw():
    assert(test_person.test_credentials(USERNAME, PASSWORD).get_id() == test_person.get_id()), \
        "test_credentials() did not correctly return True given valid inputs for person"

def person_get_username():
    assert(test_person.get_username() == USERNAME), \
        "get_username() did not return username for person"

def person_check_password():
    assert(test_person.check_password(PASSWORD) == True), \
        "check_password() did not return True when given correct password for person"

def person_check_password_invalid():
    assert(test_person.check_password("not valid password") == False), \
        "check_password() did not return False when given incorrect password for person"

# Manipulating username

def person_modify_username():
    # successfully modify own username with unique new username
    test_person.modify_username("new user")
    assert(test_person.get_username() == "new user"), \
        "modify and get username did not modify and retrieve username for person"

def person_modify_username_with_nonunique_new_username():
    # unsuccessfully modify own username with non-unique new username
    new_test_person = person.Person.new_person("second test person", PASSWORD, FNAME, LNAME, \
        middle_initial = MIDDLE_INIT)
    new_test_person.modify_username(USERNAME)
    assert(test_person.get_username() == "second test person"), \
        "modify_username allowed username to be set to non-unique value for person"

# Manipulating password

def person_modify_password():
    # successfully modify own password
    new_pw = "new password"
    new_test_person.modify_password(new_pw)
    assert(test_person.check_credentials("second test person", new_pw) == True), \
        "modify_password failed to modify password field and return True for credential check \
        for person"

#**************************************************************************************************
# NAME
#**************************************************************************************************

def person_get_first_name():
    assert(test_person.get_first_name() == FNAME), \
        "get_first_name failed to return first name for person"

def person_get_middle_initial():
    assert(test_person.get_middle_initial() == MIDDLE_INIT), \
        "get_middle_initial failed to return middle initial for person"

def person_get_last_name():
    assert(test_person.get_last_name() == LNAME), \
        "get_last_name failed to return last name for person"

def person_modify_first_name():
    new_fname = "new first name"
    second_test_person.modify_first_name(new_fname)
    assert(second_test_person.get_first_name() == new_fname), \
        "modify_first_name failed to modify first name for person"

def person_modify_first_name_null():
    # unsuccessfully modify first name with null value
    test_person.modify_first_name(None)
    assert(test_person.get_first_name() == FNAME), \
        "modify_first_name failed to handle None entry for first name for person"

def person_modify_last_name():
    # successfully modify last name
    new_lanme = "new last name"
    second_test_person.modify_last_name(new_lname)
    assert(second_test_person.get_last_name() == new_lname), \
        "modify_last_name failed to modify last name for person"

def person_modify_last_name_null():
    # unsuccessfully modify last name with null value
    test_person.modify_last_name(None)
    assert(test_person.get_last_name() == LNAME), \
        "modify_last_name failed to handle None enyry for last name for person"

def person_modify_middle_initial():
    # successfully modify middle initial
    new_mi = "NI"
    second_test_person.modify_middle_initial(new_mi)
    assert(second_test_person.get_middle_initial() == new_mi), \
        "modify_middle_initial failed to modify middle initial for person"

def person_modify_middle_initial_null():
    # successfully modify middle initial with null value
    new_mi = None
    second_test_person.modify_middle_initial(new_mi)
    assert(second_test_person.get_middle_initial() == new_mi), \
        "modify_middle_initial failed to modify middle initial with None for person"


#**************************************************************************************************
# JOB TITLE
#**************************************************************************************************

def person_get_job_title():
    # successfully retrieve job title
    assert(TEST_STAFF.get_job_title() == JOB_TITLE), \
        "get_job_title failed to retrieve job title for person of staff type"

def person_get_none_job_title():
    assert(TEST_CUSTOMER.get_job_title() == None), \
        "get_job_title failed to retrieve job title of None for person"

def person_modify_job_title():
    # successfully modify staff member's job title
    new_title = "associate sales engineer"
    TEST_STAFF.modify_job_title(new_title)
    assert(TEST_STAFF.get_job_title() == new_title), \
        "modify_job_title failed to modify job title for person"

#**************************************************************************************************
# SALARY
#**************************************************************************************************

def person_get_salary():
    # successfully retrieve salary
    assert(TEST_STAFF.get_salary() == SALARY), \
        "get_salary did not retrieve salary for person"

def person_modify_salary():
    # successfully modify staff member's salary
    TEST_STAFF.modify_salary(50000)
    assert(TEST_STAFF.get_salary() == 50000), \
        "modify_salary failed to modify person's salary"

#**************************************************************************************************
# CART and BALANCE
#**************************************************************************************************

def person_get_None_cart():
    # successfully retrieve None for customer without cart
    assert(TEST_CUSTOMER.get_cart() == None), \
        "get_cart failed to return None for customer person without cart"

def person_add_cart_order():
    # successfully retrieve cart instance
    TEST_CUSTOMER.start_cart()
    assert(isinstance(TEST_CUSTOMER.get_cart(), order.Order)), \
        "start_cart failed to start order object for customer type person"


def person_get_balance():
    # successfully get balance (as a customer or site administrator only)
    TEST_CUSTOMER.add_product_to_cart(PRODUCT)

#**************************************************************************************************
# TYPE
#**************************************************************************************************

def person_get_type():
    # successfully retrieve type for person
    assert(TEST_STAFF.get_type() == "staff"), \
        "get_type failed to return type for person"

#**************************************************************************************************
# ORDERS
#**************************************************************************************************

def get_order_history():
    pass
