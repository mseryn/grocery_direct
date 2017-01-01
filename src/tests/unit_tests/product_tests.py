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
    assert(product.get_name()

def product_modify_name():
    # successfully modify product name

def product_modify_name_null():
    # unsuccessfully modify product name with null value

#**************************************************************************************************
#**  PRODUCT: TESTING TYPES
#**************************************************************************************************

#**************************************************************************************************
#**  PRODUCT: TESTING EXISTANCE OF DESCRIPTION FIELDS GIVEN TYPES
#**************************************************************************************************

#**************************************************************************************************
#**  PRODUCT: TESTING IMAGE
#**************************************************************************************************

