from datetime import datetime
from flask_login import UserMixin
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer(), nullable=False)

    car_type = db.Column(db.String(100), nullable=True)

    body_type = db.Column(db.String(50), nullable=False)
    traction = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    price_per_day = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    slug = db.Column(db.String(255), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'car_type': self.car_type,
            'body_type': self.body_type,
            'traction': self.traction,
            'color': self.color,
            'transmission': self.transmission,
            'image_url': self.image_url,
            'price_per_day': self.price_per_day,
            'location': self.location,
            'available': self.available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'slug': self.slug
        }

    def update_from_args(self, args):
        for k, v in args.items():
            if v is not None:
                setattr(self, k, v)

        if not db.session.object_session(self):
            db.session.add(self)


    def save(self):
        if not self.slug and self.model and self.year:
            self.slug = slugify(f"{self.model} {self.year}")
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f"Car: {self.brand} {self.model} {self.year}"


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    car = db.relationship('Cars', backref=db.backref('orders', lazy=True))
    customer_name = db.Column(db.String(100), nullable=False)
    customer_age = db.Column(db.Integer(), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'car_id': self.car_id,
            'customer_name': self.customer_name,
            'customer_age': self.customer_age,
            'customer_email': self.customer_email,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def update_from_args(self, args):
        for k, v in args.items():
            if v is not None:
                setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def complete_order(self):
        self.status = 'Completed'
        db.session.commit()

    def __repr__(self):
        return f"Order: {self.car_id} {self.customer_email}"


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    address = db.Column(db.String(155), nullable=True)
    address2 = db.Column(db.String(155), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip = db.Column(db.String(50), nullable=True)


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'created_on': self.created_on.isoformat() if self.created_on else None,
            'updated_on': self.updated_on.isoformat() if self.updated_on else None,

            'address': self.address,
            'address2': self.address2,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }

    def update_from_args(self, args):
        for k, v in args.items():
            if v is not None:
                setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.id}:{self.username}"
