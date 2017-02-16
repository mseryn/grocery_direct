#***
#*  GroceryDirect - Front-End API Class
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#***

import address
import credit_card
import order
import person
import product
import warehouse

import datetime

#*************************************************************************************************
#** GENERAL ACTIONS
#*************************************************************************************************

# Get objects by ID

def get_product(product_id):
    return product.Product(product_id)

def get_warehouse(warehouse_id):
    return warehouse.Warehouse(warehouse_id)

def get_order(order_id):
    return order.Order(order_id)

def get_credit_card(card_id):
    return credit_card.CreditCard(card_id)

def get_person(person_id):
    return person.Person(person_id)

def get_address(address_id):
    return address.Address(address_id)

# Get values out of enum tables

def get_product_types():
    return product.get_product_types()

def get_state_codes():
    return address.get_all_state_codes()

def get_address_types():
    return address.get_all_address_types()

def get_person_types():
    return person.get_all_person_types()

def get_card_types():
    return credit_card.get_all_card_types()

# Manufacture new objects

def make_new_product(name, type_string, description = None, nutrition_facts = None, \
    alcohol_content = None, size = 1, state_code = None, state_price = None):
    # This is a litle different from the API - here, users can specify a state and a price,
    # or the user can specify an invalid state code ALL to set the price for all states.

    new_product = product.Product.new_product(name, type_string, description, \
        nutrition_facts, alcohol_content, size)

    if state_code == "ALL" and state_price:
        new_product.set_price_for_all_states(state_price)
    elif state_code and state_price:
        new_product.modify_price_per_state(state_code, state_price)

    return new_product

def make_new_credit_card(person_reference, card_number, security_code, expiration_month, \
    expiration_year, type_string, address_reference):
    
    new_card = credit_card.CreditCard.new_credit_card(person_reference, card_number, security_code, \
        expiration_month, expiration_year, type_string, address_reference)
    return new_card

def make_new_address(street, city, state_code, zip_code, type_string, input_person, \
    apt_no = None):

    new_address = address.Address.new_address(street, city, state_code, zip_code, type_string, \
        input_person, apt_no)
    return new_address

def make_new_warehouse(capacity, address_reference):
    
    new_warehouse = warehouse.Warehouse.new_warehouse(capacity, address_reference.get_street(), \
        address_reference.get_city(), address_reference.get_state(), address_reference.get_zip_code(), \
        address_reference.get_apartment_no())
    return new_warehouse

def make_new_person(username, password, first_name, last_name, type_string, middle_initial = None, \
    salary = None, job_title = None):
    
    new_person = person.Person.new_person(username, password, first_name, last_name, type_string, middle_initial, \
        salary, job_title)
    return new_person

# Some product utility functions

def set_price_all_states(product_reference, price):
    if not isinstance(product_reference, product.Product):
        return ValueError("product must be product type")
    product.set_price_for_all_states(price)

def set_price_by_state(product_reference, price, state_code):
    if not isinstance(product_reference, product.Product):
        return ValueError("product must be product type")
    product.modify_price_per_state(state_code, price)

def get_all_products():
    """
        Returns list of references to products in given state
    """
    return product.get_all_products()

def get_all_products_by_state(input_state):
    """
        Returns list of references to products in given state
    """
    state_products = []
    all_products = get_all_products()
    for product_reference in all_products:
        if input_state == product_reference.get_state():
            state_products.append(product_reference)
    return state_products

def get_products_by_name(product_name):
    """
        Returns list of references to products with given name
    """
    products_with_name = []
    all_products = get_all_products()
    for product_reference in all_products:
        if product_name.lower().strip() == product_reference.get_name().lower():
            products_with_name.append(product_reference)
    return products_with_name

# Some order utilities

def get_orders():
    # Returns a list of all orders in the system - potentially costly!
    return order.get_all_orders()

def get_orders_by_status(status_string):
    # Returns all orders of a type in the system
    return order.get_all_orders_of_status(status_string)

#*************************************************************************************************
#** USER AUTHENTICATION
#*************************************************************************************************

def login(username, password):
    """
        Returns person reference if username, password combination is a person in the DB, 
        else returns None.
    """
    return person.check_credentials(username, password)

#*************************************************************************************************
#** CUSTOMER ACTIONS
#*************************************************************************************************

def get_cart(customer):
    """
        Gets customer's cart, returns order object. If customer doesn't have cart, starts new
        order and saves as cart.
    """
    # Ensuring customer is person
    if not isinstance(customer, person.Person):
        raise ValueError("Input customer must be person reference.")

    # Seeing if customer has cart
    cart = customer.get_cart()
    if not cart:
        new_cart = order.Order.new_order(customer)
        print("making new cart...")
        cart = customer.get_cart()
    return cart

def cart_add_item(customer, new_product):
    """
        Adds item to customer's cart. Starts new cart if customer doesn't have cart.
    """
    cart = get_cart(customer)
    cart.add_product(new_product)

