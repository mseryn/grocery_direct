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
        database.disconnect(db)
        return name

    def get_type(self):
        # Returns string of product type -- not type_id
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select product_types.product_type \
                        from products join product_types on products.product_type_id = product_types.id \
                        where products.id = :product_id", product_id = self._id)
        type_string = cursor.fetchone()[0]
        database.disconnect(db)
        return type_string

    def get_description(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select description from products where id = :product_id", product_id = self._id)
        description = cursor.fetchone()[0]
        database.disconnect(db)
        return description

    def get_nutrition_facts(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select nutrition_facts from products where id = :product_id", product_id = self._id)
        nutrition_facts = cursor.fetchone()[0]
        database.disconnect(db)
        return nutrition_facts

    def get_alcohol_content(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select alcohol_content from products where id = :product_id", product_id = self._id)
        alcohol_content = cursor.fetchone()[0]
        database.disconnect(db)
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
                database.disconnect(db)
                return price[0]
            else:
                database.disconnect(db)
                return -1
        database.disconnect(db)
        
    def get_all_prices(self):
        # Returns dict mapping from state code: price
        db = database.connect()
        cursor = database.get_cursor(db)
        state_to_price = {}
        cursor.execute("select state_codes.state_code, state_to_product.state_price \
                        from state_codes join state_to_product \
                        on state_codes.id = state_to_product.state_id \
                        where state_to_product.product_id = :input_id", \
                        input_id = self.get_id())
        state_price_tuples = cursor.fetchall()
        for state_price_tuple in state_price_tuples:
            state_to_price[state_price_tuple[0]] = state_price_tuple[1]
        database.disconnect(db)
        return state_to_price

    def get_size(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select product_size from products where id = :product_id", product_id = self._id)
        size = cursor.fetchone()[0]
        database.disconnect(db)
        return size

    # Modification Methods

    def modify_name(self, new_name):
        db = database.connect()
        cursor = database.get_cursor(db)
        if new_name:
            cursor.execute("update products set name = :name_string where id = :product_id", name_string = new_name, \
                product_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

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
        database.disconnect(db)

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
        database.disconnect(db)


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
        database.disconnect(db)

    def modify_price_per_state(self, state_code, new_price):
        # First must ensure state code in state code table
        if state_code == "ALL":
            self.set_price_for_all_states(new_price)

        else:
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
            database.disconnect(db)

    def set_price_for_all_states(self, new_price, overwrite=True):
        """ 
            Sets the price to new_price for all states in state codes list 
            If overwrite=True, sets price for all states. If =False, only sets for states not
            currently listed.
        """
        db = database.connect()
        cursor = database.get_cursor(db)

        # Ensure price is number and is positive:
        if not isinstance(new_price, (int, float, long)):
            raise ValueError("new price must be numeric type")
        if new_price < 0:
            raise ValueError("new price must be postive numeric value")

        # First need all state code ids
        cursor.execute("select id from state_codes")
        state_id_tuples = cursor.fetchall()

        for id_tuple in state_id_tuples:
            # Then must look at state-to-product table, see if price listed
            cursor.execute("select state_price from state_to_product where product_id = :p_id and state_id = :s_id", \
                p_id = self.get_id(), s_id = id_tuple[0])
            old_price = cursor.fetchone()

            # Now get state code
            cursor.execute("select state_code from state_codes where id = :input_id", \
                            input_id = id_tuple[0])
            state_code = cursor.fetchone()[0]

            # If price exists and overwrite exists, overwrite price to new_price. Otherwise, leave.
            if old_price and overwrite:
                # Existing state price overwrite:
                self.modify_price_per_state(state_code, new_price)
            # If price doesn't exist, make new row.
            elif not old_price:
                self.modify_price_per_state(state_code, new_price)
        database.disconnect(db)

    def modify_size(self, new_size):
        # ensuring it's a number:
        db = database.connect()
        cursor = database.get_cursor(db)
        if isinstance(new_size, (int, float, long)):
            cursor.execute("update products set product_size = :psize where id = :product_id", \
                psize = new_size, product_id = self.get_id())
            database.commit(db)
        database.disconnect(db)
        
    def remove(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("delete from products where id = :input_id", input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

# Static helper methods

def get_all_products_by_state(state_string):
    """ Returns mapping of product_ids to quantities for all products in all warehouses
     in given state"""
    db = database.connect()
    cursor = database.get_cursor(db)
    
    # Ensuring state is valid code
    cursor.execute("select id from state_codes where state_code = :input_code", \
                    state_code = state_string)
    state_id = cursor.fetchone()
    if not state_id:
        raise ValueError("State string %s not in list of states" %state_string)
    
    warehouse_to_stock = {}       # maps from warehouse reference to list of product refs
    products_to_quantities = {}   # maps from product ID to total quantity in state
    
    # First we get mapping from warehouse to products for all warehouse in state
    cursor.execute("select warehouses.id from warehouses join addresses \
                    on warehouses.address_id = addresses.id \
                    where addresses.state_code_id = :input_state_id",
                    input_state_id = state_id[0])
    warehouse_ids_returned = cursor.fetchall()
    database.disconnect(db)

    if not warehouse_ids_returned:
        print("no warehouses in this state.")
        return products_to_quantities
    for warehouse_id_tuple in warehouse_ids_returned:
        warehouse_ref = warehouse.Warehouse(warehouse_id_tuple[0])
        warehouse_to_stock[warehouse_ref] = warehouse_ref.get_stock()

    # Now we get mapping from products to quantities across state
    for warehouse_ref, product_list in warehouse_to_stock.items():
        for product_ref in product_list:
            if not product_ref.get_id() in products_to_quantities:
                # The product's IDis not in the mapping yet, so add it and set the
                # product's quantity equal to the current warehouse's quantity
                products_to_quantities[product_ref.get_id()] = \
                    warehouse_ref.get_product_quantity(product_ref)
            else:
                # The product's ID is already in mapping, so just incriment by quantity 
                # in warehouse
                products_to_quantities[product_ref.get_id()] += \
                    warehouse_ref.get_product_quantity(product_ref)

    return products_to_quantities

def get_all_products():
    """ Returns list of references to all products in DB """
    db = database.connect()
    cursor = database.get_cursor(db)
    cursor.execute("select id from products")
    product_list = []
    id_tuples = cursor.fetchall()
    database.disconnect(db)
    for id_tuple in id_tuples:
        product_list.append(Product(id_tuple[0]))
    return product_list

def get_product_types():
    db = database.connect()
    cursor = database.get_cursor(db)
    types = []
    cursor.execute("select product_type from product_types")
    type_tuples = cursor.fetchall()
    for type_tuple in type_tuples:
        types.append(type_tuple[0])
    return types
