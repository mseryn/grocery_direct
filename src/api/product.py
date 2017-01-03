#***
#*  GroceryDirect - Product Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*  
#*  Product Description:
#*  - has:
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

class Product():

    def __init__(self, name, type_string, description, nutrition_facts = None, alcohol_content = None):
        _name = name
        _type = self.modify_type(type_string)
        _description = self.modify_description(description)
        _nutrition_facts = self.modify_nutrition_facts(nutrition_facts)
        _alcohol_content = self.modify_alcohol_content(alcohol_content)

        # TODO: requires functional person to test, do later
        #_price = self.get_price()

        # Setting nutrition facts and alcohol content as needed
        if (_type != "non-food"):
            _nutrition_facts = self.modify_nutrition_facts(nutrition_facts)

        else:
            _nutrition_facts = "product is not consumable and does not have nutrition facts"

        if (_type == "alcoholic beverage"):
            _alcohol_content = self.modify_alcohol_content(alcohol_content)
        else:
            _alcohol_content = "product is non-alcoholic and does not have alcohol content"

        # TODO: move these fields to modify_blah methods, more correct

    # Get Methods

    def get_name(self):
        return _name

    def get_type(self):
        return _type

    def get_description(self):
        return _description

    # Modification Methods

    def modify_type(self, modify_string):
        pass

    def modify_description(self, description):
        self._description = description

    def modify_nutrition_facts(self, nutrition_facts):
        pass

    def modify_alcohol_content(self, alcohol_content):
        pass
