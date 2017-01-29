#***
#*  GroceryDirect - Address Class
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
import database
import person

class Address():

    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)
        # Ensuring given ID is int
        if isinstance(given_id, int):
            # Ensuring ID is in addresses table
            cursor.execute("select id from addresses where id = :address_id", address_id = given_id)
            if cursor.fetchone():
                self._id = given_id

            else:
                print("Given ID not in addresses table, id: %i" %given_id)
        else:
            print("Given ID not an int, id: %s" %str(given_id))
        database.close()
            
    def new_address(street, city, zip_code, state_code, type_string, input_person = None, \
        credit_card = None, apt_no = None)
        db = database.connect()
        cursor = database.get_cursor(db)

        # Checking input types
        if not isinstance(zip_code, int):
            raise ValueError("Zip code given (%s) not int" %str(zip_code))
        if zip_code > 100000 or zip_code < 0:
            raise ValueError("Zip code given (%i) out of range" %zip_code)

        # Getting type id from type_string
        cursor.execute("select id from address_types where address_type = :input_type", \
                        input_type = type_string)
        type_id = cursor.fetchone()
        if type_id:
            type_id = type_id[0]
        else:
            raise ValueError("Type string given (%s) not valid address type." %(type_string))

        # Getting state id from state_code
        cursor.execute("select id from state_codes where state_code = :input_code", \
                        input_code = str(state_code))
        state_id = cursor.fetchone()
        if state_id:
            state_id = state_id[0]
        else:
            raise ValueError("State code given (%s) not valid state code" %(str(state_code)))

        # Getting peson id from person if specified
        if input_person:
            cursor.execute("select id from persons where id = :input_person_id", \
                            input_person_id = input_person.get_id())
            person_id = cursor.fetchone()
            if person_id:
                person_id = person_id[0]
            else:
                raise ValueError("Person reference passed to address not in persons table.")

        # TODO: get credit card ID once credit card implemented

        returned_id = returned_id = cursor.var(database.cx_Oracle.NUMBER)

        # Making new row in addresses table
        if apt_no:
            if person_id:
                cursor.execute("insert into addresses \
                                (street, apartment_no, city, zip_code, state_code_id, \
                                address_type_id, person_id) \
                                values (:input_street, :input_apt_no, :input_city, :input_zip, \
                                :input_state, :input_type, :input_person) \
                                returning id into :output_id", \
                                input_street = street, input_apt_no = apt_no, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                input_person = person_id, output_id = returned_id)
                database.commit(db)
            elif not person_id:
                cursor.execute("insert into addresses \
                                (street, apartment_no, city, zip_code, state_code_id, \
                                address_type_id) \
                                values (:input_street, :input_apt_no, :input_city, :input_zip, \
                                :input_state, :input_type) \
                                returning id into :output_id", \
                                input_street = street, input_apt_no = apt_no, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                output_id = returned_id)
                database.commit(db)
        elif not apt_no:
            if person_id:
                cursor.execute("insert into addresses \
                                (street, city, zip_code, state_code_id, \
                                address_type_id, person_id) \
                                values (:input_street, :input_city, :input_zip, \
                                :input_state, :input_type, :input_person) \
                                returning id into :output_id", \
                                input_street = street, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                input_person = person_id, output_id = returned_id)
                database.commit(db)
            elif not person_id:
                cursor.execute("insert into addresses \
                                (street, city, zip_code, state_code_id, \
                                address_type_id) \
                                values (:input_street, :input_city, :input_zip, \
                                :input_state, :input_type) \
                                returning id into :output_id", \
                                input_street = street, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                output_id = returned_id)
                database.commit(db)

        returned_id = returned_id.getvalue()
        database.close()
        return Address(returned_id)

    # Get Methods

    def get_id(self):
        return self._id

    def get_person(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select person_id from addresses \
                        where id = :input_id", \
                        input_id = self.get_id())
        person_id = cursor.fetchone()
        database.close(db)

        if person_id:
            person_reference = person.Person(person_id[0])
        else:
            person_reference = None
        return person_reference


    def get_address_string(self):
        apt_no = self.get_apartment_no()
        if apt_no:
            return ", ".join((self.get_street(), apt_no, self.get_city(), \
                " ".join((self.get_state(), str(self.get_zip_code())))))
        else:
            return ", ".join((self.get_street(), self.get_city(), " ".join((self.get_state(), \
                str(self.get_zip_code())))))

    def get_street(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select street from addresses where id = :address_id", \
                        address_id = self.get_id())
        street = cursor.fetchone()[0]
        database.close(db)
        return street

    def get_apartment_no(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select apartment_no from addresses where id = :address_id", \
                        address_id = self.get_id())
        returned_apt_no = cursor.fetchone()
        database.close(db)
        if returned_apt_no:
            return returned_apt_no[0]
        else:
            return None
    
    def get_city(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select city from addresses where id = :address_id", \
                        address_id = self.get_id())
        city = cursor.fetchone()[0]
        database.close(db)
        return street
    
    def get_zip_code(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select zip_code from addresses where id = :address_id", \
                        address_id = self.get_id())
        zip_code = cursor.fetchone()[0]
        database.close(db)
        return zip_code
    
    def get_state(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        # Returns state string not state ID
        cursor.execute("select state_codes.state_code \
                        from state_codes join addresses on state_codes.id = addresses.state_code_id \
                        where addresses.id = :address_id", \
                        address_id = self.get_id())
        database.close(db)
        return cursor.fetchone()[0]

    def get_type(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        # Returns address type in string form not by ID
        cursor.execute("select address_types.address_type \
                        from address_types join addresses \
                        on address_types.id = addresses.address_type_id \
                        where addresses.id = :address_id", \
                        address_id = self.get_id())
        type_string =  cursor.fetchone()[0]
        database.close(db)
        return type_string


    # Modification Methods

    def modify_street(self, new_street):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update addresses \
                        set street = :input_street \
                        where id = :address_id",
                        input_street = new_street, address_id = self.get_id())
        database.commit(db)
        database.close(db)

    def modify_apartment_no(self, new_apt):
        db = database.connect()
        cursor = database.get_cursor(db)
        if new_apt:
            cursor.execute("update addresses \
                            set apartment_no = :input_apt \
                            where id = :address_id",
                            input_apt = new_apt, address_id = self.get_id())
            database.commit(db)
        database.close(db)
    
    def modify_city(self, new_city):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update addresses \
                        set city = :input_city \
                        where id = :address_id",
                        input_city = new_city, address_id = self.get_id())
        database.commit(db)
    
    def modify_zip_code(self, new_zip):
        db = database.connect()
        cursor = database.get_cursor(db)
        if isinstance(new_zip, int) and new_zip >= 0 and new_zip <= 99999:
            cursor.execute("update addresses \
                            set zip_code = :input_zip \
                            where id = :address_id", \
                            input_zip = new_zip, address_id = self.get_id())
            database.commit(db)
            database.close(db)
        else:
            print("Zip code must be a positive 5-digit int. \
                \nInput zip: %s \nInput type: %s" %(str(new_zip), type(new_zip).__name__))
            database.close(db)

    def modify_state(self, new_state):
        db = database.connect()
        cursor = database.get_cursor(db)
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
            database.commit(db)
            database.close(db)
        else:
            print("State code given not found in list of state codes. \nState given: %s" \
                %(new_state))
            database.close(db)
    
    def modify_type(self, new_type):
        db = database.connect()
        cursor = database.get_cursor(db)
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
            database.commit(db)
            database.close(db)
        else:
            print("Address type not found in list of address types. \nType given: %s" \
                %(new_type))
            database.close(db)

    @staticmethod
    def new_address(street, city, state_string, zip_code, type_string, apt_no = None):
        # Inserts a new address into the database
        # Returns Address reference to new address
        db = database.connect()
        cursor = database.get_cursor(db)

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
                database.commit(db)
                return Address(int(returned_id.getvalue()))
        else:
            print("Input type and/or state did not return against DB. \
                \nType string: %s \nState string: %s" %(type_string, state_string))
        database.close(db)


