from datetime import datetime, timezone
from app.models import Cars, Orders, Users
from app.extensions import db


# Models Cars tests

def create_sample_car():
    car = Cars(
        brand='Toyota',
        model='Corolla',
        year=2020,
        car_type='Sedan',
        body_type='Sedan',
        traction='Front-wheel drive',
        color='Red',
        transmission='Automatic',
        price_per_day=50.0,
        location='Edmonton, AB',
        available=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    car.save()
    return car


def test_create_car(test_app):
    car = create_sample_car()
    saved_car = Cars.query.first()
    assert saved_car.brand == 'Toyota'
    assert saved_car.model == 'Corolla'
    assert saved_car.slug == 'corolla-2020'


def test_serialize_car(test_app):
    car = create_sample_car()
    serialized_data = car.serialize()
    assert serialized_data['id'] == car.id
    assert serialized_data['brand'] == car.brand
    assert serialized_data['model'] == car.model
    assert serialized_data['year'] == car.year
    assert serialized_data['slug'] == car.slug
    assert 'created_at' in serialized_data
    assert 'updated_at' in serialized_data


def test_update_car(test_app):
    car = create_sample_car()  # Створюємо машину

    update_args = {
        'brand': 'Honda',
        'model': 'Civic',
        'year': 2022,
        'color': 'Blue',
        'price_per_day': 60.0
    }

    car.update_from_args(update_args)  # Update
    updated_car = db.session.get(Cars, car.id)  # Get from db again

    assert updated_car.brand == 'Honda'
    assert updated_car.model == 'Civic'
    assert updated_car.year == 2022
    assert updated_car.color == 'Blue'
    assert updated_car.price_per_day == 60.0

# Models Orders tests



