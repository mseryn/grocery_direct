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

        database.close(db)

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

        hashed_password = hash_password(username, password)
            
        if type_id and middle_initial:
            cursor.execute("insert into persons \
                            (username, password, first_name, middle_initial, last_name, \
                            person_type_id) \
                            values (:input_username, :input_password, \
                            :input_first, :input_middle, :input_last, :input_type_id)
                            returning id into :output_id", \
                            input_username = username, input_password = hashed_password, \
                            input_first = first_name, input_middle = middle_name, \
                            input_last = last_name, input_type_id = type_id, \
                            output_id = returned_id)
            database.commit(db)
        elif type_id and not middle_initial:
            cursor.execute("insert into persons \
                            (username, password, first_name, last_name, \
                            person_type_id) \
                            values (:input_username, :input_password, \
                            :input_first, :input_last, :input_type_id)
                            returning id into :output_id", \
                            input_username = username, input_password = hashed_password, \
                            input_first = first_name, \
                            input_last = last_name, input_type_id = type_id, \
                            output_id = returned_id)
            database.commit(db)
                            
        returned_id = returned_id.getvalue()
        database.close(db)
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
        database.close(db)
        return type_string

    def get_first_name(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select first_name \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        name = cursor.fetchone()[0]
        database.close(db)
        return name

    def get_middle_initial(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select middle_initial \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        middle_initial = cursor.fetchone()
        database.close(db)
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
        database.close(db)
        return name

    def get_salary(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select salary \
                        from persons where persons.id = :input_id", \
                        input_id = self.get_id())
        salary = cursor.fetchone()
        database.close(db)
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
        database.close(db)
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
        database.close(db)
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
                address_list.append(address.Address(addres_id)
        else:
            address_list = []
        return address_list

    def get_default_billing_address(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select default_billing_address from persons \
                        where id = :input_id", input_id = self.get_id())

        address_id = cursor.fetchone()
        database.close(db)

        if address:
            address = address.Address(address_id[0])
        else:
            address = 


    # Modify Methods

    def modify_status(self, new_status):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        cursor.execute("select id from order_statuses where order_status = :input_status", \
                        input_status = new_status)
        status_id_tuple = cursor.fetchone()

        if status_id_tuple:
            status_id = status_id_tuple[0]
            cursor.execute("update orders set status_id = :input_status \
                            where id = :input_id", \
                            input_status = status_id, input_id = self.get_id())
            db.commit()
        else:
            print("Status is not valid order status string. \nString given: %s" %(new_status))
        db.close()

    def modify_shipping_address(self, new_address):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if isinstance(new_address, address.Address):
            cursor.execute("update orders set shipping_addr_id = :input_ship_id \
                            where id = :input_id", \
                            input_ship_id = new_address.get_id(), input_id = self.get_id()) 
            db.commit()
        else:
            print("Requires valid address to set shipping address")
        db.close()

    def modify_billing_address(self, new_address):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if isinstance(new_address, address.Address):
            cursor.execute("update orders set billing_addr_id = :input_bill_id \
                            where id = :input_id", \
                            input_bill_id = new_address.get_id(), input_id = self.get_id()) 
            db.commit()
        else:
            print("Requires valid address to set billing address")
        db.close()

    def add_product(self, new_product):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if isinstance(new_product, product.Product):
            current_quantity = self.get_product_quantity(product)
            if current_quantity == 0:
                # Product not yet in order
                cursor.execute("insert into order_to_product \
                                (order_id, product_id) values (:input_oid, :input_pid)", \
                                input_oid = self.get_id(), input_pid = new_product.get_id())
                db.commit()
            else:
                # Product already in order, incriment quantity
                cursor.execute("update order_to_product set quantity = :input_quantity \
                                where order_id = :input_oid and product_id = :input_pid", \
                                input_quantity = (current_quantity + 1), \
                                input_oid = self.get_id(), input_pid = new_product.get_id())
                db.commit()
        else:
            print("new product must be a product instance")
        db.close()

    def remove_product(self, product):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if isinstance(product, product.Product):
            current_quantity = self.get_product_quantity(product)
            if current_quantity > 1:
                # Product already in order, decriment quantity
                cursor.execute("update order_to_product set quantity = :input_quantity \
                                where order_id = :input_oid and product_id = :input_pid", \
                                input_quantity = (current_quantity - 1), \
                                input_oid = self.get_id(), input_pid = product.get_id())
                db.commit()
            elif current_quantity == 1:
                # Only one product exists, remove row from DB
                cursor.execute("delete from order_to_product \
                                where order_id = :input_oid and product_id = :input_pid", \
                                input_oid = self.get_id(), input_pid = product.get_id())
                db.commit()
            else:
                print("Product does not exist in order, doing nothing")
        else:
            print("product must be a product instance")
        db.close()

    def change_product_quantity(self, product, new_quantity):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if isinstance(new_quantity, int) and new_quantity >= 0:
            
            if isinstance(product, product.Product):
                if new_quantity == 0:
                    # Remove product from table
                    cursor.execute("delete from order_to_product \
                                    where order_id = :input_oid and product_id = :input_pid", \
                                    input_oid = self.get_id(), input_pid = product.get_id())
                    db.commit()
                else:
                    current_quantity = self.get_product_quantity(product)
                    if current_quantity != 0:
                        # Product already exists, just update its quantity
                        cursor.execute("update order_to_product set quantity = :input_quantity \
                                        where order_id = :input_oid and product_id = :input_pid", \
                                        input_quantity = new_quantity, \
                                        input_oid = self.get_id(), input_pid = product.get_id())
                        db.commit()
                    else:
                        # Product doesn't exist, add new row
                        cursor.execute("insert into order_to_product \
                                        (order_id, product_id, quantity) \
                                        values (:input_oid, :input_pid, :input_quantity", \
                                        input_quantity = new_quantity, \
                                        input_oid = self.get_id(), input_pid = product.get_id())
                        db.commit()
            else:
                print("product to change quantity must be valid product in products table")
        else:
            print("specified quantity must be int >= 0 \nquantity given: %i" %(new_quantity))
        db.close()

    def set_submission_date(self):
        # Sets submission date to now
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()
        cursor.execute("update orders set submission_date = :input_date where id = :input_id", \
                        input_date = datetime.datetime.now(), input_id = self.get_id())
        db.commit()
        db.close()

    def hash_password(username, password):
        return (hashlib.md5(username.encode('utf-8') + password.encode('utf-8').hexdigest())
