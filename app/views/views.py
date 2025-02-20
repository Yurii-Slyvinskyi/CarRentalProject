# from email.message import Message
# from tkinter.font import names
#
# from flask import render_template, Blueprint, flash, redirect, url_for
# from flask_login import login_required, login_user, current_user, logout_user
#
# import app
# from app.forms import OrderForm, LoginForm, RegistrationFrom
# from app import db, login_manager
# from app.models import Orders, Cars, Users
# from app.utils import send_mail
#
#
# main = Blueprint('main', __name__)
#
#
# @main.route('/')
# def homepage():
#     return render_template('homepage.html')
#
#
# @main.route('/all-cars')
# def all_cars():
#     cars = Cars.query.all()
#     return render_template('all_cars.html', cars=cars)
#
#
# @main.route('/car/<slug>')
# def car_page(slug):
#     car = Cars.query.filter_by(slug=slug).first_or_404()
#     return render_template('car.html', car=car)
#
#
# # Form Function
# @main.route('/order-form/<slug>', methods=['GET', 'POST'])
# def order_form(slug):
#     form = OrderForm()
#     car = Cars.query.filter_by(slug=slug).first_or_404()
#
#     form.car_id.data = car.id
#
#     if form.validate_on_submit():
#         car_id = car.id
#         customer_name = form.customer_name.data
#         customer_age = form.customer_age.data
#         customer_email = form.customer_email.data
#         start_date = form.start_date.data
#         end_date = form.end_date.data
#
#         new_order = Orders(car_id=car_id, customer_name=customer_name,
#                           customer_age=customer_age, customer_email=customer_email,
#                           start_date=start_date, end_date=end_date)
#
#         db.session.add(new_order)
#         db.session.commit()
#
#         send_mail(
#             subject='Car Rental Request',
#             recipient=customer_email,
#             template='mail/feedback.html',
#             customer_name=customer_name,
#             customer_email=customer_email,
#             car=car
#         )
#
#         # flash('Your car rent request has been submitted!')
#         return redirect(url_for('main.thank_you', slug=car.slug))
#
#     return render_template('order.html', form=form, car=car)
#
#
# #Authorization
# @login_manager.user_loader
# def load_user(user_id):
#     return db.session.query(Users).get(user_id)
#
#
# @main.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         user = db.session.query(Users).filter(Users.username == form.username.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember.data)
#             return redirect(url_for('main.user_profile'))
#
#         flash("Invalid username/password", 'error')
#         return redirect(url_for('main.login'))
#     return render_template('authorization/login.html', form=form)
#
#
# @main.route('/logout/')
# @login_required
# def logout():
#     logout_user()
#     flash("You have been logged out.")
#     return redirect(url_for('main.login'))
#
#
# @main.route('/registration/', methods=['GET', 'POST'])
# def registration():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.all_cars'))
#
#     form = RegistrationFrom()
#
#     if form.validate_on_submit():
#         existing_user = Users.query.filter((Users.email == form.email.data) | (Users.username == form.username.data)).first()
#
#         if existing_user:
#             flash('This email or username is already registered. Please use another one.', 'danger')
#             return redirect(url_for('main.registration'))
#
#         new_user = Users(
#             name=form.name.data,
#             username=form.username.data,
#             email=form.email.data
#         )
#         new_user.set_password(form.password.data)
#
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Your account has been created successfully!', 'success')
#             return redirect(url_for('main.login'))
#         except Exception as e:
#             flash(f'There was an issue creating your account: {e}', 'danger')  # Покажемо помилку
#
#     return render_template('authorization/registration.html', form=form)
#
#
# @main.route('/user-profile/')
# @login_required
# def user_profile():
#     return render_template('authorization/profile.html')
#
#
# # Else basic functions
# @main.route('/thank_you/<slug>')
# def thank_you(slug):
#     car = Cars.query.filter_by(slug=slug).first_or_404()
#     return render_template('thank_you.html', car=car)
#
#
# @main.route('/admin/')
# @login_required
# def admin():
#     return render_template('admin.html')
