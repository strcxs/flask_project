from flask import Blueprint
from app.utils.response import error_message


ErrorHandler = Blueprint('ErrorHandler', __name__)

@ErrorHandler.app_errorhandler(Exception)
def handle_exception(e):
    return error_message(str(e).split()[0], str(e))