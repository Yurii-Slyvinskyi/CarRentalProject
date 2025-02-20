from flask import render_template, Blueprint, request, jsonify
from flask_login import login_required
from app.models import Cars


cars_bp = Blueprint('cars', __name__)


@cars_bp.route('/')
def homepage():
    return render_template('cars/homepage.html')


@cars_bp.route('/all-cars')
def all_cars():
    cars = Cars.query.all()
    return render_template('cars/all_cars.html', cars=cars)


@cars_bp.route('/car/<slug>')
def car_page(slug):
    car = Cars.query.filter_by(slug=slug).first_or_404()
    return render_template('cars/car.html', car=car)


@cars_bp.route('/filter', methods=['POST'])
def filter_cars():
    try:
        car_type = request.form.getlist('cartype')
        body_types = request.form.getlist('bodytype')
        transmissions = request.form.getlist('transmission')
        tractions = request.form.getlist('traction')
        locations = request.form.getlist('location')

        print("Filter:",car_type, body_types, transmissions, tractions, locations)  # FOR DIAGNOSTIC

        query = Cars.query

        if car_type:
            query = query.filter(Cars.car_type.in_(car_type))
        if body_types:
            query = query.filter(Cars.body_type.in_(body_types))
        if transmissions:
            query = query.filter(Cars.transmission.in_(transmissions))
        if tractions:
            query = query.filter(Cars.traction.in_(tractions))
        if locations:
            query = query.filter(Cars.location.in_(locations))

        cars = query.all()

        return jsonify([{
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'image_url': car.image_url or 'https://via.placeholder.com/150',
            'slug': car.slug
        } for car in cars])
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

