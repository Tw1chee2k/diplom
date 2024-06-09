from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, json
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Tovar, Sklad, Cart, Order, Comment, Message, Point
from . import db
from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from sqlalchemy import func
import smtplib
from email.mime.multipart  import MIMEMultipart
from email.mime.text import MIMEText
import re
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = str(request.form.get('password'))
        remember = True if request.form.get('remember') else False 
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if user:    
            if check_password_hash(user.password, password):
                flash('Authorization was successful', category='success')
                login_user(user, remember=remember) 
                return redirect(url_for('views.catalog'))
            else:
                flash('Incorrect password', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('There is no user with this email address', category='error')
            return redirect(url_for('auth.login')) 
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfstrly', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('A user with this email already exists', category='error')
        elif not re.match(r'[\w\.-]+@[\w\.-]+', email):
            flash('Invalid email address', category='error')
        elif password1!=password2:
            flash('An error occurred in confirming the password', category='error')
        else:
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(password2))
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('The account has been created', category='success')
            return redirect(url_for('views.catalog'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/forgot_password', methods=['POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            send_email(f'Your new password is {gener_password()}, if desired, you can change it in your profile settings', email)   
            user.password = generate_password_hash(gener_password())
            db.session.commit()
            flash('A new password has been sent to your email', category='success')
            return redirect(url_for('views.login'))
        else:
            flash('There is no user with this email address', category='error')
            return redirect(url_for('views.login'))
    return render_template("login.html", user=current_user)

def send_email(message_body, recipient_email):
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587 
    email_address = 'tw1.ofcompay@mail.ru'  
    email_password = '6McTMF3uX2chGcFchUmZ'
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = recipient_email
    message['Subject'] = 'Message for user'
    message.attach(MIMEText(message_body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls() 
    server.login(email_address, email_password)
    server.send_message(message)
    server.quit()

def gener_password():
    password = '1111'
    return password

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
        return render_template("account.html", user=current_user)

@auth.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if current_user.is_authenticated:
        tovar_name = request.form.get('tovar_name')
        user_email = current_user.email
        quantity = int(request.form.get('tovar_count'))
        price = float(request.form.get('tovar_cost'))
        existing_item = Cart.query.filter_by(user_email=user_email, tovar_name=tovar_name).first()
        tovar = Tovar.query.filter_by(name=tovar_name).first()
        if tovar.count <= 0:
            flash(f'No in stoke {tovar_name} mat', category='error')
            return redirect(url_for('views.product', name=tovar_name))
        else:
            if existing_item:
                if existing_item.quantity + quantity <= tovar.count: 
                    existing_item.quantity += quantity
                    existing_item.price += float(price)
                else:
                    flash(f'Count of {tovar_name} mat is less than required', category='error')
                    return redirect(url_for('views.product', name=tovar_name))
            else:
                new_item = Cart(
                    user_email=user_email, 
                    tovar_name=tovar_name, 
                    quantity=quantity, 
                    price=price)
                db.session.add(new_item)
            db.session.commit()
            flash('Tovar added to cart', category='success')
            return redirect(url_for('views.product', name=tovar_name))
    else:
        flash('Need to authenticate', category='error')
        return redirect(url_for('views.catalog'))


@auth.route('/cart', methods=['GET', 'POST'])
def createorder():
    if request.method == 'POST': 
        items = Cart.query.filter_by(user_email=current_user.email).all()
        all_cart_price = round(sum(item.price for item in items), 2)
        type = ''        
        max_nomerzakaza = db.session.query(func.max(Order.nomerzakaza)).scalar()
        nomerzakaza = max_nomerzakaza + 1 if max_nomerzakaza is not None else 1  
        fio = request.form.get('fio')
        telephone = request.form.get('telephone')
        receiving_point = request.form.get('receiving_point')
        country = request.form.get('country')
        city = request.form.get('cityInput')
        street = request.form.get('street')
        house = request.form.get('house')
        flat = request.form.get('flat')
        comment = request.form.get('comment')
        promocod = request.form.get('promocod')

        cart_items = Cart.query.filter_by(user_email=current_user.email).all()
        if cart_items:
            if receiving_point:
                type = 'Delivery across the RB to the branch (Evropochta)' 
                current_point = Point.query.filter_by(number=receiving_point).first()
                current_point = current_point.id
                all_cart_price = round(all_cart_price + 2.5, 2)
            elif country and city:
                type =  'Worldwide shipping'  
                current_point = None
                all_cart_price = round(all_cart_price + 7.5, 2)
            else:
                type = "Door-to-door delivery in the RB (Evropochta)"
                current_point = None
                all_cart_price = round(all_cart_price + 4.5, 2)
            if country == '':
                country = 'Belarus'
            for item in cart_items:
                new_order = Order(nomerzakaza=nomerzakaza, 
                                type = type,
                                fio=fio, 
                                email=current_user.email, 
                                telephone=telephone, 
                                receiving_point=current_point,
                                street=street,
                                house=house,
                                flat=flat,
                                city=city, 
                                country=country, 
                                comment=comment, 
                                promocod=promocod,             
                                price = item.price, 
                                tovar_name=item.tovar_name, 
                                tovar_quantity=item.quantity
                                )
                db.session.add(new_order)
                tovar = Tovar.query.filter_by(name=item.tovar_name).first()
                if tovar:
                    tovar.count -= item.quantity
                    Cart.query.filter_by(user_email=current_user.email).delete()
                    db.session.commit()          
            current_tovar = Tovar.query.filter_by(name=item.tovar_name).all() 
            for i in current_tovar:
                if i.count == 0:
                    i.status = "Sold"
                    db.session.commit()        
            new_massage = Message(
                text = f"The order №{new_order.nomerzakaza} has been added to the processing",
                user_email = current_user.email, 
                category = True,
            )
            db.session.add(new_massage)
            db.session.commit()
            flash('Order added!', category='success')
            return redirect(url_for('views.profile_orders'))
        else:
            flash('Add items in Cart')
    return render_template("cart.html", user=current_user)

@auth.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        tovar_id = request.form.get('tovar_id')
        text = request.form.get('text')
        name_tovar = Tovar.query.filter_by(id=tovar_id).first()
        if current_user.is_authenticated:    
            if tovar_id and text:
                user_id = current_user.id
                new_comment = Comment(text=text, user_id=user_id, tovar_id=tovar_id)
                db.session.add(new_comment)
                db.session.commit()
                flash("The comment has been added successfully", category='success')
                return redirect(url_for('views.product', name=name_tovar.name))
            else:
                flash("Error: there is not enough data to add a comment", category='error')
                return redirect(url_for('views.product', name=name_tovar.name))
        else:      
            flash("Need to login", category='error')        
            return redirect(url_for('views.product', name=name_tovar.name))
    else:
        flash("Error: Invalid request method", category='error')
        return redirect(url_for('views.product', name=name_tovar.name))
      
@auth.route('/profile/password', methods=['POST'])
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        conf_new_password = request.form.get('conf_new_password')
        if old_password and new_password and conf_new_password:
            user = User.query.filter_by(email=current_user.email).first()
            if not check_password_hash(current_user.password, old_password):
                flash('Incorrect old password', category='error')
                return redirect(url_for('views.profile_password'))
            elif new_password != conf_new_password:
                flash('An error occurred while confirming the password', category='error')
                return redirect(url_for('views.profile_password'))
            else:
                user.password = generate_password_hash(conf_new_password)
                db.session.commit()
                flash('The password change was successful', category='success')
                send_email(f'Your password has been changed to {conf_new_password}', current_user.email)
                return redirect(url_for('views.login'))
        else:
            flash('Need to input your info')
            return redirect(url_for('views.profile_password'))

@auth.route('/profile/orders', methods=['POST'])
@login_required
def cancel_order():
    if request.method == 'POST':
        nomerzakaza = request.form.get('nomerzakaza')
        current_order = Order.query.filter_by(nomerzakaza=nomerzakaza).all()
        if not current_order:
            flash('Order not found', category='error')
            return redirect(url_for('views.profile_orders'))
        else:
            if current_order[0].status == 'Cancelled':
                flash('The order is already cancelled', category='info')
            elif current_order[0].status == 'In processing':
                current_order[0].status = 'Cancelled'
                order_items = Order.query.filter_by(nomerzakaza=nomerzakaza).all()
                for item in order_items:
                    tovar = Tovar.query.filter_by(name=item.tovar_name).first()
                    if tovar:
                        tovar.count += item.tovar_quantity
                        tovar.status = "In stoke"
                        db.session.commit()         
                db.session.commit()
                flash("Order status changed to Cancelled", category='success')
            else:
                flash("You cannot cancel this order because it has already been processed", category='error')
            return redirect(url_for('views.profile_orders'))
            