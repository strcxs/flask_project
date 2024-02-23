from flask import Blueprint

sign_up_bp = Blueprint("sign_up", __name__, url_prefix="/sign-up")
sign_in_bp = Blueprint("sign_in", __name__, url_prefix="/sign-in")
from . import auth

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")
shipping_price_bp = Blueprint("shipping_price", __name__, url_prefix="/shipping_price")
from . import cart

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")
from . import category

home_bp = Blueprint("home", __name__, url_prefix="/home")
from . import home

order_bp = Blueprint("order", __name__, url_prefix="/order")
orders_bp = Blueprint("orders", __name__, url_prefix="/orders")
from . import order

products_bp = Blueprint("products", __name__, url_prefix="/products")
from . import product

universal_bp = Blueprint("universal", __name__, url_prefix="/image")
from . import universal

user_bp = Blueprint("user", __name__, url_prefix="/user")
sales_bp = Blueprint("sales", __name__, url_prefix="/sales")
from . import user