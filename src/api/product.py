#***
#*  GroceryDirect - Product Class
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
#*      -- size (cubic feet)
#*      -- price (by state)
#*  - get:
#*      -- name
#*      -- type
#*      -- image
#*      -- description
#*      -- nutrition facts
#*      -- alcohol content
#*      -- size (cubic feet)
#*      -- price (by state)
#*  - modify:
#*      -- name
#*      -- type
#*      -- image
#*      -- description
#*      -- nutrition facts
#*      -- alcohol content
#*      -- size (cubic feet)
#*      -- price (by state)
#***

import database

# String defaults:
DEFAULT_DESCRIPTION     = "default product description"
DEFAULT_NUTRITION_FACTS = "nutrition facts not yet set"
DEFAULT_ALCOHOL_CONTENT = "alcohol content not yet set"

DEFAULT_INEDIBLE_NUTRITION_FACTS = "product is not consumable and does not have nutrition facts"
DEFAULT_NON_ALCOHOLIC_CONTENT    = "product is non-alcoholic and does not have alcohol content"

class Product():

    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)
        # Ensuring given ID is int
        if isinstance(given_id, int):
            # Ensuring warehouse ID is in warehouses table
            cursor.execute("select id from products where id = :product_id", product_id = given_id)
            if cursor.fetchone():
                self._id = given_id

            else:
                print("Given ID not in products table, id: %i" %given_id)
        else:
            print("Given ID not an int, id: %s" %str(given_id))

    @staticmethod
    def new_product(name, type_string, description = None, nutrition_facts = None, alcohol_content = None, size = 1):
        # Adding new product to database, returning reference to new product instance
        db = database.connect()
        cursor = database.get_cursor(db)

        # Getting type_id from type_string, ensuring it's a valid type string (returns int ID)
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()[0]

        if type_id:
            if isinstance(type_id, int):
                # Adding new product to database (ONLY name and type_id) and retrieving generated product ID
                returned_id = cursor.var(database.cx_Oracle.NUMBER)
                cursor.execute("insert into products (name, product_type_id, product_size) values \
                    (:product_name, :ptype_id, :psize) returning id into :new_product_id", product_name = name, \
                    ptype_id = type_id, new_product_id = returned_id, psize = size)
                database.commit(db)

                # Getting product reference
                returned_id = int(returned_id.getvalue())
                new_product = Product(returned_id)

                # Now adding description, nutrition facts, and alcohol content (automatically generating defaults)
                new_product.modify_description(description)
                new_product.modify_nutrition_facts(nutrition_facts)
                new_product.modify_alcohol_content(alcohol_content)

                return new_product


    # Get Methods

    def get_id(self):
        return self._id

    def get_name(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select name from products where id=:product_id", product_id = self._id)
        name =  cursor.fetchone()[0]
        database.close(db)
        return name

    def get_type(self):
        # Returns string of product type -- not type_id
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select product_types.product_type \
                        from products join product_types on products.product_type_id = product_types.id \
                        where products.id = :product_id", product_id = self._id)
        type_string = cursor.fetchone()[0]
        database.close(db)
        return type_string

    def get_description(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select description from products where id = :product_id", product_id = self._id)
        description = cursor.fetchone()[0]
        database.close(db)
        return description

    def get_nutrition_facts(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select nutrition_facts from products where id = :product_id", product_id = self._id)
        nutrition_facts = cursor.fetchone()[0]
        database.close(db)
        return nutrition_facts

    def get_alcohol_content(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select alcohol_content from products where id = :product_id", product_id = self._id)
        alcohol_content = cursor.fetchone()[0]
        database.close(db)
        return alcohol_content

    def get_price_per_state(self, state_code):
        # First must ensure state code in state code table
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select id from state_codes where state_code = :input_code", input_code = state_code)
        state_id = cursor.fetchone()
        if state_id:
            state_id = state_id[0]
            # Then must look at state-to-product table, see if price listed
            cursor.execute("select state_price from state_to_product where product_id = :p_id and state_id = :s_id", \
                p_id = self.get_id(), s_id = state_id)
            price = cursor.fetchone()
            # If yes to both above conditions, return a price (ensuring it's a valid price), otherwise return -1.0 (sentianl)
            if price:
                database.close(db)
                return price[0]
            else:
                database.close(db)
                return -1
        database.close(db)

    def get_size(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select product_size from products where id = :product_id", product_id = self._id)
        size = cursor.fetchone()[0]
        database.close(db)
        return size

    # Modification Methods

    def modify_name(self, new_name):
        db = database.connect()
        cursor = database.get_cursor(db)
        if new_name:
            cursor.execute("update products set name = :name_string where id = :product_id", name_string = new_name, \
                product_id = self.get_id())
        database.commit(db)
        database.close(db)

    def modify_type(self, type_string):
        # Verify it's a valid type (in the table) - selection should return nothing if type invalid
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select id from product_types where product_type = :input_type", input_type = type_string)
        type_id = cursor.fetchone()[0]
        if type(type_id).__name__ == 'int':
            cursor.execute("update products set product_type_id = :input_id where id = :product_id", \
                input_id = type_id, product_id = self.get_id())
            database.commit(db)
            self.modify_nutrition_facts(None)
            self.modify_alcohol_content(None)
        # else do nothing -- possibly eventually return error here
        database.close(db)

    def modify_description(self, input_description):
        db = database.connect()
        cursor = database.get_cursor(db)
        if input_description:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = input_description, product_id = self._id)
            database.commit(db)
        else:
            cursor.execute("update products set description = :new_description where id = :product_id", \
                new_description = DEFAULT_DESCRIPTION, product_id = self._id)
            database.commit(db)

    def modify_nutrition_facts(self, input_nutrition_facts):
        db = database.connect()
        cursor = database.get_cursor(db)
        if (self.get_type() == "non-food"):
            cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                new_nutrition_facts = DEFAULT_INEDIBLE_NUTRITION_FACTS, product_id = self._id)
            database.commit(db)
        else:
            if input_nutrition_facts:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = input_nutrition_facts, product_id = self._id)
                database.commit(db)
            else:
                cursor.execute("update products set nutrition_facts = :new_nutrition_facts where id = :product_id", \
                    new_nutrition_facts = DEFAULT_NUTRITION_FACTS, product_id = self._id)
                database.commit(db)
        database.close(db)


    def modify_alcohol_content(self, alcohol_content):
        db = database.connect()
        cursor = database.get_cursor(db)
        if (self.get_type() == "alcoholic beverage"):
            if alcohol_content:
                cursor.execute("update products set alcohol_content = :new_alcohol_content where id = :product_id", \
                    new_alcohol_content = alcohol_content, product_id = self._id)
                database.commit(db)
            else:
                cursor.execute("update products set alcohol_content = :new_alcohol_content where id = :product_id", \
                    new_alcohol_content = DEFAULT_ALCOHOL_CONTENT, product_id = self._id)
                database.commit(db)
        else:
            cursor.execute("update products set alcohol_content = :new_alcohol_content where id = :product_id", \
                new_alcohol_content = DEFAULT_NON_ALCOHOLIC_CONTENT, product_id = self._id)
            database.commit(db)
        database.close(db)

    def modify_price_per_state(self, state_code, new_price):
        # First must ensure state code in state code table
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select id from state_codes where state_code = :input_code", input_code = state_code)
        state_id = cursor.fetchone()
        if state_id:
            state_id = state_id[0]
            # Ensure price is number and is positive:
            if isinstance(new_price, (int, float, long)) and new_price >= 0:
                # Then must look at state-to-product table, see if price listed
                cursor.execute("select state_price from state_to_product where product_id = :p_id and state_id = :s_id", \
                    p_id = self.get_id(), s_id = state_id)
                old_price = cursor.fetchone()
                if old_price:
                    # Existing state price overwrite:
                    cursor.execute("update state_to_product set state_price = :input_price where product_id = :p_id and state_id = :s_id", \
                        input_price = new_price, p_id = self.get_id(), s_id = state_id)
                    database.commit(db)
                else:
                    # New state price, new row:
                    cursor.execute("insert into state_to_product (state_id, product_id, state_price) \
                        values (:s_id, :p_id, :price)", s_id = state_id, p_id = self.get_id(), price = new_price)
                    database.commit(db)
        database.close(db)

    def modify_size(self, new_size):
        # ensuring it's a number:
        db = database.connect()
        cursor = database.get_cursor(db)
        if isinstance(new_size, (int, float, long)):
            cursor.execute("update products set product_size = :psize where id = :product_id", \
                psize = new_size, product_id = self.get_id())
            database.commit(db)
        database.close(db)
