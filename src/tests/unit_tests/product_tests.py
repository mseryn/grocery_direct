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

import product

#**************************************************************************************************
#**  PRODUCT: TESTING NAME 
#**************************************************************************************************

def test_product_get_id():
    # successfully retrieve product ID using get_id()
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    print test_product.get_id()
    assert(test_product.get_id() == test_product._id), "get_id() did not return correct product ID"
    

#**************************************************************************************************
#**  PRODUCT: TESTING NAME 
#**************************************************************************************************

def test_product_get_name():
    # successfully retrieve name using get_name()
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    assert(test_product.get_name() == "test product"), "get_name did not return correct product name"

def test_product_modify_name():
    # successfully modify product name
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    test_product.modify_name("new name")
    assert(test_product.get_name() == "new name"), "modify_name did not modify product name"

def test_product_modify_name_null():
    # unsuccessfully modify product name with null value
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    test_product.modify_name(None)
    assert(test_product.get_name() == "test product"), \
        "modify_name did not behave correctly when give None product name"


#**************************************************************************************************
#**  PRODUCT: TESTING TYPES
#**************************************************************************************************

def test_product_get_non_food_type():
    type_string = "non-food"
    test_product = product.Product.new_product("test product", type_string, description = "unit test product")
    assert(test_product.get_type() == type_string), \
        "get_type() did not correctly return non-food type"

def test_product_get_food_type():
    type_string = "food"
    test_product = product.Product.new_product("test product", type_string, description = "unit test product")
    assert(test_product.get_type() == type_string), \
        "get_type() did not correctly return food type"

def test_product_get_non_alcoholic_beverage_type():
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string, description = "unit test product")
    assert(test_product.get_type() == type_string), \
        "get_type() did not correctly return non-alcoholic beverage type"

def test_product_get_alcoholic_beverage_type():
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string, description = "unit test product")
    assert(test_product.get_type() == type_string), \
        "get_type() did not correctly return alcoholic beverage type"

def product_invalid_type():
    # Assert throws error -- TODO
    pass
    type_string = "invalid"
    test_product = product.Product.new_product("test product", type_string, description = "unit test product")

def test_product_modify_type_to_non_food():
    type_string = "non-food"
    test_product = product.Product.new_product("test product", "food", description = "unit test product")
    test_product.modify_type(type_string)
    print test_product.get_type()
    assert(test_product.get_type() == type_string), \
        "modify_type() did not correctly modify and return non-food type"
        
def test_product_modify_type_to_food():
    type_string = "food"
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    test_product.modify_type(type_string)
    assert(test_product.get_type() == type_string), \
        "modify_type() did not correctly modify and return food type"

def test_product_modify_type_to_non_alcoholic_beverage():
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    test_product.modify_type(type_string)
    assert(test_product.get_type() == type_string), \
        "modify_type() did not correctly modify and return non-alcoholic beverage type"

def test_product_modify_type_to_alcoholic_beverage():
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", "non-food", description = "unit test product")
    test_product.modify_type(type_string)
    assert(test_product.get_type() == type_string), \
        "modify_type() did not correctly modify and return alcoholic beverage type"

def product_modify_type_to_invalid():
    # TODO
    pass

#**************************************************************************************************
#**  PRODUCT: TESTING EXISTANCE OF DESCRIPTION FIELDS GIVEN TYPES
#**************************************************************************************************

# Description (all product types):

def test_product_get_default_description_non_food():
    # successfully retrieve default description of a non-food product
    test_product = product.Product.new_product("test product", "non-food")
    assert(test_product.get_description() == "default product description"), \
        "default product description not correctly returned for non-food product"

def test_product_get_default_description_food():
    # successfully retrieve default description of a food product
    test_product = product.Product.new_product("test product", "food")
    assert(test_product.get_description() == "default product description"), \
        "default product description not correctly returned for food product"

