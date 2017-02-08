#***
#*  GroceryDirect - Warehouse Class
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*  
#*  Warehouse Description:
#*  - has:
#*      -- id
#*      -- address (id)
#*      -- capacity
#*      -- stock (with prices set by state)
#*  - get:
#*      -- address (id)
#*      -- capacity
#*  - modify:
#*      -- address (id)
#*      -- capacity
#***

import address
import database
import product


class Warehouse():

    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)
        # Ensuring given ID is int
        if isinstance(given_id, int):
            # Ensuring warehouse ID is in warehouses table
            cursor.execute("select id from warehouses where id = :warehouse_id", warehouse_id = given_id)
            if cursor.fetchone():
                self._id = given_id
            else:
                raise ValueError("Given ID not in warehouses table, id: %i" %given_id)
        else:
            raise ValueError("Given ID not an int, id: %s" %str(given_id))
        database.disconnect(db)

    @staticmethod
    def new_warehouse(capacity, street, city, state_string, zip_code, apartment_no = None):
        # Adding new warehouse to database, and returning reference to that warehouse
        db = database.connect()
        cursor = database.get_cursor(db)
        warehouse_address = address.Address.new_address(street, city, state_string, zip_code,\
            "warehouse", apt_no = apartment_no)
        address_id = warehouse_address.get_id()

        if isinstance(capacity, (int, float)):
            returned_id = cursor.var(database.cx_Oracle.NUMBER)
            capacity = int(capacity)
            cursor.execute("insert into warehouses \
                            (capacity, address_id) values (:input_capacity, :input_address) \
                            returning id into :new_warehouse_id", \
                            input_capacity = capacity, input_address = address_id, \
                            new_warehouse_id = returned_id)
            database.commit(db)

        returned_id = int(returned_id.getvalue())

        database.disconnect(db)
        return Warehouse(returned_id)

    # Get Methods

    def get_id(self):
        return self._id

    def get_capacity(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select capacity from warehouses where id = :warehouse_id", \
                        warehouse_id = self.get_id())
        cap = cursor.fetchone()[0]
        database.disconnect(db)
        return cap

    def get_stock(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        stock = []
        cursor.execute("select product_id \
                        from warehouses join warehouse_to_product \
                        on warehouses.id = warehouse_to_product.warehouse_id \
                        where warehouses.id = :warehouse_id", warehouse_id = self.get_id())
        product_list = cursor.fetchall()
        if product_list:
            for product_id in product_list:
                stock.append(product.Product(int(product_id[0])))
        database.disconnect(db)
        return stock

    def get_product_quantity(self, product):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select quantity \
                        from warehouses join warehouse_to_product \
                        on warehouses.id = warehouse_to_product.warehouse_id \
                        where warehouses.id = :warehouse_id \
                        and warehouse_to_product.product_id = :input_product", \
                        warehouse_id = self.get_id(), input_product = product.get_id())
        product_quantity = cursor.fetchone()
        if product_quantity:
            return product_quantity[0]
        else:
            return 0

    def get_remaining_capacity(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        total_used_space = 0
        for product in self.get_stock():
            total_used_space += product.get_size() * self.get_product_quantity(product)
        remaining_cap = self.get_capacity() - total_used_space
        database.disconnect(db)
        return remaining_cap

    def get_address(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select address_id from warehouses where id = :warehouse_id", \
                        warehouse_id = self.get_id())
        returned_id = cursor.fetchone()
        if returned_id:
            returned_id = returned_id[0]
            database.disconnect(db)
            if isinstance(returned_id, int):
                warehouse_address = address.Address(returned_id)
                return warehouse_address
        else:
            database.disconnect(db)
            return None

    # Modification Methods

    def modify_capacity(self, new_capacity):
        db = database.connect()
        cursor = database.get_cursor(db)
        if isinstance(new_capacity, (int, float)):
            if new_capacity >=0:
                if new_capacity >= (self.get_capacity() - self.get_remaining_capacity()):
                    cursor.execute("update warehouses set capacity = :input_capacity \
                                    where id = :warehouse_id", input_capacity = int(new_capacity), \
                                    warehouse_id = self.get_id())
                    database.commit(db)
                else:
                    raise ValueError("New capacity must be >= remaining capacity")
            else:
                raise ValueError("Capacity must be >=0")
        else:
            raise ValueError("New capacity must be integer \nInput capacity: %s" %(str(new_capacity)))
        database.disconnect(db)

    def add_product(self, new_product):
        db = database.connect()
        cursor = database.get_cursor(db)
        product_id = new_product.get_id()
        cursor.execute("select quantity from warehouse_to_product \
                        where product_id = :input_pid and warehouse_id = :input_wid", \
                        input_pid = product_id, input_wid = self.get_id())
        current_quantity = cursor.fetchone()
        if current_quantity:
            # The item is already in this table in the DB, just incriment quantity
            incrimented_quantity = int(current_quantity[0]) + 1
            cursor.execute("update warehouse_to_product set quantity = :input_quantity \
                            where product_id = :input_pid and warehouse_id = :input_wid", \
                            input_quantity = incrimented_quantity, input_pid = product_id, \
                            input_wid = self.get_id())
            database.commit(db)
            database.disconnect(db)
        else:
            # The item is not yet in the warehouse's stock, so add it to the table
            cursor.execute("insert into warehouse_to_product (product_id, warehouse_id, quantity) \
                            values (:input_pid, :input_wid, :input_quantity)", \
                            input_pid = product_id, input_wid = self.get_id(), input_quantity = 1)
            database.commit(db)
            database.disconnect(db)

    def remove_product(self, product):
        db = database.connect()
        cursor = database.get_cursor(db)
        product_id = product.get_id()
        cursor.execute("select quantity from warehouse_to_product \
                        where product_id = :input_pid and warehouse_id = :input_wid", \
                        input_pid = product_id, input_wid = self.get_id())
        current_quantity = cursor.fetchone()

        if current_quantity:
            # The item is already in this table in the DB, just decriment quantity
            decrimented_quantity = int(current_quantity[0]) - 1
            if decrimented_quantity > 0:
                # Removing one will not remove all instances of that product
                cursor.execute("update warehouse_to_product set quantity = :input_quantity \
                                where product_id = :input_pid and warehouse_id = :input_wid", \
                                input_quantity = decrimented_quantity, input_pid = product_id, \
                                input_wid = self.get_id())
                database.commit(db)
            else:
                # Remove the line from the DB if product has quantity of zero
                cursor.execute("delete from warehouse_to_product \
                                where product_id = :input_pid and warehouse_id = :input_wid", \
                                input_pid = product_id, input_wid = self.get_id())
                database.commit(db)
        else:
            # The item is not yet in the warehouse's stock, so do nothing
            pass
        database.disconnect(db)

    def modify_quantity(self, product, new_quantity):
        db = database.connect()
        cursor = database.get_cursor(db)
        if isinstance(new_quantity, int) and new_quantity >= 0:
            product_id = product.get_id()
            cursor.execute("select quantity from warehouse_to_product \
                            where product_id = :input_pid and warehouse_id = :input_wid", \
                            input_pid = product_id, input_wid = self.get_id())
            current_quantity = cursor.fetchone()

            if current_quantity:
                # Ensuring product is in warehouse stock
                current_quantity = int(current_quantity[0])
                if current_quantity == new_quantity:
                    # Do nothing if quantity doesn't change
                    pass
                elif new_quantity == 0: 
                    # Remove line in DB is new quantity is zero
                    cursor.execute("delete from warehouse_to_product \
                                    where product_id = :input_pid and warehouse_id = :input_wid", \
                                    input_pid = product_id, input_wid = self.get_id())
                    database.commit(db)
                else:
                    # Otherwise just update the quantity
                    cursor.execute("update warehouse_to_product set quantity = :input_quantity \
                                    where product_id = :input_pid and warehouse_id = :input_wid", \
                                    input_quantity = new_quantity, input_pid = product_id, \
                                    input_wid = self.get_id())
                    database.commit(db)
        else:
            raise ValueError("new quantity must be positive integer value")
        database.disconnect(db)
