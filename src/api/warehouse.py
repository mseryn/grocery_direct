#***
#*  GroceryDirect - Warehouse API
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
import product

import cx_Oracle

# Starting up interaction with database:
db = cx_Oracle.connect('system', 'oracle')
cursor = db.cursor()

class Warehouset():

    def __init__(self, capacity, street, city, state_string, zip_code, apartment_no = None):
        db = cx_Oracle.connect('system', 'oracle')
        cursor = db.cursor()

        warehouse_address = address.Address(street, city, state_string, zip_code, "warehouse", \
                                            apt_no = apartment_no)
        address_id = warehouse_address.get_id()

        if isinstance(capacity, (int, float)):
            returned_id = cursor.var(cx_Oracle.NUMBER)
            capacity = int(capacity)
            cursor.execute("insert into warehouses \
                            (capacity, address_id) values (:input_capacity, :input_address) \
                            returning id into :new_warehouse_id", \
                            input_capacity = capacity, input_address = address_id, \
                            new_warehouse_id = returned_id)
            db.commit()

        _id = returned_id

    # Get Methods

    def get_id(self):
        return self._id

    def get_capacity(self):
        cursor.execute("select capacity from warehouses where id = :warehouse_id", \
                        warehouse_id = self.get_id())
        return cursor.fetchone()[0]

    # Address-Get Methods

    def get_address(self):
        address = self.get_address_reference()
        return address.get_address_string()

    def get_street(self):
        address = self.get_address_reference()
        return address.get_street()

    def get_apartment_no(self)
        address = self.get_address_reference()
        return address.get_apartment_no()

    def get_city(self):
        address = self.get_address_reference()
        return address.get_city()

    def get_state(self):
        address = self.get_address_reference()
        return address.get_state()

    def get_zip_code(self):
        address = self.get_address_reference()
        return address.get_zip_code()

    # Modification Methods

    def modify_capacity(self, new_capacity):
        if isinstance(new_capacity, (int, float)):
            # Ensuring new capacity is >= remaining capacity -- TODO
            cursor.execute("update warehouses set capacity = :input_capacity \
                            where id = :warehouse_id", input_capacity = int(new_capacity), \
                            warehouse_id = self.get_id())
            db.commit()
        else:
            print("New capacity must be integer \nInput capacity: %s" %(str(new_capacity)))

    def modify_street(self, new_street):
        address = self.get_address_reference()
        address.modify_street(new_street)

    def modify_apartment_no(self, new_apt):
        address = self.get_address_reference()
        address.modify_apartment_no(self, new_apt)

    def modify_city(self, new_city):
        address = self.get_address_reference()
        address.modify_city(new_city)

    def modify_state(self, new_state):
        address = self.get_address_reference()
        address.modify_state(new_state)

    def modify_zip_code(self, new_zip):
        address = self.get_address_reference()
        address.modify_zip_code(new_zip)

    # Helper Methods

    def get_address_reference(self):
        cursor.execute("select address_id from warehouses where id = :warehouse_id", \
                        warehouse_id = self.get_id())
        returned_id = cursor.fetchone()
        if returned_id:
            if isinstance(returned_id[0], int):
                warehouse_address = address.Address_by_ID(returned_id)
                return warehouse_address

class Warehouse_by_ID(Warehouse):

    def __init__(self, given_id):
        # Ensuring given ID is int
        if isinstance(given_id, int):
            # Ensuring warehouse ID is in warehouses table
            cursor.execute("select from warehouses where id = :warehouse_id", warehouse_id = given_id)
            if cursor.fetchone():
                self._id = given_id
            else:
                print("Given ID not in warehouses table, id: %i" %given_id)
        else:
            print("Given ID not an int, id: %s" %str(given_id))
