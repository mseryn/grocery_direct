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
    # 
    pass

def person_modify_middle_name():
    # 
    pass

def person_modify_last_name():
    # 
    pass

def person_modify_first_name_unathorized():
    # 
    pass

def person_modify_middle_name_unathorized():
    # 
    pass

def person_modify_last_name_unauthorized():
    # 
    pass

def person_modify_first_name():
    # 
    pass
