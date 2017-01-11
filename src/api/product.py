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

    def __init__(self, name, type_string, description = None, nutrition_facts = None, alcohol_content = None):
        db = cx_Oracle.connect('system', 'oracle')
        cursor = db.cursor()

        # Getting type_id from type_string, ensuring it's a valid type string (returns int ID)
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()[0]


        if type_id:
            if type(type_id).__name__ == 'int':
                # Adding new product to database (ONLY name and type_id) and retrieving generated product ID
                print(type_id)
                returned_id = cursor.var(cx_Oracle.NUMBER)
                cursor.execute("insert into products (name, product_type_id) values (:product_name, :ptype_id) \
                    returning id into :new_product_id", product_name = name, ptype_id = type_id, new_product_id = returned_id)
                db.commit()
                self._id = returned_id

                # Now adding description, nutrition facts, and alcohol content (automatically generating defaults)
                self.modify_description(description)
                self.modify_nutrition_facts(nutrition_facts)
                self.modify_alcohol_content(alcohol_content)

        # TODO: requires functional person to test, do later
        #_price = self.get_price()

    # Get Methods

    def get_id(self):
        return self._id

    def get_name(self):
        cursor.execute("select name from products where id=:product_id", product_id = self._id)
        name =  cursor.fetchone()[0]
        return name

    def get_type(self):
        cursor.execute("select product_types.product_type \
                        from products join product_types on products.product_type_id = product_types.id \
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

    def modify_name(self, new_name):
        if new_name:
            cursor.execute("update products set name = :name_string where id = :product_id", name_string = new_name, \
                product_id = self.get_id())
        db.commit()

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


