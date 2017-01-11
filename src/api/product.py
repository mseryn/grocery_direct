#***
#*  GroceryDirect - Product API
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*  
#*  Product Description:
#*  - has:
#*      -- id
#*      -- name
#*      -- type
#*      -- image -- TODO, optional, implement LAST
#*      -- description      (all types)
#*      -- nutrition facts  (food and all beverages)
#*      -- alcohol content  (alcoholic beverages only)
#*  - get:
#*      -- name
#*      -- type
#*      -- image
#*      -- description
#*      -- nutrition facts
#*      -- alcohol content
#*  - modify:
#*      -- name
#*      -- type
#*      -- image
#*      -- description
#*      -- nutrition facts
#*      -- alcohol content
#***

#* TODO: Questions:
#*          -- going to need a get_product_by_id() method outside this class?

import cx_Oracle

# String defaults:
DEFAULT_DESCRIPTION     = "default product description"
DEFAULT_NUTRITION_FACTS = "nutrition facts not yet set"
DEFAULT_ALCOHOL_CONTENT = "alcohol content not yet set"

DEFAULT_INEDIBLE_NUTRITION_FACTS = "product is not consumable and does not have nutrition facts"
DEFAULT_NON_ALCOHOLIC_CONTENT    = "product is non-alcoholic and does not have alcohol content"

# Starting up interaction with database:
db = cx_Oracle.connect('system', 'oracle')
cursor = db.cursor()

class Product():

    def __init__(self, name, type_string, description, nutrition_facts = None, alcohol_content = None):
        db = cx_Oracle.connect('system', 'oracle')
        cursor = db.cursor()
        cursor.execute("insert into products (name, description, ")

        _id = self.get_id()

        # TODO: requires functional person to test, do later
        #_price = self.get_price()

        # TODO: move these fields to modify_blah methods, more correct

    # Get Methods

    def get_id(self):
        return self._id

    def get_name(self):
        cursor.execute("select name from products where id=:product_id", product_id = self._id)
        return cursor.fetchone()

    def get_type(self):
        cursor.execute("select product_types.product_type 
                        from products join product_types on products.product_type_id = product_types.id
                        where products.id = :product_id", product_id = self._id)
        return cursor.fetchone()

    def get_description(self):
        cursor.execute("select description from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()

    def get_nutrition_facts(self):
        cursor.execute("select nutrition_facts from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()

    def get_alcohol_content(self):
        cursor.execute("select alcohol_content from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()

    # Modification Methods

    def modify_type(self, type_string):
        # Verify it's a valid type (in the table) - selection should return nothing if type invalid
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()
        if type(type_id) == 'int':
            cursor.execute("update products set product_type_id = :input_id", input_id = type_id)
            db.commit()
        # else do nothing -- possibly eventually return error here

    def modify_description(self, description):
        if description:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = description, product_id = self._id)
            db.commit()
        else:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = DEFAULT_DESCRIPTION, product_id = self._id)
            db.commit()

    def modify_nutrition_facts(self, nutrition_facts):
        if (self.get_type() != "non-food"):
            if nutrition_facts:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = nutrition_facts, product_id = self._id)
                db.commit()
            else:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = DEFAULT_NUTRITION_FACTS, product_id = self._id)
                db.commit()

        else:
            cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                new_description = DEFAULT_INEDIBLE_NUTRITION_FACTS, product_id = self._id)
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


