#!/usr/bin/env python2

import sys

sys.path.append("../api")
sys.path.append("api")

import grocerydirect_api as api

from flask import Flask, render_template, session, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = '\xfc<\x02{\xbf\xd2\\\xcf\xe0K\xdc\xf3\xa9\xca!\xbbi\xc8[\x9c\xd1\xa1n\xff\nK\xf53\xd6R\x81\xff'

def form_entry_exists(input_name):
    return input_name in request.form and request.form[input_name]

def make_navs():
    navs = []
    if 'username' in session:
        if session['user_type'] == 'staff':
            navs.append((url_for('index'), "Staff Home"))
            navs.append((url_for('view_products'), "Products"))
            navs.append((url_for('view_warehouses'), "Warehouses"))
#        elif session['supplier'] == 'staff': 
        elif session['user_type'] == 'customer':
            navs.append((url_for('index'), "Home"))
            navs.append((url_for('view_products'), "Products"))
            navs.append((url_for('view_cart'), "Cart"))
            navs.append((url_for('address'), "Addresses"))
            navs.append((url_for('credit_cards'), "Credit Cards"))
        navs.append((url_for('logout'), "Log Out"))
    else:
        navs.append((url_for('login'), "Log In"))
    return navs

@app.after_request
def remove_if_invalid(response):
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
    return response

@app.route("/")
def index():
    account_balance = None
    orders = None
    if session['user_type'] == 'customer':
        user = api.get_person(session['user_id'])
        account_balance = user.get_balance()
        orders = user.get_order_history()
        orders = [order for order in user.get_order_history() if order.get_status() == 'pending' or order.get_status() == 'shipping']
        
    elif session['user_type'] == 'staff':
        orders = [order for order in api.get_orders() if order.get_status() == 'pending' or order.get_status() == 'shipping']
    return render_template('index.html',orders = orders, account_balance = account_balance, navs=make_navs());

@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login_post():
    if (not 'username' in request.form) or (not 'password' in request.form) or (not request.form['username']) or (not request.form['password']):
        flash("Username and password are required", category='error')
        return redirect(url_for('login'))

    # Returns person reference if valid
    person_reference = api.login(request.form["username"], request.form["password"])

    if person_reference:  
        session['logged_in'] = True
        session['username'] = request.form["username"]
        session['user_type'] = person_reference.get_type()
        session['user_id'] = person_reference.get_id()
        flash("Logged in successfully")
    else:
        flash("Username/password invalid", category='error')
        return redirect(url_for('login'))
    target = getattr(request.form, 'target', '/')
    return redirect(target)

# AUTHENTICATION

@app.route("/logout")
def logout():
    session["logged_in"] = False
    session['username'] = ""
    session["__invalidate__"] = True
    return redirect(url_for("index"))

# WAREHOUSES

@app.route("/warehouses")
def view_warehouses():
    warehouses = api.get_all_warehouses()
    # TODO - what should the return use
    return render_template('warehouses.html', warehouses=warehouses, navs=make_navs())

