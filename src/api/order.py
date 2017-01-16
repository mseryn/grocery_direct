#***
#*  GroceryDirect - Order API
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

import customer
import product
import address

import datetime.datetime
import cx_Oracle

class Order():
    def __init__(self, given_id):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if isinstance(given_id, int):
            # Ensuring warehouse ID is in warehouses table
            cursor.execute("select id from orders where id = :order_id", order_id = given_id)
            if cursor.fetchone():
                self._id = given_id

            else:
                print("Given ID not in orders table, id: %i" %given_id)
        else:
            print("Given ID not an int, id: %s" %str(given_id))

        db.close()

    @staticmethod
    def new_order(customer):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        returned_id = returned_id = cursor.var(cx_Oracle.NUMBER)
        initial_status = "pending"

        status_id = cursor.fetchone()
        if status_id:
            status_id = status_id[0]

        if isinstance(customer, person.Person):
            cursor.execute("insert into orders (person_id, status_id) \
                            values (:input_pid, :input_sid) \
                            returning id into :output_id", \
                            input_pid = customer.get_id(), input_sid = status_id, \
                            output_id = returned_id)
            db.commit()
        
        db.close()
        return Order(returned_id)

    # Get Methods

    def get_id(self):
        return self._id

    def get_product_list(self):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()
        
        product_list = []

        cursor.execute("select product_id from order_to_product \
                        where order_id = :input_id", \
                        input_id = self.get_id())
        returned_products = cursor.fetchall()

        if returned_products:
            for product_id in returned_products
                product_list.append(product.Product(product_id))

        db.close()
        return product_list

    def get_product_quantity(self, product):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()


        if isinstance(product, product.Product):
            cursor.execute("select id from products where id = :input_pid", \
                            input_pid = product.get_id())
            if cursor.fetchone():
                cursor.execute("select quantity from order_to_product \
                                where order_id = :input_id and product_id = :input_pid", \
                                input_id = self.get_id(), input_pid = product.get_id())
                db.close()
                return cursor.fetchone()[0]
            else:
                db.close()
                return 0

    def get_total_cost(self):
        total_cose = 0
        product_list = self.get_product_list()
        if product_list and self.get_shipping_address():
            for product in product_list:
                total_cost += product.get_price_per_state(self.get_shipping_address().get_state()) \
                              * self.get_product_quantity(product)
        return total_cost

    def get_status(self):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        cursor.execute("select order_statuses.order_status \
                        from order_statuses join orders on order_statuses.id = orders.status_id \
                        where orders.id = :input_id", input_id = self.get_id())
        status_tuple = cursor.fetchone()
        db.close()
        if status_tuple:
            return status_tuple[0]
        else:
            print("Status not found in DB, this should never happen")

    def get_customer(self):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        cursor.execute("select person_id from orders where id = :input_id", \
                        input_id = self.get_id())
        customer_id_tuple = cursor.fetchone()
        db.close()
        if customer_id_tuple:
            return customer.Customer(customer_id_tuple()[0])
        else:
            print("person id was not found, this should never happen")

    def get_shipping_address(self):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        cursor.execute("select shipping_addr_id from orders where id = :input_id", \
                        input_id = self.get_id())
        shipping_id_tuple = cursor.fetchone()
        db.close()
        if shipping_id_tuple:
            return address.Address(shipping_id_tuple[0])
        else:
            print("Shipping address not set for this order.")

    def get_billing_address(self):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        cursor.execute("select billing_addr_id from orders where id = :input_id", \
                        input_id = self.get_id())
        billing_id_tuple = cursor.fetchone()
        db.close()
        if billing_id_tuple:
            return address.Address(billing_id_tuple[0])
        else:
            print("Shipping address not set for this order.")

    def get_submission_date(self):
        db = cx_Oracle.connect("system", "oracle")
        cursor = db.cursor()

        if self.get_status() == "pending":
            print("Order has not yet been submitted.")
            return None

        cursor.execute("select submission_date from orders where id = :input_id", \
                        input_id = self.get_id())
        submission_date_tuple = cursor.fetchone()
        if submission_date_tuple:
            submission_date = submission_date_tuple[0].getvalue()
        db.close()
        return submission_date

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
            print("Status is not valid order status string. \nString given: %s", %(new_status))
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
                cursor.execute("delete from order_to_product
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
                    cursor.execute("delete from order_to_product
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
