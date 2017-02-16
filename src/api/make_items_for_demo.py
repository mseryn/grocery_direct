#!/usr/bin/env python2

#***
#*  GroceryDirect - Manufacturing Items for Demo
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#***

import address
import order
import person
import product
import warehouse

import grocerydirect_api as api

# Making two customers and one staff user

api.make_new_person("mcornelius", "password", "Melanie", "Cornelius", "customer", middle_initial = "E")
api.make_new_person("joe", "password", "Joe", "Doe", "customer")
api.make_new_person("benny@gd.com", "password", "Benny", "Denny", "staff", salary = 45000, job_title = "stock")

# Making 10 products

prod_names  = ["apple", "orange", "bread", "candy bar", "steak", "milk", "eggs", "rum", "toilet paper", "paper plates"]
prod_desc   = ["red deliscious", "navel, large", "wheat", "chocolate with hazelnuts", "20 oz t-bone", \
              "2%", "1 dozen", "fancy", "pack of 6 rolls", "pack of 40"]
prod_prices = [1.5, .75, 1, 1.25, 13, 2.25, 1.75, 15.5, 4.5, 3]
prod_sizes  = [1, 1, 1, 1, 2, 2, 1, 1, 3, 2]
prod_types  = ["food", "food", "food", "food", "food", "non-alcoholic beverage", "food", "alcoholic beverage", "non-food", "non-food"]
prod_nut    = ["70 calories", "40 calories", "70 calories per slice", "250 calories", "cook until well done", \
               "120 calories per cup, 50% daily recommended calcium intake", "cook until well done", None, None, None]
alc_content = "35%"

for i in range(0, 10):

    if prod_types[i] == "alcoholic beverage":
        api.make_new_product(prod_names[i], prod_types[i], description = prod_desc[i], nutrition_facts = prod_nut[i], \
            alcohol_content = alc_content, size = prod_sizes[i], state_code = "ALL", state_price = prod_prices[i])
    else:
        api.make_new_product(prod_names[i], prod_types[i], description = prod_desc[i], nutrition_facts = prod_nut[i], \
            alcohol_content = alc_content, size = prod_sizes[i], state_code = "ALL", state_price = prod_prices[i])

# Making 2 warehouses

owner = api.login("benny@gd.com", "password")
ware_addr_1 =  api.make_new_address("556 Warehouse St.", "Tampa", "FL", 54387, "warehouse", owner)
ware_addr_2 =  api.make_new_address("798 Another Rd.", "Chicago", "IL", 60616, "warehouse", owner)
api.make_new_warehouse(15000, ware_addr_1)
api.make_new_warehouse(25000, ware_addr_2)

