from datetime import datetime, timezone

import pytest
from app import create_app
from app.extensions import db
from app.models import Cars


@pytest.fixture(scope="session")
def test_app():
    app = create_app(config='config.TestingConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


# @pytest.fixture
# def sample_car(test_app):
#     with test_app.app_context():
#
#         car = Cars(
#             brand='Toyota',
#             model='Corolla',
#             year=2020,
#             car_type='Sedan',
#             body_type='Sedan',
#             traction='Front-wheel drive',
#             color='Red',
#             transmission='Automatic',
#             price_per_day=50.0,
#             location='Edmonton, AB',
#             available=True,
#             created_at=datetime.now(timezone.utc),
#             updated_at=datetime.now(timezone.utc),
#         )
#
#         car.save()
#         return car


