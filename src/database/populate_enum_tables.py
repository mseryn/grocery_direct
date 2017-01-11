#***
#*  GroceryDirect - Script to Populate Enum Tables
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#***

import cx_Oracle
import pprint

# Files (symlinks) defining enum table contents
PERSON_TYPES_FILE   = "person_types.txt"
PRODUCT_TYPES_FILE  = "product_types.txt"
ADDRESS_TYPES_FILE  = "address_types.txt"
ORDER_STATUSES_FILE = "order_statuses.txt"
STATE_CODES_FILE    = "state_codes.txt"
CARD_TYPES_FILE     = "card_types.txt"

# Lists for storing values
person_types = []
product_types = []
address_types = []
order_statuses = []
state_codes = []
card_types = []

# Connecting to DB
db = cx_Oracle.connect('system','oracle')
cursor = db.cursor()

# Erasing all enum tables
cursor.execute("delete from person_types")
cursor.execute("delete from product_types")
cursor.execute("delete from address_types")
cursor.execute("delete from order_statuses")
cursor.execute("delete from state_codes")
cursor.execute("delete from card_types")

# People Types
person_types_file = open(PERSON_TYPES_FILE, 'r')
for line in person_types_file:
    cursor.execute("insert into person_types (person_type) values (:type_string)", type_string = line.strip())

# Product Types
product_types_file = open(PRODUCT_TYPES_FILE, 'r')
for line in product_types_file:
    cursor.execute("insert into product_types (product_type) values (:type_string)", type_string = line.strip())

# Address Types
address_types_file = open(ADDRESS_TYPES_FILE, 'r')
for line in address_types_file:
    cursor.execute("insert into address_types (address_type) values (:type_string)", type_string = line.strip())

# Order Statuses
order_status_file = open(ORDER_STATUSES_FILE, 'r')
for line in order_status_file:
    cursor.execute("insert into order_statuses (order_status) values (:status_string)", status_string = line.strip())

# State Codes
state_code_file = open(STATE_CODES_FILE, 'r')
for line in state_code_file:
    cursor.execute("insert into state_codes (state_code) values (:code_string)", code_string = line.strip())

# Card Types
card_types_file = open(CARD_TYPES_FILE, 'r')
for line in card_types_file:
    cursor.execute("insert into card_types (card_type) values (:type_string)", type_string = line.strip())

# committing and closing database connection
db.commit()
db.close()
