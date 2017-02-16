#***
#*  GroceryDirect - Database Hook
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#***

# Purpose is to simplify importing database

import cx_Oracle

DATABASE_NAME       = "grocerydirect"
DATABASE_PASSWORD   = "oracle"

db_handle = None

def connect():
    """ Returns DB handle """
    global db_handle
    if not db_handle:
        db_handle = cx_Oracle.connect(DATABASE_NAME, DATABASE_PASSWORD)
    return db_handle

def get_cursor(handle):
    """ Requires DB handle, returns cursor """
    return handle.cursor()

def commit(handle):
    """ Requires DB handle, commits DB """
    handle.commit()
    return True

def disconnect(handle):
    """ Requires DB handle, closes that handle """
    # Leaving the connection open for now
    # handle.close()