def test_product_get_default_description_beverage():
    # successfully retrieve default description of a non-alcoholic beverage
    test_product = product.Product.new_product("test product", "non-alcoholic beverage")
    assert(test_product.get_description() == "default product description"), \
        "default product description not correctly returned for beverage product"

def test_product_get_default_description_alcoholic_beverage():
    # successfully retrieve default description of an alcoholic beverage
    test_product = product.Product.new_product("test product", "alcoholic beverage")
    assert(test_product.get_description() == "default product description"), \
        "default product description not correctly returned for alcoholic beverage product"

def test_product_get_description_non_food():
    # successfully retrieve description of a non-food product
    test_product = product.Product.new_product("test product", "non-food", \
        description = "unit test non-food product description")
    assert(test_product.get_description() == "unit test non-food product description"), \
        "product description not correctly returned for non-food product"

def test_product_get_description_food():
    # successfully retrieve description of a food product
    test_product = product.Product.new_product("test product", "food", \
        description = "unit test food product description") 
    assert(test_product.get_description() == "unit test food product description"), \
        "product description not correctly returned for food product"

def test_product_get_description_beverage():
    # successfully retrieve description of a non-alcoholic beverage
    test_product = product.Product.new_product("test product", "non-alcoholic beverage", \
        description = "unit test non-alcoholic beverage product description")
    assert(test_product.get_description() == "unit test non-alcoholic beverage product description"), \
        "product description not correctly returned for non-alcoholic beverage product"

def test_product_get_description_alcoholic_beverage():
    # successfully retrieve description of an alcoholic beverage
    test_product = product.Product.new_product("test product", "alcoholic beverage", \
        description = "unit test alcoholic beverage product description")
    assert(test_product.get_description() == "unit test alcoholic beverage product description"), \
        "product description not correctly returned for alcoholic beverage product"

def test_product_modify_description():
    # successfully modify and retrieve modified description of product
    test_product = product.Product.new_product("test product", "non-food")
    test_product.modify_description("modified product description")
    assert(test_product.get_description() == "modified product description"), \
        "product description not correctly modified"

# Nutrition Facts (all consumable products):

def test_product_get_default_nutrition_facts_non_food():
    # successfully retrieve default nutrition facts of a non-food product
    test_product = product.Product.new_product("test product", "non-food")
    assert(test_product.get_nutrition_facts() == \
        "product is not consumable and does not have nutrition facts"), \
        "default nutrition facts not correctly returned for non-food product"

def test_product_get_default_nutrition_facts_food():
    # successfully retrieve default nutrition facts of a food product
    test_product = product.Product.new_product("test product", "food")
    assert(test_product.get_nutrition_facts() == \
        "nutrition facts not yet set"), \
        "default nutrition facts not correctly returned for food product"

def test_product_get_default_nutrition_facts_beverage():
    # successfully retrieve default nutrition facts of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string)
    assert(test_product.get_nutrition_facts() == "nutrition facts not yet set"), \
        "default nutrition facts not correctly returned for %s product" %type_string

def test_product_get_default_nutrition_facts_alcoholic_beverage():
    # successfully retrieve default nutrition facts of an alcoholic beverage
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string)
    assert(test_product.get_nutrition_facts() == "nutrition facts not yet set"), \
        "default nutrition facts not correctly returned for %s product" %type_string

def test_product_get_nutrition_facts_non_food():
    # successfully retrieve nutrition facts of a non-food product
    type_string = "non-food"
    test_product = product.Product.new_product("test product", type_string, \
        nutrition_facts = "test nutrition facts")
    assert(test_product.get_nutrition_facts() == \
        "product is not consumable and does not have nutrition facts"), \
        "nutrition facts not correctly returned for %s product" %type_string

def test_product_get_nutrition_facts_food():
    # successfully retrieve nutrition facts of a food test_product
    type_string = "food"
    test_product = product.Product.new_product("test product", type_string, \
        nutrition_facts = "test nutrition facts")
    assert(test_product.get_nutrition_facts() == "test nutrition facts"), \
        "nutrition facts not correctly returned for %s product" %type_string

