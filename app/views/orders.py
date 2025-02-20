from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.models import Orders, Cars
from app.forms import OrderForm
from app.utils import send_mail
from app import db


orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/order-form/<slug>', methods=['GET', 'POST'])
def order_form(slug):
    form = OrderForm()
    car = Cars.query.filter_by(slug=slug).first_or_404()

    form.car_id.data = car.id

    if form.validate_on_submit():
        car_id = car.id
        customer_name = form.customer_name.data
        customer_age = form.customer_age.data
        customer_email = form.customer_email.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        new_order = Orders(car_id=car_id, customer_name=customer_name,
                          customer_age=customer_age, customer_email=customer_email,
                          start_date=start_date, end_date=end_date)

        db.session.add(new_order)
        db.session.commit()

        send_mail(
            subject='Car Rental Request',
            recipient=customer_email,
            template='mail/feedback.html',
            customer_name=customer_name,
            customer_email=customer_email,
            car=car
        )

        # flash('Your car rent request has been submitted!')
        return redirect(url_for('orders.thank_you', slug=car.slug))

    return render_template('orders/order.html', form=form, car=car)


@orders_bp.route('/thank_you/<slug>')
def thank_you(slug):
    car = Cars.query.filter_by(slug=slug).first_or_404()
    return render_template('orders/thank_you.html', car=car)
