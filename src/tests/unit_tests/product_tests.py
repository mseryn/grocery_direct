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

#**************************************************************************************************
#**  PRODUCT: TESTING NAME 
#**************************************************************************************************

def product_get_name():
    # successfully retrieve name using get_name()
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    assert(product.get_name() == "test product"), "get_name did not return correct product name"

def product_modify_name():
    # successfully modify product name
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    product.modify_name("new name")
    assert(product._name == "new name"), "modify_name did not modify product name"

def product_modify_name_null():
    # unsuccessfully modify product name with null value
    product = product.Product("test product", "non-food", 1.00, description = "unit test product")
    product.modify_name(None)
    assert(product._name == "test product"), 
        "modify_name did not behave correctly when give None product name"


#**************************************************************************************************
#**  PRODUCT: TESTING TYPES
#**************************************************************************************************

#**************************************************************************************************
#**  PRODUCT: TESTING EXISTANCE OF DESCRIPTION FIELDS GIVEN TYPES
#**************************************************************************************************

# Description (all product types):

def product_get_default_description_non_food():
    # successfully retrieve default description of a non-food product
    product = product.Product("test product", "non-food", 1.00)
    assert(product.get_description() == "default product description"), 
        "default product description not correctly returned for non-food product"

def product_get_default_description_food():
    # successfully retrieve default description of a food product
    product = product.Product("test product", "food", 1.00)
    assert(product.get_description() == "default product description"), 
        "default product description not correctly returned for food product"

def product_get_default_description_beverage():
    # successfully retrieve default description of a non-alcoholic beverage
    product = product.Product("test product", "non-alcoholic beverage", 1.00)
    assert(product.get_description() == "default product description"), 
        "default product description not correctly returned for beverage product"

def product_get_default_description_alcoholic_beverage():
    # successfully retrieve default description of an alcoholic beverage
    product = product.Product("test product", "alcoholic beverage", 1.00)
    assert(product.get_description() == "default product description"), 
        "default product description not correctly returned for alcoholic beverage product"

def product_get_description_non_food():
    # successfully retrieve description of a non-food product
    product = product.Product("test product", "non-food", 1.00, 
        description = "unit test non-food product description")
    assert(product.get_description() == "unit test non-food product description"), 
        "product description not correctly returned for non-food product"

def product_get_description_food():
    # successfully retrieve description of a food product
    product = product.Product("test product", "food", 1.00,
        description = "unit test food product description")
    assert(product.get_description() == "unit test food product description"), 
        "product description not correctly returned for food product"

def product_get_description_beverage():
    # successfully retrieve description of a non-alcoholic beverage
    product = product.Product("test product", "non-alcoholic beverage", 1.00,
        description = "unit test non-alcoholic beverage product description")
    assert(product.get_description() == "unit test non-alcoholic beverage product description"),
        "product description not correctly returned for non-alcoholic beverage product"

def product_get_description_alcoholic_beverage():
    # successfully retrieve description of an alcoholic beverage
    product = product.Product("test product", "alcoholic beverage", 1.00,
        description = "unit test non-alcoholic beverage product description")
    assert(product.get_description() == "unit test non-alcoholic beverage product description"), 
        "product description not correctly returned for alcoholic beverage product"

def product_modify_description():
    # successfully modify and retrieve modified description of product
    product = product.Product("test product", "non-food", 1.00)
    product.modify_description("modified product description")
    assert(product._description == "modified product description"), 
        "product description not correctly modified"

# Nutrition Facts (all consumable products):

def product_get_default_nutrition_facts_non_food():
    # successfully retrieve default nutrition facts of a non-food product
    product = product.Product("test product", "non-food", 1.00)
    assert(product.get_nutrition_facts() == 
        "product is not consumable and does not have nutrition facts"), 
        "default nutrition facts not correctly returned for non-food product"

