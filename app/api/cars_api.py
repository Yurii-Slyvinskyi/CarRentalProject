from flask_restful import Resource, reqparse
from app.models import Cars
from app.extensions import db


car_parser = reqparse.RequestParser()

fields = [
    ('brand', str, True), ('model', str, True), ('year', int, True),
    ('body_type', str, True), ('traction', str, True), ('color', str, True),
    ('transmission', str, True), ('image_url', str, False),
    ('price_per_day', float, True), ('location', str, True), ('available', bool, False)
]

for field, dtype, required in fields:
    car_parser.add_argument(field, type=dtype, required=required, help=f"{field.capitalize()} is required")


# API for list of cars
class CarsApiList(Resource):
    def get(self):
        return [car.serialize() for car in Cars.query.all()]

    def post(self):
        args = car_parser.parse_args()
        new_car = Cars(**args)
        new_car.save()
        return {'id': new_car.id, 'message': 'Car created successfully', 'slug': new_car.slug}, 201


# API for car
class CarApi(Resource):
    def get(self, car_id):
        return Cars.query.get_or_404(car_id).serialize()

    def put(self, car_id):
        car = Cars.query.get_or_404(car_id)
        car.update_from_args(car_parser.parse_args())
        db.session.commit()
        return {'message': 'Car updated successfully'}

    def delete(self, car_id):
        car = Cars.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        return {'message': 'Car deleted successfully'}