def cart_remove_item(customer, product_reference):
    """
        Removes item from customer's cart.
    """
    cart = get_cart(customer)
    cart.remove_product(product_reference)

def cart_modify_item_quantity(customer, product_reference, new_quantity):
    """
        Changes quantity of product in cart
    """
    cart = get_cart(customer)
    cart.modify_product_quantity(product_reference, new_quantity)
    

def order_cart(customer):
    """
        Sets status of order to "shipping"
        #TODO incriments customer's total balance by cost of cart
    """
    cart = get_cart(customer)
    cart.modify_status("shipping")

def cancel_cart(customer):
    """
        Sets status of order to "canceled"
    """
    cart = get_cart(customer)
    cart.modify_status("canceled")

#*************************************************************************************************
#** STAFF ACTIONS
#*************************************************************************************************

def add_product(staff, name, type_string, description = None, nutrition_facts = None, \
    alcohol_content = None, size = 1):
    """
        Makes a new product (puts it in the table) and returns a reference to it.
    """
    return product.Product.new_product(name, type_string, description = None, nutrition_facts = \
        None, alcohol_content = None, size = 1)

def modify_product_price(staff, product, new_price, state="ALL", overwrite_flag = True):
    """
        Modifies the price of a product
        Defaults to modifying price for all states
        If overwrite_flag = True, set price regardless of if price already listed.
        If overwrite_flag = False, set price only if price not listed for state.
    """
    if state != "ALL":
        product.modify_price_per_state(self, state, new_price) 
    else:
        product.set_price_for_all_states(new_price, overwrite_flag)

def get_all_warehouses():
    """
        Returns list of references to all warehouses in table
    """
    return warehouse.get_all_warehouses()

def start_new_warehouse(staff, capacity, street, city, state_string, zip_code, \
    apartment_no = None):
    """
        Takes list of user inputs and makes a new warehouse
        Returns reference to the new warehouse
    """
    return warehouse.Warehouse.new_warehouse(capacity, street, city, state_string, zip_code, \
        apartment_no = None)
    

def add_product_to_warehouse(staff, warehouse_ref, product_ref, quantity=1):
    """
        Adds product to warehouse "quantity" number of times.
        Quantity defaults to 1.
    """
    if not isinstance(warehouse_ref, warehouse.Warehouse):
        raise ValueError("Warehouse reference must be valid.")
    if not isinstance(product_ref, product.Product):
        raise ValueError("Product reference must be valid.")
    for _ in range(0, quantity):
        warehouse_ref.add_product(product_ref)

def modify_product_quantity_by_warehouse(staff, warehouse_ref, product_ref, new_quantity):
    """ Modifies product quantity at warehouse """
    # Some quick type-checking:
    if not isinstance(warehouse_ref, warehouse.Warehouse):
        raise ValueError("Warehouse reference must be valid.")
    if not isinstance(product_ref, product.Product):
        raise ValueError("Product reference must be valid.")
    warehouse_ref.modify_quantity(product_ref, new_quantity)

def remove_product_from_warehouse(staff, warehouse_ref, product_ref):
    """ Removes product from warehouse """
    if not isinstance(warehouse_ref, warehouse.Warehouse):
        raise ValueError("Warehouse reference must be valid.")
    if not isinstance(product_ref, product.Product):
        raise ValueError("Product reference must be valid.")
    warehouse_ref.remove_product(product_ref)


#*************************************************************************************************
#** SUPPLIER ACTIONS -- OPTIONAL
#*************************************************************************************************

def supplier_add_product(supplier, product, price):
    pass

def supplier_remove_product(supplier, product):
    pass

#*************************************************************************************************
#** ADMIN ACTIONS
#*************************************************************************************************

def make_new_admin(admin, username, password, first_name, last_name, middle_init \
    = None):
    """ Makes a new administrator """
    type_string = "site administrator"
    return person.Person.new_person(username, password, first_name, last_name, type_string, \
        middle_initial = middle_init)

def make_new_customer(username, password, first_name, last_name, middle_init = None):
    """ Makes new customer """
    type_string = "customer"
    try:
        return person.Person.new_person(username, password, first_name, last_name, type_string, \
            middle_initial = middle_init)
    except:
        pass

def make_new_staff(admin, username, password, first_name, last_name, salary_input, \
    job_title_input, middle_init = None):
    """ Makes new staff member """
    type_string = "staff"
    try:
        return person.Person.new_person(username, password, first_name, last_name, type_string, \
            middle_initial = middle_init, salary = salary_input, job_title = job_title_input)
    except:
        pass

def make_new_supplier(admin, username, password, first_name, last_name, middle_init = None):
    """ Makes new supplier """
    type_string = "supplier"
    try:
        return person.Person.new_person(username, password, first_name, last_name, type_string, \
        middle_initial = middle_init)
    except:
        pass