def test_product_get_nutrition_facts_beverage():
    # successfully retrieve nutrition facts of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string, \
        nutrition_facts = "test nutrition facts")
    assert(test_product.get_nutrition_facts() == "test nutrition facts"),\
        "nutrition facts not correctly returned for %s product" %type_string

def test_product_get_nutrition_facts_alcoholic_beverage():
    # successfully retrieve nutrition facts of an alcoholic beverage
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string, \
        nutrition_facts = "test nutrition facts")
    assert(test_product.get_nutrition_facts() == "test nutrition facts"), \
        "nutrition facts not correctly returned for %s product" %type_string

def test_product_modify_nutrition_facts():
    # successfully modify and retrieve modified nutrition facts of product
    type_string = "food"
    test_product = product.Product.new_product("test product", type_string)
    test_product.modify_nutrition_facts("modified nutrition facts")
    assert(test_product.get_nutrition_facts() == "modified nutrition facts"), \
        "nutrition facts not correctly modified"

def test_product_modify_nutrition_facts_non_food():
    # successfully return from attempt to modify nutrition facts of non-food product
    # nutrition facts should be default option
    type_string = "non-food"
    test_product = product.Product.new_product("test product", type_string, \
        nutrition_facts = "test nutrition facts")
    assert(test_product.get_nutrition_facts() == "product is not consumable and does not have nutrition facts"), \
        "nutrition facts not correctly returned for %s product" %type_string

# Alcohol Content (all alcoholic beverages):

product_is_non_alcoholic = "product is non-alcoholic and does not have alcohol content"

def test_product_get_default_alcohol_content_non_food():
    # successfully retrieve default alcohol content of a non-food product
    type_string = "non-food"
    test_product = product.Product.new_product("test product", type_string)
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "default alcohol content not correctly returned for %s product" %type_string

def test_product_get_default_alcohol_content_food():
    # successfully retrieve default alcohol content of a food product
    type_string = "food"
    test_product = product.Product.new_product("test product", type_string)
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "default alcohol content not correctly returned for %s product" %type_string

def test_product_get_default_alcohol_content_beverage():
    # successfully retrieve default alcohol content of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string)
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "default alcohol content not correctly returned for %s product" %type_string

def test_product_get_default_alcohol_content_alcoholic_beverage():
    # successfully retrieve default alcohol content of an alcoholic beverage
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string)
    assert(test_product.get_alcohol_content() == "alcohol content not yet set"), \
        "default alcohol content not correctly returned for %s product" %type_string

def test_product_get_alcohol_content_non_food():
    # successfully retrieve alcohol content of a non-food product
    type_string = "non-food"
    test_product = product.Product.new_product("test product", type_string, alcohol_content = "test")
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "alcohol content not correctly returned for %s product" %type_string

def test_product_get_alcohol_content_food():
    # successfully retrieve alcohol content of a food product
    type_string = "food"
    test_product = product.Product.new_product("test product", type_string, alcohol_content = "test")
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "alcohol content not correctly returned for %s product" %type_string

def test_product_get_alcohol_content_beverage():
    # successfully retrieve alcohol content of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string, alcohol_content = "test")
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "alcohol content not correctly returned for %s product" %type_string

def test_product_get_alcohol_content_alcoholic_beverage():
    # successfully retrieve alcohol content of an alcoholic beverage
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string, \
        alcohol_content = "test alcohol content")
    assert(test_product.get_alcohol_content() == "test alcohol content"), \
        "alcohol content not correctly returned for %s product" %type_string

def test_product_modify_alcohol_content_non_food():
    # successfully return from attempt to modify alcohol content of non-food product
    # alcohol content should be default option
    type_string = "non-food"
    test_product = product.Product.new_product("test product", type_string)
    test_product.modify_alcohol_content("test")
    assert(test_product._alcohol_content == product_is_non_alcoholic), \
        "modify alcohol content did not correctly set for %s product" %type_string

