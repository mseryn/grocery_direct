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
        if not isinstance(given_id, int):
            raise ValueError("ID must be int. Given ID: %s" %str(given_id))

        # Ensuring ID is in addresses table
        cursor.execute("select id from addresses where id = :address_id", address_id = given_id)
        if cursor.fetchone():
            self._id = given_id

        else:
            print("Given ID not in addresses table, id: %i" %given_id)

        database.disconnect(db)
            
    @staticmethod
    def new_address(street, city, state_code, zip_code, type_string, input_person = None, \
        apt_no = None):

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
        person_id = None
        if input_person:
            cursor.execute("select id from persons where id = :input_person_id", \
                            input_person_id = input_person.get_id())
            person_id = cursor.fetchone()
            if person_id:
                person_id = person_id[0]
            else:
                raise ValueError("Person reference passed to address not in persons table.")

        returned_id = returned_id = cursor.var(database.cx_Oracle.NUMBER)

        # Making new row in addresses table
        if apt_no:

            if person_id:
                cursor.execute("insert into addresses \
                                (street, apartment_no, city, zip_code, state_code_id, \
                                address_type_id, person_id, default_flag) \
                                values (:input_street, :input_apt_no, :input_city, :input_zip, \
                                :input_state, :input_type, :input_person, :input_flag) \
                                returning id into :output_id", \
                                input_street = street, input_apt_no = apt_no, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                input_person = person_id, input_flag = 0, output_id = returned_id)
                database.commit(db)

            elif not person_id:
                cursor.execute("insert into addresses \
                                (street, apartment_no, city, zip_code, state_code_id, \
                                address_type_id, default_flag) \
                                values (:input_street, :input_apt_no, :input_city, :input_zip, \
                                :input_state, :input_type, :input_flag) \
                                returning id into :output_id", \
                                input_street = street, input_apt_no = apt_no, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                input_flag = 0, output_id = returned_id)
                database.commit(db)
        elif not apt_no:

            if person_id:
                cursor.execute("insert into addresses \
                                (street, city, zip_code, state_code_id, \
                                address_type_id, person_id, default_flag) \
                                values (:input_street, :input_city, :input_zip, \
                                :input_state, :input_type, :input_person, :input_flag) \
                                returning id into :output_id", \
                                input_street = street, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                input_person = person_id, input_flag = 0, output_id = returned_id)
                database.commit(db)

            elif not person_id:
                cursor.execute("insert into addresses \
                                (street, city, zip_code, state_code_id, \
                                address_type_id, default_flag) \
                                values (:input_street, :input_city, :input_zip, \
                                :input_state, :input_type, :input_flag) \
                                returning id into :output_id", \
                                input_street = street, input_city = city, \
                                input_zip = zip_code, input_state = state_id, input_type = type_id, \
                                input_flag = 0, output_id = returned_id)
                database.commit(db)

        returned_id = int(returned_id.getvalue())
        database.disconnect(db)

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

        database.disconnect(db)

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

        database.disconnect(db)

        return street

    def get_apartment_no(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select apartment_no from addresses where id = :address_id", \
                        address_id = self.get_id())
        returned_apt_no = cursor.fetchone()

        database.disconnect(db)

        if returned_apt_no and returned_apt_no[0]:
            return returned_apt_no[0]
        else:
            return ""
    
    def get_city(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select city from addresses where id = :address_id", \
                        address_id = self.get_id())
        city = cursor.fetchone()[0]

        database.disconnect(db)

        return city
    
    def get_zip_code(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select zip_code from addresses where id = :address_id", \
                        address_id = self.get_id())
        zip_code = cursor.fetchone()[0]

        database.disconnect(db)

        return zip_code
    
    def get_state(self):
        # Returns state string not state ID
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select state_codes.state_code \
                        from state_codes join addresses on state_codes.id = addresses.state_code_id \
                        where addresses.id = :address_id", \
                        address_id = self.get_id())
        state_string = cursor.fetchone()[0]

        database.disconnect(db)

        return state_string

    def get_type(self):
        # Returns address type in string form not by ID
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select address_types.address_type \
                        from address_types join addresses \
                        on address_types.id = addresses.address_type_id \
                        where addresses.id = :address_id", \
                        address_id = self.get_id())
        type_string =  cursor.fetchone()[0]

        database.disconnect(db)

        return type_string

    def get_default_flag(self):
        # Returns True/False based on 1/0 value in table
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select default_flag from addresses \
                        where id = :input_id", \
                        input_id = self.get_id())
        flag = cursor.fetchone()[0]

        database.disconnect(db)

        if flag == 0:
            return False
        elif flag == 1:
            return True
        else:
            raise ValueError("This should have returned 1 or 0, major error, should never happen" \
                + "\nValue returned: %s" %str(flag))


    # Modification Methods

    def add_person(self, new_person):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select id from persons where id = :input_id", \
                        input_id = new_person.get_id())
        if cursor.fetchone():
            # The person exists
            cursor.execute("update addresses set person_id = :input_p_id \
                            where id = :input_id", \
                            input_p_id = new_person.get_id(), input_id = self.get_id())
            database.commit(db)

        else:
            raise ValueError("Person does not exist")

        database.disconnect(db)

    def set_default_flag(self, state):
        if state != True and state != False:
            raise ValueError("Requires True or False")

        if state == True:
            flag = 1
        elif state == False:
            flag = 0

        db = database.connect()
        cursor = database.get_cursor(db)

        # Get id of own type
        cursor.execute("select id from address_types where address_type = :input_type", \
                        input_type = self.get_type())
        type_id = cursor.fetchone()[0]

        if state == True and self.get_person():
            # If address has a person remove other true flags so only one remains of this type
            cursor.execute("update addresses set default_flag = 0 \
                            where person_id = :input_id and default_flag = 1 \
                            and address_type_id = :input_tid", \
                            input_id = self.get_person().get_id(), input_tid = type_id)
            database.commit(db)

        cursor.execute("update addresses set default_flag = :input_flag \
                        where id = :input_id", \
                        input_flag = flag, input_id = self.get_id())

        database.commit(db)
        database.disconnect(db)

    def modify_street(self, new_street):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("update addresses \
                        set street = :input_street \
                        where id = :address_id",
                        input_street = new_street, address_id = self.get_id())

        database.commit(db)
        database.disconnect(db)

    def modify_apartment_no(self, new_apt):
        db = database.connect()
        cursor = database.get_cursor(db)

        if new_apt != None:
            cursor.execute("update addresses \
                            set apartment_no = :input_apt \
                            where id = :address_id",
                            input_apt = new_apt, address_id = self.get_id())
            database.commit(db)

        database.disconnect(db)
    
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

        else:
            print("Zip code must be a positive 5-digit int. \
                \nInput zip: %s \nInput type: %s" %(str(new_zip), type(new_zip).__name__))

        database.disconnect(db)

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

        else:
            print("State code given not found in list of state codes. \nState given: %s" \
                %(new_state))

        database.disconnect(db)
    
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

        else:
            print("Address type not found in list of address types. \nType given: %s" \
                %(new_type))
        database.disconnect(db)

    def remove(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("delete from addresses where id = :input_id", input_id = self.get_id())

        database.commit(db)
        database.disconnect(db)

def get_all_state_codes():
    db = database.connect()
    cursor = database.get_cursor(db)
    codes = []

    cursor.execute("select state_code from state_codes")
    code_tuples = cursor.fetchall()

    database.disconnect(db)

    for code_tuple in code_tuples:
        codes.append(code_tuple[0])

    return codes 

def get_all_address_types():
    db = database.connect()
    cursor = database.get_cursor(db)
    codes = []

    cursor.execute("select address_type from address_types")
    code_tuples = cursor.fetchall()

    database.disconnect(db)

    for code_tuple in code_tuples:
        codes.append(code_tuple[0])
    return codes 

def get_all_addresses():
    db = database.connect()
    cursor = database.get_cursor(db)
    address_list = []

    cursor.execute("select id from addresses")
    address_tuples = cursor.fetchall()
    
    database.disconnect(db)
    
    for address_tuple in address_tuples:
        address_list.append(address.Address(address_tuple[0]))
    
    return address_list

def get_all_addresses_of_type(type_string):
    db = database.connect()
    cursor = database.get_cursor(db)
    address_list = []
    
    cursor.execute("select id from address_types where address_type = :input_type", \
                    input_type = type_string)
    type_tuple = cursor.fetchone()
    if not type_tuple:
        raise ValueError("given string %s not a valid address type" %type_string)

    cursor.execute("select id from addresses where address_type_id = :input_id", \
                    input_id = type_tuple[0])
    address_tuples = cursor.fetchall()

    database.disconnect(db)

    for address_tuple in address_tuples:
        address_list.append(address.Address(address_tuple[0]))

    return address_list
