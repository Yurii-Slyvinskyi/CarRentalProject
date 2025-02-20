from flask_restful import Resource, reqparse
from app.extensions import db
from app.models import Users


user_parser = reqparse.RequestParser()

fields = [
    ('name', str, True), ('username', str, True),
    ('email', str, True), ('password', str, True)
]

for field, dtype, required in fields:
    user_parser.add_argument(field, type=dtype, required=required, help=f"{field.capitalize()} is required")


class UsersApiList(Resource):
    def get(self):
        return [user.serialize() for user in Users.query.all()]

    def post(self):
        args = user_parser.parse_args()
        new_user = Users(**args)
        new_user.set_password(args['password'])
        new_user.save()
        return {'id': new_user.id, 'message': 'User created successfully'}, 201


class UserApi(Resource):
    def get(self, user_id):
        return Users.query.get_or_404(user_id).serialize()

    def delete(self, user_id):
        user = Users.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

    def put(self, user_id):
        args = user_parser.parse_args()
        user = Users.query.get_or_404(user_id)
        user.update_from_args(args)
        db.session.commit()
        return {'message': 'User updated successfully'}