def product_get_default_nutrition_facts_food():
    # successfully retrieve default nutrition facts of a food product
    product = product.Product("test product", "food", 1.00)
    assert(product.get_nutrition_facts() == 
        "nutrition facts not yet set"), 
        "default nutrition facts not correctly returned for food product"

def product_get_default_nutrition_facts_beverage():
    # successfully retrieve default nutrition facts of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    product = product.Product("test product", type_string, 1.00)
    assert(product.get_nutrition_facts() == "nutrition facts not yet set"),
        "default nutrition facts not correctly returned for %s product" %type_string

def product_get_default_nutrition_facts_alcoholic_beverage():
    # successfully retrieve default nutrition facts of an alcoholic beverage
    type_string = "alcoholic beverage"
    product = product.Product("test product", type_string, 1.00)
    assert(product.get_nutrition_facts() == "nutrition facts not yet set"),
        "default nutrition facts not correctly returned for %s product" %type_string

def product_get_nutrition_facts_non_food():
    # successfully retrieve nutrition facts of a non-food product
    type_string = "non-food"
    product = product.Product("test product", type_string, 1.00, \
        nutrition_facts = "test nutrition facts")
    assert(product.get_nutrition_facts() == \
        "product is not consumable and does not have nutrition facts"), \
        "nutrition facts not correctly returned for %s product" %type_string

def product_get_nutrition_facts_food():
    # successfully retrieve nutrition facts of a food product
    type_string = "food"
    product = product.Product("test product", type_string, 1.00, 
        nutrition_facts = "test nutrition facts")
    assert(product.get_nutrition_facts() == "test nutrition facts"),
        "nutrition facts not correctly returned for %s product" %type_string

def product_get_nutrition_facts_beverage():
    # successfully retrieve nutrition facts of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    product = product.Product("test product", type_string, 1.00, 
        nutrition_facts = "test nutrition facts")
    assert(product.get_nutrition_facts() == "test nutrition facts"),
        "nutrition facts not correctly returned for %s product" %type_string

def product_get_nutrition_facts_alcoholic_beverage():
    # successfully retrieve nutrition facts of an alcoholic beverage
    type_string = "alcoholic beverage"
    product = product.Product("test product", type_string, 1.00, 
        nutrition_facts = "test nutrition facts")
    assert(product.get_nutrition_facts() == "test nutrition facts"),
        "nutrition facts not correctly returned for %s product" %type_string

def product_modify_nutrition_facts():
    # successfully modify and retrieve modified nutrition facts of product
    type_string = "food"
    product = product.Product("test product", type_string, 1.00)
    product.modify_nutrition_facts("modified nutrition facts")
    assert(product.get_nutrition_facts() == "modified nutrition facts"), \
        "nutrition facts not correctly modified"

def product_modify_nutrition_facts_non_food():
    # successfully return from attempt to modify nutrition facts of non-food product
    # nutrition facts should be default option
    type_string = "non-food"
    product = product.Product("test product", type_string, 1.00, 
        nutrition_facts = "test nutrition facts")
    assert(product.get_nutrition_facts() == "test nutrition facts"),
        "nutrition facts not correctly returned for %s product" %type_string

# Alcohol Content (all alcoholic beverages):

product_is_non_alcoholic = "product is non-alcoholic and does not have alcohol content"

def product_get_default_alcohol_content_non_food():
    # successfully retrieve default alcohol content of a non-food product
    type_string = "non-food"
    product = product.Product("test product", type_string, 1.00)
    assert(product.get_alcohol_content() == product_is_non_alcoholic),
        "default alcohol content not correctly returned for %s product" %type_string

def product_get_default_alcohol_content_food():
    # successfully retrieve default alcohol content of a food product
    type_string = "food"
    product = product.Product("test product", type_string, 1.00)
    assert(product.get_alcohol_content() == product_is_non_alcoholic),
        "default alcohol content not correctly returned for %s product" %type_string

def product_get_default_alcohol_content_beverage():
    # successfully retrieve default alcohol content of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    product = product.Product("test product", type_string, 1.00)
    assert(product.get_alcohol_content() == product_is_non_alcoholic),
        "default alcohol content not correctly returned for %s product" %type_string

