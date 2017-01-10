#***
#*  GroceryDirect - Product Tests
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
default_description     = "default product description"
default_nutrition_facts = "nutrition facts not yet set"
default_alcohol_content = "alcohol content not yet set"

default_inedible_nutrition_facts = "product is not consumable and does not have nutrition facts"
default_non_alcoholic_content    = "product is non-alcoholic and does not have alcohol content"

# Store only ID; have get/modify methods interact with DB, store nothing else

class Product():

    def __init__(self, name, type_string, description, nutrition_facts = None, alcohol_content = None):
        db = cx_Oracle.connect('system', 'oracle')
        cursor = db.cursor()
        cursor.execute("insert into products (name, description, ")

        _id = self.get_id()
        _name = name
        _type = self.modify_type(type_string)
        _description = self.modify_description(description)
        _nutrition_facts = self.modify_nutrition_facts(nutrition_facts)
        _alcohol_content = self.modify_alcohol_content(alcohol_content)

        # TODO: requires functional person to test, do later
        #_price = self.get_price()

        # TODO: move these fields to modify_blah methods, more correct

    # Get Methods

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_description(self):
        return self._description

    def get_nutrition_facts(self):
        return self._nutrition_facts

    def get_alcohol_content(self):
        return self._alcohol_content

    # Modification Methods

    def modify_type(self, modify_string):
        pass

    def modify_description(self, description):
        if description:
            self._description = description
        else:
            self._description = default_description

    def modify_nutrition_facts(self, nutrition_facts):
        if (_type != "non-food"):
            if nutrition_facts:
                self._nutrition_facts = nutrition_facts
            else:
                self._nutrition_facts = default_nutrition_facts

        else:
            self._nutrition_facts = default_inedible_nutrition_facts 

    def modify_alcohol_content(self, alcohol_content):
        if (_type == "alcoholic beverage"):
            if alcohol_content:
                self._alcohol_content = alcohol_content
            else:
                self._alcohol_content = default_alcohol_content
        else:
            self._alcohol_content = default_non_alcoholic_content
