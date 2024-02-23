from flask import Flask
from flask_cors import CORS
from app.utils.handle_error import ErrorHandler
from app.data import dummy
from app.models import get_engine
import app.models as models
import app.routes as routes


def create_app():
    app = Flask(__name__)
    engine = get_engine()
    blueprints = [
        ErrorHandler,
        routes.universal_bp,
        routes.home_bp,
        routes.sign_up_bp,
        routes.sign_in_bp,
        routes.products_bp,
        routes.categories_bp,
        routes.cart_bp,
        routes.shipping_price_bp,
        routes.user_bp,
        routes.order_bp,
        routes.orders_bp,
        routes.sales_bp,
    ]

    # Register models to engine/database
    models.Base.metadata.create_all(bind=engine)

    # Register blueprints to flask
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # To allow CORS for all domains on all routes
    CORS(app)

    return app


create_app()
dummy()