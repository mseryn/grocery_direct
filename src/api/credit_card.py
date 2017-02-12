#***
#*  GroceryDirect - Credit Card Class
#*  
#*  Author: Melanie Cornelius, mseryn
#*  Written for CS 425-02 Fall 2016 Final Project
#*  
#*  Warehouse Description:
#*  - has:
#*      -- id
#*      -- address (id)
#*      -- card number
#*      -- security code
#*      -- expiration date
#*      -- type 
#*      -- person ID
#*  - get:
#*      -- address (id)
#*      -- card number
#*      -- security code
#*      -- expiration date
#*      -- type 
#*      -- person ID
#*  - modify:
#*      -- address (id)
#*      -- card number
#*      -- security code
#*      -- expiration date
#*      -- type 
#***

import address
import database
import person

import datetime


class CreditCard():

    def __init__(self, given_id):
        db = database.connect()
        cursor = database.get_cursor(db)
        # Ensuring given ID is int
        if isinstance(given_id, int):
            # Ensuring card ID is in credit card table
            cursor.execute("select id from credit_cards where id = :card_id", card_id = given_id)
            if cursor.fetchone():
                self._id = given_id
            else:
                raise ValueError("Given ID not in credit cards table, id: %i" %given_id)
        else:
            raise ValueError("Given ID not an int, id: %s" %str(given_id))
        database.disconnect(db)

    @staticmethod
    def new_credit_card(person_reference, card_number, security_code, expiration_month, \
        expiration_year, type_string, address_reference):
        # Adding new warehouse to database, and returning reference to that warehouse
        db = database.connect()
        cursor = database.get_cursor(db)

        # type-checking numeric inputs
        if not isinstance(card_number, int):
            raise ValueError("Card number must be integer value")
        if not isinstance(security_code, int):
            raise ValueError("Security code must be integer value")
        if not isinstance(expiration_month, int):
            raise ValueError("Expiration month must be integer value")
        if not isinstance(expiration_year, int):
            raise ValueError("Expiration year must be integer value")

        # value checking numeric inputs
        if not len(str(card_number)) == 16:
            raise ValueError("Card number must be int of 16 digits")
        if not len(str(security_code)) == 3:
            raise ValueError("Security code must be into of 3 digits")
        if expiration_month > 12 or expiration_month < 1:
            raise ValueError("Expiration month must be between 1 and 12")
        if not len(str(expiration_year)) == 4:
            raise ValueError("Expiration year must be 4 digit integer")

        # Ensuring person's ID is in persons table
        cursor.execute("select id from persons where id = :input_id", \
                        input_id = person_reference.get_id())
        person_id = cursor.fetchone()
        if not person_id:
            raise ValueError("Person not found in persons table.")
        else:
            person_id = person_id[0]

        # Ensuring address' ID is in addresses table AND it is a billing address
        cursor.execute("select id from addresses \
                        where id = :input_id", \
                        input_id = address_reference.get_id())
        address_id = cursor.fetchone()
        if not address_id:
            raise ValueError("Address not found in addresses table")
        else:
            address_id = address_id[0]

        if not address_reference.get_type() == "billing":
            raise ValueError("Address must be billing type. Type is %s." %address_reference.get_type())

        # Ensuring type string has associated ID in card types table
        cursor.execute("select id from card_types where card_type = :input_type", \
                        input_type = type_string)
        type_id = cursor.fetchone()
        if not type_id:
            raise ValueError("Card type string %s not found in card types table" %type_string)
        else:
            type_id = type_id[0]

        # Formatting the date
        expiration_date = format_date(expiration_month, expiration_year)

        # Making variable to hold stored returned ID
        returned_id = returned_id = cursor.var(database.cx_Oracle.NUMBER)

        # Finally, putting it all into the credit_cards table:
        cursor.execute("insert into credit_cards \
                        (card_number, security_code, expiration_date, card_type_id, \
                        billing_addr_id, person_id) \
                        values (:input_card_no, :input_security_code, :input_expiration_date, \
                        :input_type_id, :input_addr_id, :input_person_id) \
                        returning id into :new_card_id", \
                        input_card_no = card_number, input_security_code = security_code, \
                        input_expiration_date = expiration_date, input_type_id = type_id, \
                        input_addr_id = address_id, input_person_id = person_id, \
                        new_card_id = returned_id)
        database.commit(db)

        returned_id = int(returned_id.getvalue())

        database.disconnect(db)
        return CreditCard(returned_id)

    # Get Methods

    def get_id(self):
        return self._id

    def get_person(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select person_id from credit_cards where id = :input_id", \
                        input_id = self.get_id())
        person_id = cursor.fetchone()
        database.disconnect(db)
        if not person_id:
            raise Exception("Person not found in table. This should never happen, fatal.")
        return person.Person(person_id[0])

    def get_address(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select billing_addr_id from credit_cards where id = :input_id", \
                        input_id = self.get_id())
        returned_id = cursor.fetchone()
        database.disconnect(db)
        if not returned_id:
            raise Exception("Address not found in table. This sould never happen, fatal.")
        return address.Address(returned_id[0])

    def get_card_number(self):
        # Note: this returns the last 4 digits of the card number
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select card_number from credit_cards \
                        where id = :input_id", \
                        input_id = self.get_id())
        card_no = cursor.fetchone()
        database.disconnect(db)
        if not card_no:
            raise Exception("Card number not found in table. This should never happen, fatal.")
        # Returning last 4 digits
        return card_no[0] % 1000

    def get_card_type(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select card_types.card_type \
                        from card_types join credit_cards \
                        on card_types.id = credit_cards.card_type_id \
                        where credit_cards.id = :input_id", \
                        input_id = self.get_id())
        type_string = cursor.fetchone()
        database.disconnect(db)
        if not type_string:
            raise ValueError("Type string/ID not found in table. This should never happen, fatal.")
        return type_string[0]

    def get_expiration_date(self):
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select expiration_date from credit_cards \
                        where id = :input_id", \
                        input_id = self.get_id())
        date = cursor.fetchone()
        if not date:
            raise ValueError("Date not found, this should never happen. Fatal.")
        date = date[0]   # This should be a datetime.datetime object by CX oracle's documentation
        # note this will have a time and day associated with it that are useless
        return date

    # Check Method

    def check_security_code(self, sec_code):
        # Ensures given code matches stored code
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select security_code from credit_cards \
                        where id = :input_id", \
                        input_id = self.get_id())
        stored_code = cursor.fetchone()
        database.disconnect(db)
        if not stored_code[0] == sec_code:
            return False
        else:
            return True

    # Modification Methods

    def modify_type(self, new_type_string):
        # Ensuring type string has associated ID in card types table
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select id from card_types where card_type = :input_type", \
                        input_type = new_type_string)
        type_id = cursor.fetchone()
        if not type_id:
            raise ValueError("Card type string %s not found in card types table" %type_string)
        type_id = type_id[0]
        cursor.execute("update credit_cards set card_type_id = :input_type \
                        where id = :input_id", \
                        input_type = type_id, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_card_number(self, new_number):
        # Type- and value-checking inputs
        if not isinstance(new_number, int):
            raise ValueError("Card number must be integer value")
        if not len(str(new_number)) == 16:
            raise ValueError("Card number must be int of 16 digits")
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update credit_cards set card_number = :input_number \
                        where id = :input_id",\
                        input_number = new_number, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_security_code(self, new_code):
        # Type- and value-checking inputs
        if not isinstance(new_code, int):
            raise ValueError("Security code must be integer value")
        if not len(str(new_code)) == 3:
            raise ValueError("Security code must be into of 3 digits")
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update credit_cards set security_code = :input_code \
                        where id = :input_id",\
                        input_code = new_code, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_address(self, new_address_reference):
        # Ensuring address' ID is in addresses table AND it is a billing address
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("select id from addresses \
                        where id = :input_id", \
                        input_id = new_address_reference.get_id())
        address_id = cursor.fetchone()
        if not address_id:
            raise ValueError("Address not found in addresses table")
        else:
            address_id = address_id[0]
        address_reference = address.Address(address_id)
        if not address_reference.get_type() == "billing":
            raise ValueError("Address must be billing type. Type is %s." %address_reference.get_type())
        cursor.execute("update credit_cards set billing_addr_id = :input_addr \
                        where id = :input_id",\
                        input_addr = address_id, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

    def modify_expiration_date(self, new_expiration_month, new_expiration_year):
        # Type- and value-checking inputs
        if not isinstance(new_expiration_month, int):
            raise ValueError("Expiration month must be integer value")
        if not isinstance(new_expiration_year, int):
            raise ValueError("Expiration year must be integer value")
        if new_expiration_month > 12 or new_expiration_month < 1:
            raise ValueError("Expiration month must be between 1 and 12")
        if not len(str(new_expiration_year)) == 4:
            raise ValueError("Expiration year must be 4 digit integer")
        # Formatting the date
        expiration_date = format_date(new_expiration_month, new_expiration_year)
        db = database.connect()
        cursor = database.get_cursor(db)
        cursor.execute("update credit_cards set expiration_date = :input_date \
                        where id = :input_id",\
                        input_date = expiration_date, input_id = self.get_id())
        database.commit(db)
        database.disconnect(db)

# Helper methods

def format_date(month, year):
    # We use the datetime library to get formatted datetime objects
    # We don't care about the day or time in this case, so set to useless values
    date_object = datetime.datetime(year, month, 1, 0, 0)
    return date_object.strftime('%d-%b-%Y')
