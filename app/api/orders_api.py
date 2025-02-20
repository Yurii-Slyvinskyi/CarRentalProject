from flask_restful import Resource, reqparse
from app.models import Orders
from app.extensions import db


order_parser = reqparse.RequestParser()

fields = [
    ('car_id', int, True), ('customer_name', str, True),
    ('customer_age', int, True), ('customer_email', str, True),
    ('start_date', str, True), ('end_date', str, True), ('status', str, False)
]

for field, dtype, required in fields:
    order_parser.add_argument(fields, type=dtype, required=required, help=f"{field.capitalize()} is required")


class OrdersApiList(Resource):
    def get(self):
        return [order.serialize() for order in Orders.query.all()]

    def post(self):
        args = order_parser.parse_args()
        new_order = Orders(**args)
        new_order.save()
        return {'id': new_order.id, 'message': 'Order created successfully'}, 201


class OrderApi(Resource):
    def get(self, order_id):
        return Orders.query.get_or_404(order_id).serialize()

    def delete(self, order_id):
        order = Orders.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully'}
