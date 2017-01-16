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

#**************************************************************************************************
#**  USERNAME/PASSWORD
#**************************************************************************************************

def person_check_user_pw():
    test_person = new_person(FNAME, LNAME, middle_initial = MI
    pass

# Manipulating username

def person_modify_username():
    # successfully modify own username with unique new username
    pass

def person_modify_username_with_nonunique_new_username():
    # unsuccessfully modify own username with non-unique new username
    pass

def person_modify_unauthorized_username():
    # unsuccessfully modify another's username
    pass

# Manipulating password

def person_modify_password():
    # successfully modify own password
    pass

def person_modify_unauthorized_password():
    # unsuccessfully modify another's password
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
