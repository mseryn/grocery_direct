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
import credit_card
import database
import order

import hashlib

class Person():
    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)

        if isinstance(given_id, (int, float)):
            # Ensuring person's ID is in persons table
            cursor.execute("select id from persons where id = :person_id", person_id = given_id)
            if cursor.fetchone():
                self._id = given_id
            else:
                raise ValueError("Given ID not in persons table, id: %i" %given_id)
                self._id = None

        else:
            if given_id != None:
                raise ValueError("Given ID not an int, id: %s" %str(given_id))
            self._id = None

        database.disconnect(db)

    @staticmethod
    def new_person(username, password, first_name, last_name, type_string, middle_initial = None, \
        salary = None, job_title = None):
        db = database.connect()
        cursor = database.get_cursor(db)
        returned_id = cursor.var(database.cx_Oracle.NUMBER)

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
            # Trimming middle initial
            middle_initial = middle_initial[0]

            cursor.execute("insert into persons \
                            (username, password, first_name, middle_initial, last_name, \
                            person_type_id, balance) \
                            values (:input_username, :input_password, \
                            :input_first, :input_middle, :input_last, :input_type_id, 0) \
                            returning id into :output_id", \
                            input_username = username, input_password = hashed_password, \
                            input_first = first_name, input_middle = middle_initial, \
                            input_last = last_name, input_type_id = type_id, \
                            output_id = returned_id)
            database.commit(db)
        else:
            cursor.execute("insert into persons \
                            (username, password, first_name, last_name, \
                            person_type_id, balance) \
                            values (:input_username, :input_password, \
                            :input_first, :input_last, :input_type_id, 0) \
                            returning id into :output_id", \
                            input_username = username, input_password = hashed_password, \
                            input_first = first_name, \
                            input_last = last_name, input_type_id = type_id, \
                            output_id = returned_id)
            database.commit(db)
                            
        database.disconnect(db)

        returned_id = returned_id.getvalue()
        reference = Person(returned_id)

        if salary:
            reference.modify_salary(salary)
        if job_title:
            reference.modify_job_title(job_title)

        return reference

    # Get Methods

    def get_id(self):
        if self._id:
            return self._id
        else:
            return None

    def get_username(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select username from persons where id = :input_id", \
                        input_id = self.get_id())
        user = cursor.fetchone()[0]

        database.disconnect(db)

        return user

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
        db = database.connect()
        cursor = database.get_cursor(db)
        order_list = []

        cursor.execute("select id from orders \
                        where person_id = :input_id", \
                        input_id = self.get_id())
        orders = cursor.fetchall()

        database.disconnect(db)

        if orders:
            for order_id in orders:
                order_list.append(order.Order(order_id[0]))

        return order_list
        
    def get_cart(self):
        orders = self.get_order_history()
        order_to_return = None
        for this_order in orders:
            if this_order.get_status() == "pending":
                order_to_return = this_order
        if not order_to_return:
            order_to_return = order.Order.new_order(self)
        return order_to_return

    def get_balance(self):
        cart = self.get_cart()
        if cart:
            return cart.get_total_cost()
        return 0

    # Addresses:

    def get_addresses(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        address_list = []

        cursor.execute("select addresses.id \
                        from addresses join persons on addresses.person_id = persons.id \
                        where persons.id = :input_id", input_id = self.get_id())
        addresses = cursor.fetchall()

        database.disconnect(db)

        if addresses:
            for address_id in addresses:
                address_list.append(address.Address(address_id[0]))
        else:
            address_list = []

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

        cursor.execute("select id from addresses \
                        where default_flag = 1 and address_type_id = :input_type \
                        and person_id = :input_pid", \
                        input_type = type_id, input_pid = self.get_id())
        address_id = cursor.fetchone()

        database.disconnect(db)

        if address_id:
            address_reference = address.Address(address_id[0])
        else:
            address_reference = None

        return address_reference

    def get_credit_cards(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        card_list = []
        
        cursor.execute("select credit_cards.id from credit_cards join persons \
                        on persons.id = credit_cards.person_id \
                        where persons.id = :input_id", \
                        input_id = self.get_id())
        all_cards = cursor.fetchall()

        database.disconnect(db)

        if all_cards:
            for card_id in all_cards:
                card_list.append(credit_card.CreditCard(card_id[0]))

        return card_list
        
    def get_balance(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select balance from persons where id = :input_id", input_id = self.get_id())
        current_balance = cursor.fetchone()[0]

        database.commit(db)
        database.disconnect(db)

        return current_balance

    # Modify Methods

    def modify_first_name(self, new_first_name):
        db = database.connect()
        cursor = database.get_cursor(db)

        if new_first_name:
            cursor.execute("update persons \
                            set first_name = :input_name \
                            where id = :input_id",  \
                            input_name = str(new_first_name), input_id = self.get_id())
            database.commit(db)

        database.disconnect(db)

    def modify_middle_initial(self, new_middle_initial):
        db = database.connect()
        cursor = database.get_cursor(db)

        if new_middle_initial:
            cursor.execute("update persons \
                            set middle_initial = :input_name \
                            where id = :input_id",  \
                            input_name = str(new_middle_initial)[0], input_id = self.get_id())
        else:
            cursor.execute("update persons \
                            set middle_initial = NULL where id = :input_id",  \
                            input_id = self.get_id())

        database.commit(db)
        database.disconnect(db)

    def modify_last_name(self, new_last_name):
        db = database.connect()
        cursor = database.get_cursor(db)

        if new_last_name:
            cursor.execute("update persons \
                            set last_name = :input_name \
                            where id = :input_id",  \
                            input_name = str(new_last_name), input_id = self.get_id())
            database.commit(db)

        database.disconnect(db)

    def modify_password(self, new_password):
        db = database.connect()
        cursor = database.get_cursor(db)

        if new_password:
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
                        input_salary = new_salary, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_balance(self, addition):
        db = database.connect()
        cursor = database.get_cursor(db)
        new_balance = self.get_balance() + addition

        cursor.execute("update persons set balance = :input_balance where id = :input_id", \
                        input_balance = new_balance, input_id = self.get_id())

        database.commit(db)
        database.disconnect(db)

    def submit_cart(self):
        cart = self.get_cart()
        cart_id = cart.get_id()
        cost = cart.get_total_cost()
        cart.submit()
        self.modify_balance(cost)
        return cart_id
    
    def modify_job_title(self, new_title):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("update persons \
                        set job_title = :input_title \
                        where id = :input_id",  \
                        input_title = str(new_title), input_id = self.get_id())

        database.commit(db)
        database.disconnect(db)

    def check_password(self, password):
        # give password on person instance, get T/F response
        db = database.connect()
        cursor = database.get_cursor(db)
        
        cursor.execute("select password from persons where id = :input_id", \
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
    

# Helper Methods

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

def hash_password(username, password):
    return (hashlib.md5(username.encode('utf-8') + password.encode('utf-8')).hexdigest())

def get_all_person_types():
    db = database.connect()
    cursor = database.get_cursor(db)
    types = []

    cursor.execute("select person_type from person_types")
    type_tuples = cursor.fetchall()

    database.disconnect(db)

    for type_tuple in type_tuples:
        types.append(type_tuple[0])

    return types
