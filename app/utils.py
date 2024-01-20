import logging
import asyncio
from http import HTTPStatus
from uuid import uuid4
from functools import wraps
from typing import Optional, Any
from quart import current_app as app, g, request

from .settings import LOG_LEVEL, SERVICE_NAME


# Dictionary to track request timestamps for rate limiting
request_timestamps = {}
def rate_limit(limit, interval):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ip_address = request.remote_addr
            endpoint = request.path

            if ip_address not in request_timestamps:
                request_timestamps[ip_address] = {}

            if endpoint not in request_timestamps[ip_address]:
                request_timestamps[ip_address][endpoint] = []

            current_time = asyncio.get_event_loop().time()

            # Remove timestamps older than the interval
            request_timestamps[ip_address][endpoint] = [
                timestamp for timestamp in request_timestamps[ip_address][endpoint] if
                current_time - timestamp < interval
            ]

            if len(request_timestamps[ip_address][endpoint]) >= limit:
                return send_api_response(
                    "Rate limit exceeded. Try again later.",
                    False,
                    status_code=HTTPStatus.TOO_MANY_REQUESTS.value
                )

            # Record the current timestamp
            request_timestamps[ip_address][endpoint].append(current_time)
            return await func(*args, **kwargs)
        return wrapper
    return decorator



def get_logger():
    extra = {"app_name": SERVICE_NAME}
    format = "[%(asctime)s] %(levelname)s in %(module)s : %(message)s"
    logging.basicConfig(level=LOG_LEVEL, format=format)
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, extra)
    return


class MissingEnvConfigsException(Exception):
    def __init__(self, message):
        self.errorCode = 501
        self.errorMessage = message
        return


class VerifyEnv:
    def __init__(self):
        self.used_configs = [
            "ENV",
            "REDIS",
            "APP_NAME",
            "LOG_LEVEL",
            "BASE_ROUTE",
            "DB_CONFIGS",
        ]

    def verify(self):
        unverified_envs = []
        success = True
        for i in self.used_configs:
            env_var = app.config.get(i, None)
            if env_var is None or "":
                unverified_envs.append(i)
                success = False

        return success, unverified_envs


def get_request_id():
    if getattr(g, "request_id", None):
        return str(g.request_id)

    headers = request.headers
    request_id = headers.get("X-Request-Id")
    if not request_id:
        request_id = str(uuid4())

    g.request_id = request_id
    return request_id


def send_api_response(
    message: str,
    success: bool = True,
    data: Optional[Any] = None,
    status_code: Optional[int] = None,
):
    response = {"message": message, "success": success}
    if data != None:
        response["data"] = data

    app.logger.debug(f"send_api_response.response:{response}")
    return (response, status_code) if status_code else (response, 200 if success else 500)
