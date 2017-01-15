#***
#*  GroceryDirect - Address Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Addresses:
#*  have:
#*      -- street
#*      -- apt (optional)
#*      -- city
#*      -- state
#*      -- zip code
#*      -- type
#*  get:
#*      -- street
#*      -- apt (if exists)
#*      -- city
#*      -- state
#*      -- zip code
#*      -- full address string?
#*      -- type
#*  modify:
#*      -- street
#*      -- apt
#*      -- city
#*      -- state
#*      -- zip code
#*      -- type
#***


import cx_Oracle

# Starting up interaction with database:
db = cx_Oracle.connect('system', 'oracle')
cursor = db.cursor()

class Address():

    def __init__(self, given_id):
        # Ensuring given ID is int
        if isinstance(given_id, int):
            # Ensuring warehouse ID is in warehouses table
            cursor.execute("select id from addresses where id = :address_id", address_id = given_id)
            if cursor.fetchone():
                self._id = given_id

            else:
                print("Given ID not in addresses table, id: %i" %given_id)
        else:
            print("Given ID not an int, id: %s" %str(given_id))
    

    # Get Methods

    def get_id(self):
        return self._id

    def get_street(self):
        cursor.execute("select street from addresses where id = :address_id", \
                        address_id = self.get_id())
        return cursor.fetchone()[0]

    def get_apartment_no(self):
        cursor.execute("select apartment_no from addresses where id = :address_id", \
                        address_id = self.get_id())
        returned_apt_no = cursor.fetchone()
        if returned_apt_no:
            return returned_apt_no[0]
        else:
            return None
    
    def get_city(self):
        cursor.execute("select city from addresses where id = :address_id", \
                        address_id = self.get_id())
        return cursor.fetchone()[0]
    
    def get_zip_code(self):
        cursor.execute("select zip_code from addresses where id = :address_id", \
                        address_id = self.get_id())
        return cursor.fetchone()[0]
    
    def get_state(self):
        # Returns state string not state ID
        cursor.execute("select state_codes.state_code \
                        from state_codes join addresses on state_codes.id = addresses.state_code_id \
                        where addresses.id = :address_id", \
                        address_id = self.get_id())
        return cursor.fetchone()[0]

    def get_type(self):
        # Returns address type in string form not by ID
        cursor.execute("select address_types.address_type \
                        from address_types join addresses \
                        on address_types.id = addresses.address_type_id \
                        where addresses.id = :address_id", \
                        address_id = self.get_id())
        return cursor.fetchone()[0]


    # Modification Methods

    def modify_street(self, new_street):
        cursor.execute("update addresses \
                        set street = :input_street \
                        where id = :address_id",
                        input_street = new_street, address_id = self.get_id())
        db.commit()

    def modify_apartment_no(self, new_apt):
        if new_apt:
            cursor.execute("update addresses \
                            set apartment_no = :input_apt \
                            where id = :address_id",
                            input_apt = new_apt, address_id = self.get_id())
            db.commit()
    
    def modify_city(self, new_city):
        cursor.execute("update addresses \
                        set city = :input_city \
                        where id = :address_id",
                        input_city = new_city, address_id = self.get_id())
        db.commit()
    
    def modify_zip_code(self, new_zip):
        if isinstance(new_zip, int) and new_zip >= 0 and new_zip <= 99999:
            cursor.execute("update addresses \
                            set zip_code = :input_zip \
                            where id = :address_id", \
                            input_zip = new_zip, address_id = self.get_id())
            db.commit()
        else:
            print("Zip code must be a positive 5-digit int. \
                \nInput zip: %s \nInput type: %s" %(str(new_zip), type(new_zip).__name__))

    def modify_state(self, new_state):
        cursor.execute("select id from state_codes where state_code = :input_state", \
                        input_state = new_state)
        state_id = cursor.fetchone()
        if state_id:
            state_id = state_id[0]
        if isinstance(state_id, int):
            cursor.execute("update addresses \
                            set state_code_id = :input_state \
                            where id = :address_id", \
                            input_state = state_id, address_id = self.get_id())
            db.commit()
        else:
            print("State code given not found in list of state codes. \nState given: %s" \
                %(new_state))
    
    def modify_type(self, new_type):
        # Verify it's a valid type (in the table) - selection should return nothing if type invalid
        cursor.execute("select id from address_types where address_type = :input_type", \
                        input_type = new_type)
        type_id = cursor.fetchone()
        if type_id:
            type_id = type_id[0]
        if isinstance(type_id, int):
            cursor.execute("update addresses \
                            set address_type_id = :input_type \
                            where id = :address_id", \
                            input_type = type_id, address_id = self.get_id())
            db.commit()
        else:
            print("Address type not found in list of address types. \nType given: %s" \
                %(new_type))

    @staticmethod
    def new_address(street, city, state_string, zip_code, type_string, apt_no = None):
        # Inserts a new address into the database
        # Returns Address reference to new address

        # Getting type_id from type_string
        cursor.execute("select id from address_types where address_type = :input_type", \
            input_type = type_string)
        type_id = cursor.fetchone()

        # Getting state_id from state_string
        cursor.execute("select id from state_codes where state_code = :input_state", \
            input_state = state_string)
        state_id = cursor.fetchone()

        # Ensuring both state and type IDs exist and are ints
        if type_id and state_id:
            type_id = type_id[0]
            state_id = state_id[0]
            if isinstance(type_id, int) and isinstance(state_id, int):
                # Making a variable to hold ID of new address
                returned_id = cursor.var(cx_Oracle.NUMBER)

                # If apartment_no specified, use first statement. Otherwise, use second.
                if apt_no:
                    cursor.execute("insert into addresses \
                        (street, apartment_no, city, zip_code, state_code_id, address_type_id) \
                        values (:input_street, :input_apt, :input_city, :input_zip, :input_state, \
                        :input_type) \
                        returning id into :new_address_id", \
                        input_street = street, input_apt = apt_no, input_city = city, \
                        input_zip = zip_code, input_state = state_id, input_type = type_id, \
                        new_address_id = returned_id)
                else:
                    cursor.execute("insert into addresses \
                        (street, city, zip_code, state_code_id, address_type_id) \
                        values (:input_street, :input_city, :input_zip, :input_state, :input_type) \
                        returning id into :new_address_id", \
                        input_street = street, input_city = city, \
                        input_zip = zip_code, input_state = state_id, input_type = type_id, \
                        new_address_id = returned_id)

                # Committing changes to DB and collecting return variable
                db.commit()
                return Address(int(returned_id.getvalue()))
        else:
            print("Input type and/or state did not return against DB. \
                \nType string: %s \nState string: %s" %(type_string, state_string))