def test_product_modify_alcohol_content_non_food():
    # successfully return from attempt to modify alcohol content of food product
    # alcohol content should be default option
    type_string = "food"
    test_product = product.Product.new_product("test product", type_string)
    test_product.modify_alcohol_content("test")
    assert(test_product._alcohol_content == product_is_non_alcoholic), \
        "modify alcohol content did not correctly set for %s product" %type_string

def test_product_modify_alcohol_content_non_food():
    # successfully return from attempt to modify alcohol content of non-alcoholic beverage product
    # alcohol content should be default option
    type_string = "non-alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string)
    test_product.modify_alcohol_content("test")
    assert(test_product.get_alcohol_content() == product_is_non_alcoholic), \
        "modify alcohol content did not correctly set for %s product" %type_string

def test_product_modify_alcohol_content():
    # successfully modify and retrieve modified alcohol content of alcoholic beverage
    type_string = "alcoholic beverage"
    test_product = product.Product.new_product("test product", type_string)
    test_product.modify_alcohol_content("test alcohol content")
    assert(test_product.get_alcohol_content() == "test alcohol content"), \
        "modify alcohol content did not correctly set for %s product" %type_string


#**************************************************************************************************
#**  PRODUCT: PRICE
#**************************************************************************************************

# Sentinal value of -1 used to indicate a product whose price is set in state
def test_product_modify_price_new_state():
    # successfully modify price of product in previously unlisted state 
    test_product = product.Product.new_product("test product", "non-food")
    test_product.modify_price_per_state("MO", 15)
    assert(test_product.get_price_per_state("MO") == 15), \
        "modify_price failed to add new state/price for product"

def test_product_modify_price_overwrite_existing_state():
    # successfully overwrite price of product in previously listed state
    test_product = product.Product.new_product("test product", "non-food")
    test_product.modify_price_per_state("MO", 1)
    test_product.modify_price_per_state("MO", 15)
    assert(test_product.get_price_per_state("MO") == 15), \
        "modify_price failed to overwrite existing state/price for product"

def test_product_get_price():
    # successfully retrieve price of valid state
    test_product = product.Product.new_product("test product", "non-food")
    test_product.modify_price_per_state("MO", 15)
    assert(test_product.get_price_per_state("MO") == 15), \
        "get_price failed to retrieve price for product"

def test_product_get_unlisted_price():
    # unsuccessfully retrieve price for invalid state (not listed for product)
    test_product = product.Product.new_product("test product", "non-food")
    assert(test_product.get_price_per_state("MO") == -1), \
        "get_price failed to retrieve sentinal value for product unlisted in given state"

def test_product_get_price_invalid_state():
    # successfully return from attempt to use invalid state code
    test_product = product.Product.new_product("test product", "non-food")
    test_product.modify_price_per_state("LL", 100)
    assert(test_product.get_price_per_state("LL") == None), \
        "get_price failed to return None for invalid state code for product"

#**************************************************************************************************
#**  PRODUCT: SIZE
#**************************************************************************************************

def test_product_get_size():
    # successfully retrieve initialized product size
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    assert(test_product.get_size() == 3), "get_size() did not correctly return for product"

def test_product_modify_size():
    # successfully modify and retrieve product size
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_product.modify_size(9)
    assert(test_product.get_size() == 9), "modify_size() did not correctly set for product"

def test_product_modify_size_invalid():
    # successfully return from attempt to modify product with invalid size
    test_product = product.Product.new_product("test product", "non-food", size = 3)
    test_product.modify_size("invalid size type")
    assert(test_product.get_size() == 3), \
        "modify_size() failed to succeed when given invalid new product size"

#**************************************************************************************************
#**  PRODUCT: TESTING IMAGE
#**  THIS IS NOT REQUIRED, IMPLEMENT LAST
#**************************************************************************************************

