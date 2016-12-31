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
    pass

def test_order_status_enum():
    pass

def test_state_codes_enum():

    state_codes_from_file = []
    state_code_text_to_id_from_db = {}

    # Get list of codes from file state_codes.txt
    file_descriptor_state_codes = file.open("state_codes.txt")
    for line in file_descriptor_state_codes:
        state_codes_from_file.append(line.strip())
        
    # Get state code IDs and text from db
    cursor.execute('select * from state_codes')
    for row in cursor:
        state_code_text_to_id_from_db[row[1]] = row[0]
    
    # Ensure all state codes are in dict from db
    for state_code_db in state_code_text_to_id_from_db.keys():
        for state_code_file in state_codes_from_file:
            if state_code_file == state_code_db:
                state_codes_from_file.remove(state_code_file)

    assert(state_codes_from_file == []), "not all state codes stored in database OR retrieval failed"
