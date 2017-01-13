#***
#*  GroceryDirect - Address Tests
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*
#*  Addresses:
#*  have:
#*      -- street
#*      -- apt (optional)
#*      -- city
#*      -- state
#*      -- zip code
#*      -- type
#*  get:
#*      -- street
#*      -- apt (if exists)
#*      -- city
#*      -- state
#*      -- zip code
#*      -- full address string?
#*      -- type
#*  modify:
#*      -- street
#*      -- apt
#*      -- city
#*      -- state
#*      -- zip code
#*      -- type
#***

###################################################################################################

import cx_Oracle

# Starting up interaction with database:
db = cx_Oracle.connect('system', 'oracle')
cursor = db.cursor()

class Product():

    def __init__(self, street, city, state_string, zip_code, type_string, apt_no = None):
    
        db = cx_Oracle.connect('system', 'oracle')
        cursor = db.cursor()

        # Getting type_id from type_string
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()[0]

        # Getting state_id from state_string

        # Ensuring both state and type IDs are ints
        if type_id:
            if type(type_id).__name__ == 'int':
                # Adding new product to database (ONLY name and type_id) and retrieving generated product ID
                print(type_id)
                returned_id = cursor.var(cx_Oracle.NUMBER)
                cursor.execute("insert into products (name, product_type_id, product_size) values \
                    (:product_name, :ptype_id, :psize) returning id into :new_product_id", product_name = name, \
                    ptype_id = type_id, new_product_id = returned_id, psize = size)
                db.commit()
                self._id = returned_id

    # Get Methods

    def get_id(self):
        return self._id

    def get_name(self):
        cursor.execute("select name from products where id=:product_id", product_id = self._id)
        name =  cursor.fetchone()[0]
        return name

    def get_type(self):
        # Returns string of product type -- not type_id
        cursor.execute("select product_types.product_type \
                        from products join product_types on products.product_type_id = product_types.id \
                        where products.id = :product_id", product_id = self._id)
        return cursor.fetchone()[0]

    def get_description(self):
        cursor.execute("select description from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()[0]

    def get_nutrition_facts(self):
        cursor.execute("select nutrition_facts from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()[0]

    def get_alcohol_content(self):
        cursor.execute("select alcohol_content from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()[0]

    def get_price_per_state(self, state_code):
        # First must ensure state code in state code table
        cursor.execute("select id from state_codes where state_code = :input_code", input_code = state_code)
        state_id = cursor.fetchone()
        if state_id:
            state_id = state_id[0]
            # Then must look at state-to-product table, see if price listed
            cursor.execute("select state_price from state_code_to_product where product_id = :p_id and state_id = :s_id", \
                p_id = self.get_id(), s_id = state_id)
            price = cursor.fetchone()
            # If yes to both above conditions, return a price (ensuring it's a valid price), otherwise return -1.0 (sentianl)
            if price:
                return price[0]
            else:
                return -1

    def get_size(self):
        cursor.execute("select product_size from products where id = :product_id", product_id = self._id)
        return cursor.fetchone()[0]

    # Modification Methods

    def modify_name(self, new_name):
        if new_name:
            cursor.execute("update products set name = :name_string where id = :product_id", name_string = new_name, \
                product_id = self.get_id())
        db.commit()

    def modify_type(self, type_string):
        # Verify it's a valid type (in the table) - selection should return nothing if type invalid
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()[0]
        if type(type_id).__name__ == 'int':
            cursor.execute("update products set product_type_id = :input_id where id = :product_id", \
                input_id = type_id, product_id = self.get_id())
            db.commit()
            self.modify_nutrition_facts(None)
            self.modify_alcohol_content(None)
        # else do nothing -- possibly eventually return error here

    def modify_description(self, input_description):
        if input_description:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = input_description, product_id = self._id)
            db.commit()
        else:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = DEFAULT_DESCRIPTION, product_id = self._id)
            db.commit()

    def modify_nutrition_facts(self, input_nutrition_facts):
        if (self.get_type() == "non-food"):
            cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                new_nutrition_facts = DEFAULT_INEDIBLE_NUTRITION_FACTS, product_id = self._id)
            db.commit()
        else:
            if input_nutrition_facts:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = input_nutrition_facts, product_id = self._id)
                db.commit()
            else:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = DEFAULT_NUTRITION_FACTS, product_id = self._id)
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

    def modify_price_per_state(self, state_code, new_price):
        # First must ensure state code in state code table
        cursor.execute("select id from state_codes where state_code = :input_code", input_code = state_code)
        state_id = cursor.fetchone()
        if state_id:
            state_id = state_id[0]
            # Ensure price is number and is positive:
            if isinstance(new_price, (int, float, long)) and new_price >= 0:
                # Then must look at state-to-product table, see if price listed
                cursor.execute("select state_price from state_code_to_product where product_id = :p_id and state_id = :s_id", \
                    p_id = self.get_id(), s_id = state_id)
                old_price = cursor.fetchone()
                if old_price:
                    # Existing state price overwrite:
                    cursor.execute("update state_code_to_product set state_price = :input_price where product_id = :p_id and state_id = :s_id", \
                        input_price = new_price, p_id = self.get_id(), s_id = state_id)
                    db.commit()
                else:
                    # New state price, new row:
                    cursor.execute("insert into state_code_to_product (state_id, product_id, state_price) \
                        values (:s_id, :p_id, :price)", s_id = state_id, p_id = self.get_id(), price = new_price)
                    db.commit()

    def modify_size(self, new_size):
        # ensuring it's a number:
        if isinstance(new_size, (int, float, long)):
            cursor.execute("update products set product_size = :psize where id = :product_id", \
                psize = new_size, product_id = self.get_id())
            db.commit()
