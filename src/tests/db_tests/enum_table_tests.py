#***
#*  GroceryDirect - Database Enum Table Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#***

def test_person_types_enum():
    pass


def test_product_types_enum():
    pass


def test_address_types_enum():
    
    file_address_types = []
    db_address_types   = []

    # Get list of address types from file order_statuses.txt
    file_descriptor_address_types = file.open("address_types.txt")
    for line in file_descriptor_address_types:
        file_address_types.append(line.strip())

    # Get address types from db
    cursor.execute('select * from address_types')
    for row in cursor:
        db_address_types.append(row[1])

    # Ensure all address types are in db
    assert(file_address_types.sort() == db_address_types.sort()), "not all address types stored in database OR retrieval failed"


def test_order_status_enum():

    file_order_statuses = []
    db_order_statuses   = []

    # Get list of statuses from file order_statuses.txt
    file_descriptor_order_statuses = file.open("order_statuses.txt")
    for line in file_descriptor_order_statuses:
        file_order_statuses.append(line.strip())

    # Get order statuses from db
    cursor.execute('select * from order_statuses')
    for row in cursor:
        db_order_statuses.append(row[1])

    # Ensure all order statuses are in db
    assert(file_order_statuses.sort() == db_order_statuses.sort()), "not all order statuses stored in database OR retrieval failed"


def test_state_codes_enum():

    file_state_codes = []
    db_state_codes   = []

    # Get list of codes from file state_codes.txt
    file_descriptor_state_codes = file.open("state_codes.txt")
    for line in file_descriptor_state_codes:
        file_state_codes.append(line.strip())
        
    # Get state code IDs and text from db
    cursor.execute('select * from state_codes')
    for row in cursor:
        db_state_codes.append(row[1])
    
    # Ensure all state codes are in db
    assert(file_state_codes.sort() == db_state_codes.sort()), "not all state codes stored in database OR retrieval failed"
