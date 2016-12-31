#***
#*  GroceryDirect - Customer Unit Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#***

# ACCOUNT AUTHENTICATION

def person_login():
    # successful login

def person_login_bad_password():
    # incorrect password

def person_login_username_nonexistant():
    # nonexistant username

def person_logout():
    

# ACCOUNT ADMINISTRATION

# Manipulating username

def person_modify_username():
    # successfully modify own username with unique new username

def person_modify_username_with_nonunique_new_username():
    # unsuccessfully modify own username with non-unique new username

def person_modify_unauthorized_username():
    # unsuccessfully modify another's username


# Manipulating password

def person_modify_password():
    # successfully modify own password

def person_modify_unauthorized_password():
    # unsuccessfully modify another's password


# Manipulating address (customer, staff, supplier)

def person_delete_address():
    # 
    pass

def person_delete_nonexistant_address():
    # unsuccessfully delete nonexistant address
    pass

def person_add_address():
    # successfully add address 
    pass

def person_modify_address_street():
    # successfully modify street of address
    pass

def person_modify_address_apt():
    # successfully modify apartment number field of address
    pass

def person_modify_address_city():
    # successfully modify apartment city
    pass

def person_modify_address_zip_code():
    # successfully modify address zip code
    pass

def person_modify_address_state():
    # successfully modify address state
    pass

def person_modify_address_state_invalid_code():
    # unsuccessfully modify address state with invalid state code
    pass

def person_modify_address_street_null():
    # unsuccessfully modify street of address with null value
    pass

def person_modify_address_apt_null():
    # successfully modify apartment number field of address with null value
    pass

def person_modify_address_city_null():
    # unsuccessfully modify apartment city with null value
    pass

def person_modify_address_zip_code_null():
    # unsuccessfully modify address zip code with null value
    pass

def person_modify_address_state_null():
    # unsuccessfully modify address state with null
    pass

def person_modify_default_customer_shipping_address():
    # if customer or site administrator, successfully modify default shipping address
    pass

def person_modify_default_customer_billing_address():
    # if customer or site administrator, successfully modify default billing address
    pass

def person_modify_default_staff_mailing_address():
    # if staff or site administrator, successfully modify default address for staff
    pass

def person_modify_default_warehouse_address():
    # if staff or site administrator, successfully modify default warehouse address
    pass

def person_modify_default_supplier_address():
    # if supplier or site administrator, successfully modify default supplier address
    pass


# Modify name

def person_modify_first_name():
    # successfully modify first name
    pass

def person_modify_middle_initial():
    # successfully modify middle initial
    pass

def person_modify_last_name():
    # successfully modify last name
    pass

def person_modify_first_name_unathorized():
    # unsuccsfully modify another's first name
    pass

def person_modify_middle_intial_unathorized():
    # unsuccessfully modify another's middle initial
    pass

def person_modify_last_name_unauthorized():
    # unsuccessfully modify another's last name
    pass

def person_modify_first_name_null():
    # unsuccessfully modify first name with null value
    pass

def person_modify_middle_initial_null():
    # successfully modify middle initial with null value
    pass

def person_modify_last_name_null():
    # unsuccessfully modify last name with null value
    pass


# ATTRIBUTE MODIFICATION

# Modify cart_id

def person_modify_customer_cart():
    # successfully modify customer's cart ID with valid order ID
    pass

def person_modify_non_customer_cart():
    # unsuccessfully modify a non-customer's cart
    pass

def person_modify_cart_with_null_id():
    # unsuccessfully modify any user type with a null ID
    pass

def person_modify_customer_cart_nonexistant_order_id():
    # unsuccessfully modify customer's cart with nonexistant order ID
    pass

def person_modify_customer_cart_unauthorized():
    # unsuccessfully modify another customer's cart with valid order ID
    pass

def person_modify_customer_cart_unauthorized_order_id():
    # unsuccessfully modify own cart with another's order ID
    pass

# Modify job title

def person_modify_job_title():
    # successfully modify staff member's job title (site administrator only)
    pass

def non_administrator_person_modify_job_title():
    # unsuccessfully modify staff member's job title as a non-site administrator
    pass

# Modify balance

def person_modify_customer_balance():
    # successfully modify customer's balance (as a customer or site administrator only)
    pass

def person_modify_customer_balance_unauthorized():
    # unsuccessfully modify another customer's balance
    pass

def person_modify_customer_balance_with_null():
    # unsuccessfully modify customer balance with null value
    pass

def person_modify_non_customer_blance():
    # unsuccessfully modify staff, warehouse, or site administrator balance
    pass

# Modify salary

def person_modify_salary():
    # successfully modify staff member's salary (site administrator only)
    pass

def person_modify_salary_unauthorized():
    # unsuccessfully modify staff member's salary as non-site administrator
    pass

def person_modify_non_staff_salary():
    # unsuccessfully modify non-staff member's salary
    pass

# Modify account type (should never happen)

def person_modify_person_type_id():
    # unsuccessfully modify person's type ID
    pass


