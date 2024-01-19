from http import HTTPStatus
from quart import Blueprint, current_app as app
from quart_schema import validate_request, validate_querystring

from app.settings import BASE_ROUTE, SERVICE_NAME
from app.utils import send_api_response

bp = Blueprint(SERVICE_NAME, __name__, url_prefix=BASE_ROUTE)
LOGGER_KEY = "app.routes"


@bp.route("/public/health", methods=["GET"])
async def health_check():
    """
    health api of weather service to check if service is working fine or not.
    """
    return {"message": "OK"}


