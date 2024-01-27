from . import main
from flask import render_template, request, current_app, jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
# import cloudinary
# from cloudinary.uploader import upload
from ..models import Product, Cart, User
from .. import db
import os
from sqlalchemy import or_, and_, func


@main.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@main.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        units = request.form.get('units')
        category = request.form.get('category')
        unit = request.form.get('units_specific')
        # thumbnail = request.form.get('image')
        description = request.form.get('description')

        product = Product(name=name, price=price, quantity=units, category=category, unit=unit, description=description, user_id=current_user.id)
        db.session.add(product)
        db.session.commit()

        flash('Product added successfully')
        return redirect(url_for('main.user_products', id=current_user.id))

    return render_template('add_product.html')

# def upload_file(image):
#     current_app.logger.info('in upload route')

#     cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
#     upload_result = None

#     current_app.logger.info('%s file_to_upload', image)

#     if image:
#         upload_result = upload(image)
#         current_app.logger.info(upload_result)
#         return jsonify(upload_result)

@main.route("/products", methods=['GET', 'POST'])
@login_required
def products():
    products = None
    users = User.query.with_entities(User.location).distinct()

    if request.method == 'POST':
        key_term_search = request.form.get('keyword_search')
        location_filter = request.form.get('location_filter')
        # cost_filter = request.form.get('cost_filter') or 0
        category_filter = request.form.get('category_filter')

        products = Product.query.join(User).filter(and_(func.lower(Product.name).like("%" + func.lower(key_term_search) + "%"), func.lower(User.location).like("%" + func.lower(location_filter) + "%"),  func.lower(Product.category).like("%" + func.lower(category_filter) + "%"))).all()     

        return render_template("products.html", products=products, users=users)

    products = Product.query.all()
    return render_template("products.html", products=products, users=users)

@main.route("/<int:id>/products", methods=['GET'])
@login_required
def user_products(id):
    products = current_user.products
    return render_template("user_products.html", products=products)

@main.route("/products/<int:id>/remove", methods=['GET'])
def remove_product(id):
    product = Product.query.get(id)
    if not product:
        flash('Product does not exist')
        return redirect(url_for('main.user_products', id=current_user.id))

    db.session.delete(product)
    db.session.commit()
    flash('Product removed successfully')
    return redirect(url_for('main.user_products', id=current_user.id))

@main.route("/<int:id>/cart", methods=['GET', 'POST'])
@login_required
def cart(id):
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        new_product = Cart(quantity=quantity, product_id=id, user_id=current_user.id)
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added to cart')
        return redirect(url_for('main.products'))

    carts = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template("cart.html", carts=carts)

@main.route("/cart/remove/<int:id>", methods=["GET"])
def remove_cart(id):
    cart = Cart.query.get(id)
    db.session.delete(cart)
    db.session.commit()

    return redirect(url_for('main.cart', id=current_user.id))