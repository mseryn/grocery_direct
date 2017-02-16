#***
#*  GroceryDirect - Order Class
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Order Description:
#*  - has:
#*      -- customer (owner) 
#*      -- id
#*      -- product list
#*      -- shipping address
#*      -- status
#*      -- placement date -- TODO, how implement?
#*  - get:
#*      -- product list
#*      -- total cost of products
#*      -- shipping address
#*      -- shipping state (for ease) - TODO
#*      -- order placement date
#*      -- order status
#*      -- customer ID
#*  - modify:
#*      -- product quantity -- TODO, vital
#*      -- shipping address
#*      -- order placement date -- TODO, how implement?
#*      -- order status
#*  - add/remove:
#*      -- products from list
#***

import address
import database
import product
import person

import datetime

class Order():
    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)

        if not isinstance(given_id, int):
            raise ValueError("Given ID not an int, id: %s" %str(given_id))

        # Ensuring order ID is in warehouses table
        cursor.execute("select id from orders where id = :order_id", order_id = given_id)
        if cursor.fetchone():
            self._id = given_id

        database.disconnect(db)

    @staticmethod
    def new_order(customer):
        db = database.connect()
        cursor = database.get_cursor(db)

        returned_id = cursor.var(database.cx_Oracle.NUMBER)

        cursor.execute("select id from order_statuses where order_status = :input_status", \
                        input_status = "pending")
        status_id = cursor.fetchone()[0]

        if isinstance(customer, person.Person):
            cursor.execute("insert into orders (person_id, status_id) \
                            values (:input_pid, :input_sid) \
                            returning id into :output_id", \
                            input_pid = customer.get_id(), input_sid = status_id, \
                            output_id = returned_id)
            database.commit(db)


        else:
            raise ValueError("Requires valid person instance")
        
        returned_id = int(returned_id.getvalue())
        this_order = Order(returned_id)

        database.disconnect(db)

        ship_addr = customer.get_default_address("shipping")
        if ship_addr:
            this_order.modify_shipping_address(ship_addr)

        return this_order


    # Get Methods

    def get_id(self):
        return self._id

    def get_products(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        
        product_list = []

        cursor.execute("select product_id from order_to_product \
                        where order_id = :input_id", \
                        input_id = self.get_id())
        returned_products = cursor.fetchall()

        if returned_products:
            for product_id_tuple in returned_products:
                product_list.append(product.Product(product_id_tuple[0]))

        database.disconnect(db)
        return product_list

    def get_product_quantity(self, this_product):
        db = database.connect()
        cursor = database.get_cursor(db)

        if not isinstance(this_product, product.Product):
            raise ValueError("product must be reference to product class")
        cursor.execute("select quantity from order_to_product \
                        where order_id = :input_id and product_id = :input_pid", \
                        input_id = self.get_id(), input_pid = this_product.get_id())
        quantity = cursor.fetchone()
        database.disconnect(db)
        if quantity:
            return quantity[0]
        else:
            return 0

    def get_products_and_quantities(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        
        product_dict = {}

        cursor.execute("select product_id, quantity from order_to_product \
                        where order_id = :input_id", \
                        input_id = self.get_id())
        returned_products = cursor.fetchall()

        if returned_products:
            for product_id_tuple in returned_products:
                product_dict[product.Product(product_id_tuple[0])] = product_id_tuple[1]

        database.disconnect(db)
        return product_dict

    def get_total_cost(self):
        total_cost = 0
        product_list = self.get_products()
        ship_address = self.get_shipping_address()
        if not product_list:
            return 0
        if not ship_address:
            raise ValueError("Order must have shipping address set before total can be given")
        for product in product_list:
            total_cost += product.get_price_per_state(ship_address.get_state()) \
                          * self.get_product_quantity(product)
        return total_cost

    def get_status(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select order_statuses.order_status \
                        from order_statuses join orders on order_statuses.id = orders.status_id \
                        where orders.id = :input_id", input_id = self.get_id())
        status_tuple = cursor.fetchone()
        database.disconnect(db)
        if status_tuple:
            return status_tuple[0]
        else:
            print("Status not found in DB, this should never happen")

    def get_customer(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select person_id from orders where id = :input_id", \
                        input_id = self.get_id())
        customer_id_tuple = cursor.fetchone()
        database.disconnect(db)
        if customer_id_tuple:
            return person.Person(customer_id_tuple[0])
        else:
            print("person id was not found, this should never happen")

    def get_shipping_address(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select shipping_addr_id from orders where id = :input_id", \
                        input_id = self.get_id())
        shipping_id_tuple = cursor.fetchone()
        database.disconnect(db)
        if shipping_id_tuple[0]:
            return address.Address(shipping_id_tuple[0])
        else:
            cust_ship_addr = self.get_customer().get_default_address("shipping")
            if cust_ship_addr:
                self.modify_shipping_address(cust_ship_addr)
                return cust_ship_addr
            print("Shipping address not set for this order.")
            return None

    def get_billing_address(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select billing_addr_id from orders where id = :input_id", \
                        input_id = self.get_id())
        billing_id_tuple = cursor.fetchone()
        database.disconnect(db)
        if billing_id_tuple[0]:
            return address.Address(billing_id_tuple[0])
        else:
            print("Shipping address not set for this order.")
            return None

    def get_submission_date(self):
        db = database.connect()
        cursor = database.get_cursor(db)

        if self.get_status() == "pending":
            return None

        cursor.execute("select submission_date from orders where id = :input_id", \
                        input_id = self.get_id())
        submission_date_tuple = cursor.fetchone()
        if submission_date_tuple:
            submission_date = submission_date_tuple[0]
        database.disconnect(db)
        return submission_date

    # Modify Methods

    def modify_status(self, new_status):
        db = database.connect()
        cursor = database.get_cursor(db)

        cursor.execute("select id from order_statuses where order_status = :input_status", \
                        input_status = new_status)
        status_id_tuple = cursor.fetchone()

        if status_id_tuple:
            status_id = status_id_tuple[0]
            cursor.execute("update orders set status_id = :input_status \
                            where id = :input_id", \
                            input_status = status_id, input_id = self.get_id())
            database.commit(db)
        else:
            print("Status is not valid order status string. \nString given: %s" %(new_status))
        database.disconnect(db)

    def modify_shipping_address(self, new_address):
        db = database.connect()
        cursor = database.get_cursor(db)

        if isinstance(new_address, address.Address):
            cursor.execute("update orders set shipping_addr_id = :input_ship_id \
                            where id = :input_id", \
                            input_ship_id = new_address.get_id(), input_id = self.get_id()) 
            database.commit(db)
        else:
            print("Requires valid address to set shipping address")
        database.disconnect(db)

    def modify_billing_address(self, new_address):
        db = database.connect()
        cursor = database.get_cursor(db)

        if isinstance(new_address, address.Address):
            cursor.execute("update orders set billing_addr_id = :input_bill_id \
                            where id = :input_id", \
                            input_bill_id = new_address.get_id(), input_id = self.get_id()) 
            database.commit(db)
        else:
            print("Requires valid address to set billing address")
        database.disconnect(db)

    def add_product(self, new_product):
        db = database.connect()
        cursor = database.get_cursor(db)

        if not isinstance(new_product, product.Product):
            raise ValueError("product must be reference to product class")
        current_quantity = self.get_product_quantity(new_product)
        if current_quantity == 0:
            # Product not yet in order
            cursor.execute("insert into order_to_product \
                            (order_id, product_id, quantity) \
                            values (:input_oid, :input_pid, 1)", \
                            input_oid = self.get_id(), input_pid = new_product.get_id())
            database.commit(db)
        else:
            # Product already in order, incriment quantity
            cursor.execute("update order_to_product set quantity = :input_quantity \
                            where order_id = :input_oid and product_id = :input_pid", \
                            input_quantity = (current_quantity + 1), \
                            input_oid = self.get_id(), input_pid = new_product.get_id())
            database.commit(db)
        database.disconnect(db)

    def remove_product(self, unwanted_product):
        db = database.connect()
        cursor = database.get_cursor(db)

        if isinstance(unwanted_product, product.Product):
            current_quantity = self.get_product_quantity(unwanted_product)
            if current_quantity > 1:
                # Product already in order, decriment quantity
                cursor.execute("update order_to_product set quantity = :input_quantity \
                                where order_id = :input_oid and product_id = :input_pid", \
                                input_quantity = (current_quantity - 1), \
                                input_oid = self.get_id(), input_pid = unwanted_product.get_id())
                database.commit(db)
            elif current_quantity == 1:
                # Only one product exists, remove row from DB
                cursor.execute("delete from order_to_product \
                                where order_id = :input_oid and product_id = :input_pid", \
                                input_oid = self.get_id(), input_pid = unwanted_product.get_id())
                database.commit(db)
            else:
                print("Product does not exist in order, doing nothing")
        else:
            raise ValueError("product must be a product instance")
        database.disconnect(db)

    def modify_product_quantity(self, new_product, new_quantity):
        db = database.connect()
        cursor = database.get_cursor(db)

        if not isinstance(new_quantity, int):
            raise ValueError("Specified quantity must be an int")
        if new_quantity < 0:
            raise ValueError("New quantity must be >= 0\nquantity given: %i" %(new_quantity))
        if not isinstance(new_product, product.Product):
            raise ValueError("product to change quantity must be valid product in products table")
        if new_quantity == 0:
            # Remove product from table
            cursor.execute("delete from order_to_product \
                            where order_id = :input_oid and product_id = :input_pid", \
                            input_oid = self.get_id(), input_pid = new_product.get_id())
            database.commit(db)
        else:
            current_quantity = self.get_product_quantity(new_product)
            if current_quantity != 0:
                # Product already exists, just update its quantity
                cursor.execute("update order_to_product set quantity = :input_quantity \
                                where order_id = :input_oid and product_id = :input_pid", \
                                input_quantity = new_quantity, \
                                input_oid = self.get_id(), input_pid = new_product.get_id())
                database.commit(db)
            else:
                # Product doesn't exist, add new row
                cursor.execute("insert into order_to_product \
                                (order_id, product_id, quantity) \
                                values (:input_oid, :input_pid, :input_quantity)", \
                                input_oid = self.get_id(), input_pid = new_product.get_id(),
                                input_quantity = new_quantity)
                database.commit(db)
        database.disconnect(db)

    def submit(self):
        # Sets submission date to now
        self.modify_status("shipping")
        db = database.connect()
        cursor = database.get_cursor(db)
        now = datetime.datetime.now()
        now = now.strftime('%d-%b-%Y')
        cursor.execute("update orders set submission_date = :input_date where id = :input_id", \
                        input_date = now, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

def get_all_orders():
    db = database.connect()
    cursor = database.get_cursor(db)
    all_orders = []

    cursor.execute("select id from orders")
    order_tuples = cursor.fetchall()
    
    database.disconnect(db)

    for order_tuple in order_tuples:
        all_orders.append(Order(order_tuple[0]))

    return all_orders

def get_all_orders_of_status(status_string):
    db = database.connect()
    cursor = database.get_cursor(db)
    selected_orders = []

    cursor.execute("select id from order_statuses where order_status = :input_status", \
                    input_status = status_string)
    id_tuple = cursor.fetchone()

    if not id_tuple:
        raise ValueError("%s is not valid order type" %status_string)

    all_orders = get_all_orders()
    for order_ref in all_orders:
        if order_ref.get_status() == status_string:
            selected_orders.append(order_ref)

    return selected_orders
