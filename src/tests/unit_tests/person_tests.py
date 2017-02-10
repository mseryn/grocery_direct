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
MIDDLE_INIT = "M"
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


# Ensuring test person doesn't exist before creating
TEST_PERSON = person.check_credentials(USERNAME, PASSWORD)
TEST_STAFF = person.check_credentials(STAFF_USER, PASSWORD)
SECOND_TEST_PERSON = person.check_credentials("second test person", PASSWORD)

if not TEST_PERSON:
    TEST_PERSON  = person.Person.new_person(USERNAME, PASSWORD, FNAME, LNAME, "customer", \
                        middle_initial = MIDDLE_INIT)
if not TEST_STAFF:
    TEST_STAFF   = person.Person.new_person(STAFF_USER, PASSWORD, FNAME, LNAME, "staff", \
                        salary = SALARY, job_title = JOB_TITLE)
if not SECOND_TEST_PERSON:
    SECOND_TEST_PERSON = person.Person.new_person("second test person", PASSWORD, FNAME, LNAME, \
                        "customer", middle_initial = MIDDLE_INIT)

#**************************************************************************************************
#**  USERNAME/PASSWORD
#**************************************************************************************************

def test_person_check_user_pw():
    assert(person.check_credentials(USERNAME, PASSWORD).get_id() == TEST_PERSON.get_id()), \
        "test_credentials() did not correctly return True given valid inputs for person"

def test_person_get_username():
    assert(TEST_PERSON.get_username() == USERNAME), \
        "get_username() did not return username for person"

def test_person_check_password():
    assert(TEST_PERSON.check_password(PASSWORD) == True), \
        "check_password() did not return True when given correct password for person"

def test_person_check_password_invalid():
    assert(TEST_PERSON.check_password("not valid password") == False), \
        "check_password() did not return False when given incorrect password for person"

# Manipulating password

def test_person_modify_password():
    # successfully modify own password
    new_pw = "new password"
    SECOND_TEST_PERSON.modify_password(new_pw)
    checked_person = person.check_credentials("second test person", new_pw)
    SECOND_TEST_PERSON.modify_password(PASSWORD)
    assert(checked_person.get_id() == SECOND_TEST_PERSON.get_id()), \
        "modify_password failed to modify password field and return True for credential check \
        for person"

#**************************************************************************************************
# NAME
#**************************************************************************************************

def test_person_get_first_name():
    assert(TEST_PERSON.get_first_name() == FNAME), \
        "get_first_name failed to return first name for person"

def test_person_get_middle_initial():
    assert(TEST_PERSON.get_middle_initial() == MIDDLE_INIT), \
        "get_middle_initial failed to return middle initial for person"

def test_person_get_last_name():
    assert(TEST_PERSON.get_last_name() == LNAME), \
        "get_last_name failed to return last name for person"

def test_person_modify_first_name():
    new_fname = "new first name"
    SECOND_TEST_PERSON.modify_first_name(new_fname)
    assert(SECOND_TEST_PERSON.get_first_name() == new_fname), \
        "modify_first_name failed to modify first name for person"

def test_person_modify_first_name_null():
    # unsuccessfully modify first name with null value
    TEST_PERSON.modify_first_name(None)
    assert(TEST_PERSON.get_first_name() == FNAME), \
        "modify_first_name failed to handle None entry for first name for person"

def test_person_modify_last_name():
    # successfully modify last name
    new_lname = "new last name"
    SECOND_TEST_PERSON.modify_last_name(new_lname)
    assert(SECOND_TEST_PERSON.get_last_name() == new_lname), \
        "modify_last_name failed to modify last name for person"

def test_person_modify_last_name_null():
    # unsuccessfully modify last name with null value
    TEST_PERSON.modify_last_name(None)
    assert(TEST_PERSON.get_last_name() == LNAME), \
        "modify_last_name failed to handle None enyry for last name for person"

def test_person_modify_middle_initial():
    # successfully modify middle initial
    new_mi = "N"
    SECOND_TEST_PERSON.modify_middle_initial(new_mi)
    assert(SECOND_TEST_PERSON.get_middle_initial() == new_mi), \
        "modify_middle_initial failed to modify middle initial for person"

def test_person_modify_middle_initial_null():
    # successfully modify middle initial with null value
    new_mi = None
    SECOND_TEST_PERSON.modify_middle_initial(new_mi)
    assert(SECOND_TEST_PERSON.get_middle_initial() == new_mi), \
        "modify_middle_initial failed to modify middle initial with None for person"


#**************************************************************************************************
# JOB TITLE
#**************************************************************************************************

def test_person_get_job_title():
    # successfully retrieve job title
    assert(TEST_STAFF.get_job_title() == JOB_TITLE), \
        "get_job_title failed to retrieve job title for person of staff type"

def test_person_get_none_job_title():
    assert(TEST_PERSON.get_job_title() == None), \
        "get_job_title failed to retrieve job title of None for person"

def test_person_modify_job_title():
    # successfully modify staff member's job title
    new_title = "associate sales engineer"
    TEST_STAFF.modify_job_title(new_title)
    returned_title = TEST_STAFF.get_job_title() 
    TEST_STAFF.modify_job_title(JOB_TITLE)
    assert(returned_title == new_title), \
        "modify_job_title failed to modify job title for person"

#**************************************************************************************************
# SALARY
#**************************************************************************************************

def test_person_get_salary():
    # successfully retrieve salary
    assert(TEST_STAFF.get_salary() == SALARY), \
        "get_salary did not retrieve salary for person"

def test_person_modify_salary():
    # successfully modify staff member's salary
    TEST_STAFF.modify_salary(50000)
    returned_salary = TEST_STAFF.get_salary()
    TEST_STAFF.modify_salary(45000)
    assert(returned_salary == 50000), \
        "modify_salary failed to modify person's salary"

#**************************************************************************************************
# CART and BALANCE
#**************************************************************************************************

def test_person_get_None_cart():
    # successfully retrieve None for customer without cart
    assert(TEST_PERSON.get_cart() == None), \
        "get_cart failed to return None for customer person without cart"

def test_person_get_balance():
    # successfully get balance (as a customer or site administrator only)
    assert(TEST_PERSON.get_balance() == 0), \
        "get_balance failed to return zerod balance"

#**************************************************************************************************
# TYPE
#**************************************************************************************************

def test_person_get_type():
    # successfully retrieve type for person
    assert(TEST_STAFF.get_type() == "staff"), \
        "get_type failed to return type for person"

#**************************************************************************************************
# ORDERS
#**************************************************************************************************

def get_order_history():
    pass
