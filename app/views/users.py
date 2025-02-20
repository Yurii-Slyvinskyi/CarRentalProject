from flask import render_template, redirect, url_for, flash, Blueprint, request, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from app.models import Users
from app.forms import LoginForm, RegistrationFrom
from app import db, login_manager


users_bp = Blueprint('users', __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@users_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(Users).filter(Users.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('users.profile'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('users.login'))
    return render_template('authorization/login.html', form=form)


@users_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('users.login'))


@users_bp.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_profile'))

    form = RegistrationFrom()

    if form.validate_on_submit():
        existing_user = Users.query.filter((Users.email == form.email.data) | (Users.username == form.username.data)).first()

        if existing_user:
            flash('This email or username is already registered. Please use another one.', 'danger')
            return redirect(url_for('users.registration'))

        new_user = Users(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created successfully!', 'success')
            return redirect(url_for('users.login'))
        except Exception as e:
            flash(f'There was an issue creating your account: {e}', 'danger')

    return render_template('authorization/registration.html', form=form)


@users_bp.route('/profile')
@login_required
def profile():
    return render_template('authorization/profile.html', current_user=current_user)


@users_bp.route('/user-profile/', methods=['POST'])
@login_required
def user_profile():
    data = request.get_json()  # Use get_json to properly parse JSON data
    user = Users.query.filter_by(username=current_user.username).first()

    if user:
        user.full_name = data['full_name']
        user.username = data['username']
        user.email = data['email']
        user.address = data['address']
        user.address2 = data['address2']
        user.city = data['city']
        user.state = data['state']
        user.zip = data['zip']

        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200
    else:
        return jsonify({"message": "User not found!"}), 404

    

@users_bp.route('/admin/')
@login_required
def admin():
    return render_template('authorization/admin.html')