@app.route('/warehouses/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    warehouse = api.get_warehouse(warehouse_id)
    return render_template('warehouse.html', warehouse=warehouse, navs=make_navs())

# PRODUCTS

@app.route("/products")
def view_products():
    search_term = request.args.get('search_term', '')
    if search_term:
        products = api.get_products_by_name(search_term)
    else:
        products = api.get_all_products()
    return render_template('products.html', products=products, search_term=search_term, navs=make_navs())

@app.route("/products/add", methods=['GET'])
def new_product_page():
    if not 'user_type' in session or session['user_type'] != 'staff':
        flash("Not allowed to add products", category='warning')
        return redirect(url_for('view_products'))
    types = api.get_product_types()
    return render_template('edit_product.html', product_types=types, navs=make_navs())

@app.route("/products/<int:product_id>/edit", methods=['GET'])
def edit_product(product_id):
    if not 'user_type' in session or session['user_type'] != 'staff':
        flash("Not allowed to edit products", category='warning')
        return redirect(url_for('view_product', product_id = product_id))
    types = api.get_product_types()
    state_codes = api.get_state_codes()
    state_codes.insert(0, 'ALL')
    product = api.get_product(product_id)
    warehouses = api.get_all_warehouses()
    if product:
        return render_template('edit_product.html', warehouses = warehouses,state_codes = state_codes,product=product, product_types=types, navs=make_navs())
    flash("Product not found", category="error")
    return redirect('view_products')

@app.route("/products/<int:product_id>/edit", methods=['POST'])
def edit_product_submit(product_id):
    if not form_entry_exists('product_name'):
        flash("Need to specify name", category='error')
        return redirect(url_for('edit_product', product_id=product_id))
    if not form_entry_exists('product_type'):
        flash("Need to specify type", category='error')
        return redirect(url_for('edit_product', product_id=product_id))
    if not form_entry_exists('product_description'):
        flash("Need to specify description", category='error')
        return redirect(url_for('edit_product', product_id=product_id))
    if not form_entry_exists('product_size'):
        flash("Need to specify product size", category='error')
        return redirect(url_for('edit_product', product_id=product_id))
    if not form_entry_exists('product_nutrition') and request.form[product_type] != "non-food":
        flash("Need to specify nutrition facts for all types except non-food", category='error')
        return redirect(url_for('edit_product', product_id=product_id))
    if not form_entry_exists('product_alcohol') and request.form[product_type] == "alcoholic beverage":
        flash("Need to specify alcohol content for alcoholic beverages", category='error')
        return redirect(url_for('edit_product', product_id=product_id))
    product = api.get_product(product_id)
    updated=[]
    if product.get_name() != request.form['product_name']:
        product.modify_name(request.form['product_name'])
        updated.append("Name")
    if product.get_type() != request.form['product_type']:
        product.modify_type(request.form['product_type'])
        updated.append("Type")
    if product.get_description() != request.form['product_description']:
        product.modify_description(request.form['product_description'])
        updated.append("Description")
    if product.get_nutrition_facts() != request.form['product_nutrition']:
        product.modify_nutrition_facts(request.form['product_nutrtition'])
        updated.append("Nutrition Facts")
    if product.get_alcohol_content() != request.form['product_alcohol']:
        product.modify_alcohol_content(request.form['product_alcohol'])
        updated.append("Alcohol Content")
    if product.get_size() != int(request.form['product_size']):
        product.modify_size(int(request.form['product_size']))
        updated.append("Size")
    if (len(updated) > 0):
        flash("Updated product: " + ", ".join(updated))
    else:
        flash("Did not update product", category='warning')
    return redirect(url_for('edit_product', product_id=product_id))


@app.route("/products/add", methods=['POST'])
def add_product():
    if not form_entry_exists('product_name'):
        flash("Need to specify name", category='error')
        return redirect(url_for('new_product_page'))
    if not form_entry_exists('product_type'):
        flash("Need to specify type", category='error')
        return redirect(url_for('new_product_page'))
    if not form_entry_exists('product_description'):
        flash("Need to specify description", category='error')
        return redirect(url_for('new_product_page'))
    if not form_entry_exists('product_size'):
        flash("Need to specify product size", category='error')
        return redirect(url_for('new_product_page'))
    if not form_entry_exists('product_nutrition') and request.form['product_type'] != "non-food":
        flash("Need to specify nutrition facts for all types except non-food", category='error')
        return redirect(url_for('new_product_page'))
    if not form_entry_exists('product_alcohol') and request.form['product_type'] == "alcoholic beverage":
        flash("Need to specify alcohol content for alcoholic beverages", category='error')
        return redirect(url_for('new_product_page'))
    if not form_entry_exists('product_price'):
        flash("Need to specify price", category='error')
        return redirect(url_for('new_product_page'))

    new_product = api.make_new_product(request.form['product_name'], request.form['product_type'], \
        description = request.form['product_description'], size = int(request.form['product_size']), state_code = "ALL", \
        state_price = float(request.form['product_price']))
        
    if form_entry_exists('product_nutrition'):
        new_product.modify_nutrition_facts(request.form['product_nutrition'])
    if form_entry_exists('product_alcohol'):
        new_product.modify_alcohol_content(request.form['product_alcohol'])

    flash("Product created")
    return redirect(url_for('view_product', product_id=new_product.get_id()))

@app.route("/products/<int:product_id>")
def view_product(product_id):
    warehouses = api.get_all_warehouses()
    product = api.get_product(product_id)
    return render_template('product.html', warehouses=warehouses, product=product, navs=make_navs())

@app.route("/products/<int:product_id>/price", methods=['POST'])
def set_price(product_id):
    product = api.get_product(product_id)
    if form_entry_exists('price_state') and form_entry_exists('price_price'):
        product.modify_price_per_state(request.form['price_state'], float(request.form['price_price']))
        flash("Price set successfully")
        return redirect(url_for('edit_product', product_id = product_id))
    else:
        return redirect(url_for('edit_product', product_id = product_id))

@app.route("/products/<int:product_id>/delete", methods=['POST', 'GET'])
def delete_product(product_id):
    if session['user_type'] == 'staff':
        product = api.get_product(product_id)
        if not product:
            flash("Invalid product ID", category='warning')
            return redirect(url_for('view_products'))
        flash("Product %s removed" % product.get_name())
        product.remove()
        return redirect(url_for('view_products'))
    return redirect(url_for('logout'))

@app.route("/cart", methods=['GET'])
def view_cart():
    cart = api.get_cart(api.get_person(session['user_id']))
    products = cart.get_products_and_quantities()
    return render_template('cart.html', products=products, cart=cart, navs=make_navs())

@app.route("/cart", methods=['POST'])
def modify_cart():
    if 'diff' in request.form and 'product_id' in request.form:

        diff = int(request.form['diff'])
        product = api.get_product(int(request.form['product_id']))
        cart = api.get_person(session["user_id"]).get_cart()
        current_quantity = cart.get_product_quantity(product)
        changed_quantity = int(current_quantity + diff)

        if changed_quantity < 0:
            cart.modify_product_quantity(product, 0)
        else:
            cart.modify_product_quantity(product, changed_quantity)

        return redirect(url_for('view_cart'))
    else:
        flash("Missing some data", category='error')
        return redirect(request.referrer)

@app.route("/address")
def address():
    if session['user_type'] != 'customer':
        return redirect(url_for('index')) 
    user = api.get_person(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    addresses = user.get_addresses()
    return render_template('addresses.html', addresses=addresses, navs=make_navs())

@app.route("/address/<int:address_id>")
def view_address(address_id):
    address = api.get_address(address_id)
    return render_template('address.html', address=address, navs=make_navs());

@app.route("/address/<int:address_id>/edit", methods=['GET'])
def edit_address(address_id):
    if session['user_type'] == 'customer':
        address_types = ["billing", "shipping"]
    if session['user_type'] == 'staff':
        address_types = ['warehouse', 'supplier']
    address = api.get_address(address_id)
    state_codes = api.get_state_codes()
    return render_template('edit_address.html', address=address, address_types=address_types, state_codes = state_codes, navs=make_navs())

@app.route("/address/<int:address_id>/edit", methods=['POST'])
def edit_address_post(address_id):
    address = api.get_address(address_id)
    updated = []
    if address.get_type() != request.form['address_type']:
        address.modify_type(request.form['address_type'])
        updated.append("Type")
    if address.get_street() != request.form['address_street']:
        address.modify_street(request.form['address_street'])
        updated.append("Street")
    if address.get_apartment_no() != request.form['address_apartment_no']:
        address.modify_apartment_no(request.form['address_apartment_no'])
        updated.append("Street 2")
    if address.get_city() != request.form['address_city']:
        address.modify_city(request.form['address_city'])
        updated.append("City")
    if address.get_state() != request.form['address_state']:
        address.modify_state(request.form['address_state'])
        updated.append("State")
    if address.get_zip_code() != int(request.form['address_zip_code']):
        address.modify_zip_code(int(request.form['address_zip_code']))
        updated.append("Zip Code")
    if address.get_default_flag() != ('address_default' in request.form):
        address.set_default_flag(('address_default' in request.form))
        updated.append("Default")
    if (len(updated) > 0):
        flash("Updated address " + ", ".join(updated))
    else:
        flash("Did not update address", category='warning')
    return redirect(url_for('edit_address', address_id = address_id))

@app.route("/address/add", methods=['GET'])
def add_address():
    if session['user_type'] == 'customer':
        address_types = ["billing", "shipping"]
    if session['user_type'] == 'staff':
        address_types = ['warehouse', 'supplier']
    state_codes = api.get_state_codes()
    return render_template('edit_address.html', state_codes = state_codes, address_types = address_types, navs=make_navs())

@app.route("/address/add", methods=['POST'])
def add_address_post():
    address = api.make_new_address(request.form['address_street'], request.form['address_city'], request.form['address_state'], int(request.form['address_zip_code']), request.form['address_type'], api.get_person(session['user_id']), apt_no=request.form['address_apartment_no'])
    address.set_default_flag(('address_default' in request.form))
    return redirect(url_for('view_address', address_id = address.get_id()))

@app.route("/address/<int:address_id>/delete", methods=['POST'])
def delete_address(address_id):
    address = api.get_address(address_id)
    if address:
        address.remove()
        flash("Address removed")
    else:
        flash("Invalid address id", category='error')
    return redirect(url_for('address'))

@app.route("/credit_cards")
def credit_cards():
    if session['user_type'] != 'customer':
        return redirect(url_for('index')) 
    user = api.get_person(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    credit_cards = user.get_credit_cards()
    return render_template('credit_cards.html', credit_cards=credit_cards, navs=make_navs())

@app.route("/credit_cards/<int:credit_card_id>")
def view_credit_card(credit_card_id):
    credit_card = api.get_credit_card(credit_card_id)
    return render_template('credit_card.html', credit_card=credit_card, navs=make_navs());

@app.route("/credit_cards/<int:credit_card_id>/edit", methods=['GET'])
def edit_credit_card(credit_card_id):
    credit_card_types = api.get_card_types()
    credit_card = api.get_credit_card(credit_card_id)
    addresses = [address for address in api.get_person(session['user_id']).get_addresses() if address.get_type() == 'billing']
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] 
    years = ["2017", "2018", "2019", "2020", "2021", "2022"]
    return render_template('edit_credit_card.html', credit_card=credit_card, addresses=addresses, credit_card_types=credit_card_types, months=months, years=years, navs=make_navs())

@app.route("/credit_cards/<int:credit_card_id>/edit", methods=['POST'])
def edit_credit_card_post(credit_card_id):
    credit_card = api.get_credit_card(credit_card_id)
    updated = []
    if credit_card.get_card_type() != request.form['credit_card_type']:
        credit_card.modify_type(request.form['credit_card_type'])
        updated.append("Type")
    if request.form['credit_card_number'] and credit_card.get_card_number() != request.form['credit_card_number']:
        credit_card.modify_card_number(int(request.form['credit_card_number']))
        updated.append("Number")
    if request.form['credit_card_security_code']:
        credit_card.modify_security_code(int(request.form['credit_card_security_code']))
        updated.append("Security Code")
    if credit_card.get_expiration_date().month != int(request.form['credit_card_expiration_month']):
        credit_card.modify_expiration_date(int(request.form['credit_card_expiration_month']), credit_card.get_expiration_date().year)
        updated.append("Expiration Month")
    if credit_card.get_expiration_date().year != int(request.form['credit_card_expiration_year']):
        credit_card.modify_expiration_date(credit_card.get_expiration_date().month, int(request.form['credit_card_expiration_year']))
        updated.append("Expiration Year")
    if credit_card.get_address().get_id != request.form['credit_card_address_id']:
        credit_card.modify_address(api.get_address(int(request.form['credit_card_address_id'])))
        updated.append("Address")
    if (len(updated) > 0):
        flash("Updated Credit Card " + ", ".join(updated))
    else:
        flash("Did not update credit_card", category='warning')
    return redirect(url_for('edit_credit_card', credit_card_id = credit_card_id))

@app.route("/credit_cards/add", methods=['GET'])
def add_credit_card():
    credit_card_types = api.get_card_types()
    addresses = [address for address in api.get_person(session['user_id']).get_addresses() if address.get_type() == 'billing']
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] 
    years = ["2017", "2018", "2019", "2020", "2021", "2022"]
    state_codes = api.get_state_codes()
    return render_template('edit_credit_card.html', addresses=addresses, credit_card_types=credit_card_types, months=months, years=years, navs=make_navs())

@app.route("/credit_cards/add", methods=['POST'])
def add_credit_card_post():
    credit_card = api.make_new_credit_card(api.get_person(session['user_id']), int(request.form['credit_card_number']), int(request.form['credit_card_security_code']), int(request.form['credit_card_expiration_month']), int(request.form['credit_card_expiration_year']), request.form['credit_card_type'], api.get_address(int(request.form['credit_card_address_id'])))
    return redirect(url_for('view_credit_card', credit_card_id = credit_card.get_id()))

@app.route("/credit_cards/<int:credit_card_id>/delete", methods=['POST'])
def delete_credit_card(credit_card_id):
    credit_card = api.get_credit_card(credit_card_id)
    if credit_card:
        credit_card.remove()
        flash("Address removed")
    else:
        flash("Invalid credit_card id", category='error')
    return redirect(url_for('credit_cards'))

@app.route("/cart/submit")
def cart_submit():
    if session['user_type'] != 'customer':
        flash("You don't have a cart to submit", category='error')
        return redirect(url_for('index'))
    user = api.get_person(session['user_id'])
    order_id = user.submit_cart()
    flash("Cart submitted as order id: %d" % order_id)
    return redirect(url_for('index'))

@app.route("/products/<int:product_id>/add_to_warehouse", methods=['POST'])
def add_to_warehouse(product_id):
    if session['user_type'] != 'staff':
        flash("You can't add things to warehouses", category='error')
        return redirect(url_for('index'))

    product = api.get_product(product_id)
    warehouse = api.get_warehouse(int(request.form['product_warehouse_id']))
    quantity = int(request.form['product_quantity'])
    old_quantity = warehouse.get_product_quantity(product)
    warehouse.add_product(product)
    warehouse.modify_quantity(product, quantity + old_quantity)
    flash("Product added to warehouse successfully")
    return redirect(url_for('view_product', product_id=product_id))


if __name__ == "__main__":
    app.run(debug=True)