def product_get_default_alcohol_content_alcoholic_beverage():
    # successfully retrieve default alcohol content of an alcoholic beverage
    type_string = "alcoholic beverage"
    product = product.Product("test product", type_string, 1.00)
    assert(product.get_alcohol_content() == "alcohol content not yet set"),
        "default alcohol content not correctly returned for %s product" %type_string

def product_get_alcohol_content_non_food():
    # successfully retrieve alcohol content of a non-food product
    type_string = "non-food"
    product = product.Product("test product", type_string, 1.00, alcohol_content = "test")
    assert(product.get_alcohol_content() == product_is_non_alcoholic),
        "alcohol content not correctly returned for %s product" %type_string

def product_get_alcohol_content_food():
    # successfully retrieve alcohol content of a food product
    type_string = "food"
    product = product.Product("test product", type_string, 1.00, alcohol_content = "test")
    assert(product.get_alcohol_content() == product_is_non_alcoholic),
        "alcohol content not correctly returned for %s product" %type_string

def product_get_alcohol_content_beverage():
    # successfully retrieve alcohol content of a non-alcoholic beverage
    type_string = "non-alcoholic beverage"
    product = product.Product("test product", type_string, 1.00, alcohol_content = "test")
    assert(product.get_alcohol_content() == product_is_non_alcoholic),
        "alcohol content not correctly returned for %s product" %type_string

def product_get_alcohol_content_alcoholic_beverage():
    # successfully retrieve alcohol content of an alcoholic beverage
    type_string = "alcoholic beverage"
    product = product.Product("test product", type_string, 1.00, \
        alcohol_content = "test alcohol content")
    assert(product.get_alcohol_content() == "test alcohol content"),
        "alcohol content not correctly returned for %s product" %type_string

def product_modify_alcohol_content_non_food():
    # successfully return from attempt to modify alcohol content of non-food product
    # alcohol content should be default option
    type_string = "non-food"
    product = product.Product("test product", type_string, 1.00)
    product.set_alcohol_content = "test"
    assert(product._alcohol_content == product_is_non_alcoholic),
        "modify alcohol content did not correctly set for %s product" %type_string

def product_modify_alcohol_content_non_food():
    # successfully return from attempt to modify alcohol content of food product
    # alcohol content should be default option
    type_string = "food"
    product = product.Product("test product", type_string, 1.00)
    product.set_alcohol_content = "test"
    assert(product._alcohol_content == product_is_non_alcoholic),
        "modify alcohol content did not correctly set for %s product" %type_string

def product_modify_alcohol_content_non_food():
    # successfully return from attempt to modify alcohol content of non-alcoholic beverage product
    # alcohol content should be default option
    type_string = "non-alcoholic beverage"
    product = product.Product("test product", type_string, 1.00)
    product.set_alcohol_content = "test"
    assert(product._alcohol_content == product_is_non_alcoholic),
        "modify alcohol content did not correctly set for %s product" %type_string

def product_modify_alcohol_content():
    # successfully modify and retrieve modified alcohol content of alcoholic beverage
    type_string = "alcoholic beverage"
    product = product.Product("test product", type_string, 1.00)
    product.set_alcohol_content = "test alcohol content"
    assert(product._alcohol_content == "test alcohol content"),
        "modify alcohol content did not correctly set for %s product" %type_string


#**************************************************************************************************
#**  PRODUCT: PRICE
#**************************************************************************************************

# Product price stored relative to state/warehouse -- not directly aspect of product
# Sentinal value of -1 used to indicate a product whose price is set in no state (warehouse)
# TODO - REQUIRES WORKING PERSON -- STAFF -- TO SET, DO AFTER PERSON MORE COMPLETE

#**************************************************************************************************
#**  PRODUCT: TESTING IMAGE
#**  THIS IS NOT REQUIRED, IMPLEMENT LAST
#**************************************************************************************************

