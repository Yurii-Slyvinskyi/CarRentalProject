from flask_restful import Api
from .cars_api import CarsApiList, CarApi
from .orders_api import OrdersApiList, OrderApi
from .users_api import UsersApiList, UserApi

api = Api()

def init_api(app):
    api.init_app(app)

    api.add_resource(CarsApiList, '/api/cars/', endpoint='carsapilist')
    api.add_resource(CarApi, '/api/cars/<int:car_id>/', endpoint='carapi')

    api.add_resource(OrdersApiList, '/api/orders/', endpoint='ordersapilist')
    api.add_resource(OrderApi, '/api/orders/<int:order_id>/', endpoint='orderapi')

    api.add_resource(UsersApiList, '/api/users/', endpoint='usersapilist')
    api.add_resource(UserApi, '/api/users/<int:user_id>/', endpoint='userapi')

