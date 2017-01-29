#***
#*  GroceryDirect - Person Class
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
#*      -- salary (not customer)
#*      -- job title (not customer)
#*      -- balance (customer only)
#***

import address
import database
import order

import hashlib

class Person():
    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)

        if isinstance(given_id, int):
            # Ensuring warehouse ID is in warehouses table
            cursor.execute("select id from orders where id = :order_id", order_id = given_id)
            if cursor.fetchone():
                self._id = given_id

            else:
                print("Given ID not in orders table, id: %i" %given_id)
        else:
            print("Given ID not an int, id: %s" %str(given_id))

        database.disconnect(db)

    @staticmethod
    def new_person(username, password, first_name, last_name, type_string, middle_initial = None):
        db = database.connect()
        cursor = database.get_cursor(db)

        returned_id = returned_id = cursor.var(database.cx_Oracle.NUMBER)

        # getting person type ID from type_string
        cursor.execute("select id from person_types where person_type = :input_type", \
                        input_type = type_string)
        type_id = cursor.fetchone()
        if type_id:
            type_id = type_id[0]
        else:
            raise ValueError("Type given (%s) not valid person type" %str(type_string))

        hashed_password = hash_password(username, password)
            
        if middle_initial:
            cursor.execute("insert into persons \
                            (username, password, first_name, middle_initial, last_name, \
                            person_type_id) \
                            values (:input_username, :input_password, \
                            :input_first, :input_middle, :input_last, :input_type_id) \
                            returning id into :output_id", \
                            input_username = username, input_password = hashed_password, \
                            input_first = first_name, input_middle = middle_name, \
                            input_last = last_name, input_type_id = type_id, \
                            output_id = returned_id)
            database.commit(db)
        else:
            cursor.execute("insert into persons \
                            (username, password, first_name, last_name, \
                            person_type_id) \
                            values (:input_username, :input_password, \
                            :input_first, :input_last, :input_type_id) \
                            returning id into :output_id", \
                            input_username = username, input_password = hashed_password, \
                            input_first = first_name, \
                            input_last = last_name, input_type_id = type_id, \
                            output_id = returned_id)
            database.commit(db)
                            
        returned_id = returned_id.getvalue()
        database.disconnect(db)
        return Person(returned_id)

    # Get Methods

    def get_id(self):
        return self._id

    def get_type(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select person_types.person_type \
                        from person_types join persons on person_types.id = persons.person_type_id \
                        where persons.id = :input_id", \
                        input_id = self.get_id())
        type_string = cursor.fetchone()[0]
        database.disconnect(db)
        return type_string

    def get_first_name(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select first_name \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        name = cursor.fetchone()[0]
        database.disconnect(db)
        return name

    def get_middle_initial(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select middle_initial \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        middle_initial = cursor.fetchone()
        database.disconnect(db)
        if middle_initial:
            return middle_initial[0]
        else:
            return None

    def get_last_name(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select last_name \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        name = cursor.fetchone()[0]
        database.disconnect(db)
        return name

    def get_salary(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select salary \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        salary = cursor.fetchone()
        database.disconnect(db)
        if salary:
            return salary[0]
        else:
            return None

    def get_job_title(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select job_title \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        title = cursor.fetchone()
        database.disconnect(db)
        if title:
            return title[0]
        else:
            return None

    # Customer attributes:

    def get_order_history(self):
        order_list = []
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select id from orders \
                        where person_id = :input_id", \
                        input_id = self.get_id())
        orders = cursor.fetchall()
        if orders:
            for order_id in orders:
                order_list.append(order.Order(order_id))
        database.disconnect(db)
        return order_list
        
    def get_cart(self):
        orders = self.get_order_history()
        for order in orders:
            if order.get_type() == "pending":
                return order
        return None

    def get_balance(self):
        cart = self.get_cart()
        if cart:
            return cart.get_total_cost()
        return None

    # Addresses:

    def get_addresses(self):
        address_list = []
        
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select addresses.id \
                        from addresses join persons on addresses.person_id = persons.id \
                        where persons.id = :input_id", input_id = self.get_id())
        addresses = cursor.fetchall()

        if addresses:
            for address_id in addresses:
                address_list.append(address.Address(addres_id))
        else:
            address_list = []

        database.disconnect(db)
        return address_list

    def get_default_address(self, type_string):
        # Returns default address of type type_string
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select id from address_types where address_type = :input_str", \
                        input_str = str(type_string))

        type_id = cursor.fetchone()
        if type_id:
            type_id = type_id[0]
        else:
            raise ValueError("Type string given (%s) not valid type" %str(type_string))

        cursor.execute("select default_billing_address from persons \
                        where id = :input_id and address_type_id = :input_type", \
                        input_id = self.get_id(), input_type = type_id)

        address_id = cursor.fetchone()

        database.disconnect(db)

        if address_id:
            address_reference = address.Address(address_id[0])
        else:
            address_reference = None
        return address_reference

    # Modify Methods

    def modify_first_name(self, new_first_name):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update persons \
                        set first_name = :input_name \
                        where id = :input_id",  \
                        input_name = str(new_first_name), input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_middle_initial(self, new_middle_initial):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update persons \
                        set middle_initial = :input_name \
                        where id = :input_id",  \
                        input_name = str(new_middle_initial), input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_last_name(self, new_last_name):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update persons \
                        set last_name = :input_name \
                        where id = :input_id",  \
                        input_name = str(new_last_name), input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_password(self, new_password):
        db = database.connect()
        cursor = database.get_cursor(db)
        hashed_password = hash_password(self.get_username(), new_password)
        cursor.execute("update persons \
                        set password = :input_pw \
                        where id = :input_id",  \
                        input_pw = hashed_password, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)
    
    def modify_salary(self, new_salary):
        db = database.connect()
        cursor = database.get_cursor(db)

        if not isinstance(new_salary, (int, float)):
            raise ValueError("Given salary (%s) is not numeric type" %str(new_salary))
        if new_salary < 0:
            raise ValueError("Given salary (%s) is invalid amount" %str(new_salary))

        cursor.execute("update persons \
                        set salary = :input_salary \
                        where id = :input_id",  \
                        salary = new_salary, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)
    
    def modify_job_title(self, new_title):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update persons \
                        set job_title = :input_title \
                        where id = :input_id",  \
                        input_name = str(new_title), input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def check_password(self, password):
        # give password on person instance, get T/F response
        db = database.connect()
        cursor = database.get_cursor(db)
        
        cursor.execute("select password from persons where id = :inpit_id", \
                        input_id = self.get_id())
        
        hashed_password = cursor.fetchone()
        database.disconnect(db)
        
        if hashed_password:
            hashed_password = hashed_password[0]
        else:
            raise ValueError("This person reference did not map to the table for some reason")

        if hashed_password == hash_password(self.get_username(), password):
            # input password is valid
            return True
        else:
            # input password is invalid
            return False
    
    @staticmethod
    def check_credentials(username, password):
        # Credential check -- give user/password, return user instance or None
        db = database.connect()
        cursor = database.get_cursor(db)
        hashed_password = hash_password(username, password)
        cursor.execute("select id from persons \
                        where username = :input_username and password = :input_pw", \
                        input_username = username, input_pw = hashed_password)
        person_id = cursor.fetchone()
        database.disconnect(db)
        if person_id:
            # Credentials had a match
            person_reference = Person(person_id[0])
        else:
            # Credentials didn't match
            person_reference = None

        return person_reference

    # Helper Methods

    def hash_password(username, password):
        return (hashlib.md5(username.encode('utf-8') + password.encode('utf-8').hexdigest()))
