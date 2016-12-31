#***
#*  GroceryDirect - Customer Unit Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#***

#**************************************************************************************************
#**  ACCOUNT AUTHENTICATION
#**************************************************************************************************

def person_login():
    # successful login

def person_login_bad_password():
    # incorrect password

def person_login_username_nonexistant():
    # nonexistant username

def person_logout():


#**************************************************************************************************
# CREATING ACCOUNTS
#**************************************************************************************************

def person_add_customer_account():
    # successfully add customer account (staff and site administrators only)
    pass

def person_add_staff_account():
    # successfully add staff account (staff and site administrators only)
    pass

def person_add_supplier_account():
    # successfully add supplier account (staff and administrators only)
    pass

def person_add_site_admin_account():
    # successfully add site administrator account (site administrator only)
    pass

def person_delete_account():
    # successfully delete an account (site administrator only)
    pass

def person_delete_default_account():
    # unsuccessfully delete default site administrator account (should never happen)
    pass
    

#**************************************************************************************************
# ACCOUNT ADMINISTRATION
#**************************************************************************************************

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


#**************************************************************************************************
# ATTRIBUTE MODIFICATION
#**************************************************************************************************

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

# Modify credit card

# TODO

#**************************************************************************************************
# INTERACTING WITH PRODUCTS
#**************************************************************************************************

# Modify cart

def person_add_product_to_cart():
    # successfully add product to customer's cart (customer or site administrator only)
    pass

def person_add_product_to_cart_out_of_state():
    # unsuccessfully add product not in warehouse in state to customer's cart
    pass

def person_add_product_to_cart_out_of_stock():
    # unsuccessfully add out of stock product to customer's cart
    pass

def person_add_nonexistant_product_to_cart():
    # unsuccessfully add nonexistant product to customer's cart
    pass

def person_delete_product_from_cart():
    # successfully delete product from customer's cart (customer or site administrator only)
    pass

def person_delete_nonexistant_product_from_cart():
    # successfully return after attempt to delete nonexistant product from cart
    # should never happen - ensure everything behaves in case it does
    pass

def person_modify_product_quantity():
    # successfully modify customer's quantity of product in cart
    pass

def person_modify_product_quantity_to_zero():
    # successfully remove product if quantity set to zero in cart
    pass

def person_modify_product_quantity_negative_number():
    # unsuccessfully modify product quantity in cart if quantity set to non-positive, nonzero value
    pass

# Modify available products (staff and site administrators only)

def person_add_product():
    # successfully add new product
    pass

def person_remove_product():
    # successfully remove product
    pass

def person_remove_nonexisant_product():
    # successfully return from attempt to remove nonexistant product
    pass

def person_modify_product_name():
    # succesfully modify product name
    pass

def person_modify_product_name_null():
    # unsuccessfully modify product name with null value
    pass

def person_modify_product_type():
    # successfully modify product to new type -- WILL INCLUDE ADDING NEW FIELDS
    pass

def person_modify_product_type_nonexistant_type_id():
    # unsuccessfully attempt to modify product type with nonexistant type
    pass

def person_modify_image_id():
    # successfully modify product's image
    pass

def person_modify_image_id_nonexistant():
    # unsuccessfully modify product's image using nonexistant image ID
    pass

def person_modify_product_description():
    # successfully modify product description
    pass

def person_modify 
