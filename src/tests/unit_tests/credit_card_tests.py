#***
#*  GroceryDirect - Credit Card Unit Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#***

import address
import credit_card
import person

import datetime

#************************************************************************************************#
#** DEFAULTS FOR TESTS
#************************************************************************************************#

# Default values for TEST_CARD
CARD_NO     = 1234123456785678 
SEC_CODE    = 321
MONTH       = 8
YEAR        = 2020
TYPE        = "visa"

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
BILL_ADDRESS = address.Address.new_address(BILL_STREET, BILL_CITY, BILL_STATE_CODE, \
                    BILL_ZIP_CODE, BILL_TYPE_STRING)
TEST_PERSON = person.check_credentials(USERNAME, PASSWORD)
if not TEST_PERSON:
    # Since persons are unique, have to be careful when making new test person - might already
    # exist
    TEST_PERSON  = person.Person.new_person(USERNAME, PASSWORD, FNAME, LNAME, "customer", \
                        middle_initial = MIDDLE_INIT)
TEST_CARD = credit_card.CreditCard.new_credit_card(TEST_PERSON, CARD_NO, SEC_CODE, MONTH, \
                    YEAR, TYPE, BILL_ADDRESS)

#**************************************************************************************************
#**  PERSON
#**************************************************************************************************

def test_get_person():
    assert(TEST_CARD.get_person().get_id() == TEST_PERSON.get_id()), \
        "get_person did not return person reference for credit card"

def test_person_through_credit_card():
    card = credit_card.CreditCard(TEST_PERSON.get_credit_cards()[0].get_id())
    assert( isinstance(card, credit_card.CreditCard)), \
        "get credit cards failed in person"

#**************************************************************************************************
#**  CARD NUMBER
#**************************************************************************************************

def test_get_card_no():
    assert(TEST_CARD.get_card_number() == CARD_NO), \
        "get_card_number did not return card number for credit card"

def test_modify_card_no():
    new_number = (9876987698769876) 
    TEST_CARD.modify_card_number(new_number) 
    stored_card_no = TEST_CARD.get_card_number()
    TEST_CARD.modify_card_number(CARD_NO)
    assert(stored_card_no == new_number), \
        "modify_card_number did not modify and return card number for credit card"

#**************************************************************************************************
#**  SECURITY CODE NUMBER
#**************************************************************************************************

def test_check_security_code():
    assert(TEST_CARD.check_security_code(SEC_CODE) == True), \
        "check_security_code did not return True for proper input in credit card"

def test_check_security_code_false():
    assert(TEST_CARD.check_security_code(000) == False), \
        "check_security_code did not return False for improper input in credit card"

def test_modify_security_code():
    new_code = 888
    TEST_CARD.modify_security_code(new_code)
    stored_boolean = TEST_CARD.check_security_code(new_code)
    TEST_CARD.modify_security_code(SEC_CODE)
    assert(stored_boolean == True), \
        "modify_security_code did not modify and return security code in credit card"

#**************************************************************************************************
#**  ADDRESS
#**************************************************************************************************

def test_get_address():
    assert(TEST_CARD.get_address().get_id() == BILL_ADDRESS.get_id()), \
        "get address failed to return correct address id in credit card"

def test_modify_address():
    pass

#**************************************************************************************************
#**  EXPIRATION DATE
#**************************************************************************************************

def test_get_expiration_date():
    returned_date = TEST_CARD.get_expiration_date()
    month = returned_date.month
    year = returned_date.year
    assert(month == MONTH and year == YEAR), \
        "get expiration date failed to return correct expiration date in credit card"

def test_modify_expiration_date():
    new_month = 1
    new_year = 2022
    TEST_CARD.modify_expiration_date(new_month, new_year)
    returned_date = TEST_CARD.get_expiration_date()
    TEST_CARD.modify_expiration_date(MONTH, YEAR)
    month = returned_date.month
    year = returned_date.year
    assert(month == new_month and year == new_year), \
        "modify expiration date failed to modify expiration date in credit card"


#**************************************************************************************************
#**  TYPE
#**************************************************************************************************

def test_get_type():
    assert(TEST_CARD.get_card_type() == TYPE), \
        "get card type failed to return credit card type"

def test_modify_type():
    new_type = "mastercard"
    TEST_CARD.modify_type(new_type)
    stored_type = TEST_CARD.get_card_type()
    TEST_CARD.modify_type(TYPE)
    assert(stored_type == new_type), \
        "modify card type failed to return/modfiy credit card type."
