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

    def get_address(self):
        address_string = ", ".join(self.get_street(), self.get_apartment_no(), self.get_city(), \
                                   (" ".join(self.get_state(), self.get_zip())))
        return address_string

    def get_street(self):
        cursor.execute("select addresses.street \
                        from addresses join warehouses on addresses.id = warehouses.address_id \
                        where warehouses.id = :warehouse_id", warehouse_id = self.get_id())
        return cursor.fetchone()[0]

    def get_apartment_no(self)

    # Modification Methods

    def modify_name(self, new_name):
        if new_name:
            cursor.execute("update products set name = :name_string where id = :product_id", name_string = new_name, \
                product_id = self.get_id())
        db.commit()

    def modify_type(self, type_string):
        # Verify it's a valid type (in the table) - selection should return nothing if type invalid
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()[0]
        if type(type_id).__name__ == 'int':
            cursor.execute("update products set product_type_id = :input_id where id = :product_id", \
                input_id = type_id, product_id = self.get_id())
            db.commit()
            self.modify_nutrition_facts(None)
            self.modify_alcohol_content(None)
        # else do nothing -- possibly eventually return error here

    def modify_description(self, input_description):
        if input_description:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = input_description, product_id = self._id)
            db.commit()
        else:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = DEFAULT_DESCRIPTION, product_id = self._id)
            db.commit()

    def modify_nutrition_facts(self, input_nutrition_facts):
        if (self.get_type() == "non-food"):
            cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                new_nutrition_facts = DEFAULT_INEDIBLE_NUTRITION_FACTS, product_id = self._id)
            db.commit()
        else:
            if input_nutrition_facts:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = input_nutrition_facts, product_id = self._id)
                db.commit()
            else:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = DEFAULT_NUTRITION_FACTS, product_id = self._id)
                db.commit()


    def modify_alcohol_content(self, alcohol_content):
        if (self.get_type() == "alcoholic beverage"):
            if alcohol_content:
                cursor.execute("update products set alcohol_content = :new_alcohol_content where id = :product_id", \
                    new_alcohol_content = alcohol_content, product_id = self._id)
                db.commit()
            else:
                cursor.execute("update products set alcohol_content = :new_alcohol_content where id = :product_id", \
                    new_alcohol_content = DEFAULT_ALCOHOL_CONTENT, product_id = self._id)
                db.commit()
        else:
            cursor.execute("update products set alcohol_content = :new_alcohol_content where id = :product_id", \
                new_alcohol_content = DEFAULT_NON_ALCOHOLIC_CONTENT, product_id = self._id)
            db.commit()


