import json
import traceback
from pydantic.error_wrappers import ValidationError
from quart import Quart, g, request
from quart_schema import QuartSchema, RequestSchemaValidationError

from . import settings
from data.database import Postgres
from data.redis import RedisCache
from app.routes import bp
from app.utils import (
    get_logger,
    VerifyEnv,
    get_request_id,
    send_api_response,
    MissingEnvConfigsException,
)

# initializing app
app = Quart(__name__)
app.config.from_object(settings)
QuartSchema(
    app,
    redoc_ui_path=f"{settings.BASE_ROUTE}/redocs", # http://localhost:9200/redocs
    swagger_ui_path=f"{settings.BASE_ROUTE}/docs", # http://localhost:9200/docs
    openapi_path=f"{settings.BASE_ROUTE}/openapi.json", # http://localhost:9200/openapi.json
    version="1.0.0",
    title="Weather Service API Documentation",
)

# stating required services before starting the app
@app.before_serving
async def _init():
    init_logger()
    app.logger.info("SERVER STARTING...")
    app.logger.info("logger initialized")
    verify_envs = VerifyEnv().verify()
    if verify_envs[0] is True:
        app.logger.info("config variables verified")
    else:
        app.logger.error("config NOT VERIFIED %s", str(verify_envs[1]))
        error = f"unable to verify these config {str(verify_envs[1])}"
        raise MissingEnvConfigsException(message=error)

    await _init_redis()
    app.logger.info("redis initialized")

    await _init_db()
    app.logger.info("all dbs initialized")

    await _setup_db()
    app.logger.info("DB setup completed")

    _register_blueprints()


@app.after_serving
async def _terminate():
    await app.db.close()
    await app.redis.close()


@app.before_request
def _before_request():
    g.request_id = get_request_id()


# initializing logger
def init_logger():
    get_logger()
    app.logger.removeHandler(app.logger.handlers[0])
    return

# initializing DB
async def _init_db():
    db_conf = app.config.get("DB_CONFIGS")
    db_kwargs = {
        "database": db_conf["NAME"],
        "host": db_conf["HOST"],
        "port": db_conf["PORT"],
        "user": db_conf["USER"],
        "password": db_conf["PASSWORD"],
    }
    app.db = Postgres(**db_kwargs)
    await app.db.connect()
    app.logger.info("weather app db connected")
    return


async def _setup_db():
    # Read and execute SQL commands from the file
    with open("./db_commands.sql", 'r') as file:
        sql_commands = file.read()

    sql_commands = f"BEGIN; {sql_commands} COMMIT;"
    response = await app.db.execute_raw_transaction_query(sql_commands)
    app.logger.info(f"response: {response}")
    return


# initializing redis
async def _init_redis():
    app.redis = RedisCache(app.config.get("APP_NAME") + "_" + app.config.get("ENV"))
    redis_conf = app.config.get("REDIS")
    await app.redis.connect(host=redis_conf["HOST"], port=redis_conf["PORT"])
    return


# registering blueprints
def _register_blueprints():
    app.register_blueprint(bp)
    return


@app.errorhandler(404)
def _route_not_found(exception):
    app.logger.error("%s, route: '%s'", exception, request.url)

    return {"message": "requested route not found"}, 404


@app.errorhandler(405)
def _method_not_allowed(exception):
    app.logger.error("%s, route: '%s'", exception, request.url)

    return {"message": "Method not allowed"}, 405


@app.errorhandler(408)
def _resource_request_timed_out(exception):
    app.logger.error(
        "resource request timed out, traceback: %s",
        traceback.extract_tb(exception.__traceback__),
    )

    return {"message": "resource request timed out"}, 408


@app.errorhandler(Exception)
def _unhandled_exception(exception):
    app.logger.error(
        "server._unhandled_exception: %s, traceback: %s",
        exception,
        traceback.extract_tb(exception.__traceback__),
    )
    return {"message": "something went wrong"}, 500


@app.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error):
    if isinstance((error.validation_error), (ValidationError)):
        error = json.loads(error.validation_error.json())
        if error[0]["type"] == "value_error":
            error = error[0]["msg"]
            return send_api_response(
                message="Invalid Payload Keys",
                data={"errors": [{"error": error}]},
                success=False,
                status_code=400,
            )
        else:
            if error and error[0].get("loc") and isinstance(error[0].get("loc"), list):
                message = f"{error[0]['msg']}:-{error[0]['loc'][-1]}"
            else:
                message = "Invalid Payload Keys"
            return send_api_response(
                message=message,
                data={"errors": [{"error": error[0]["msg"], "key": error[0]["loc"]}]},
                success=False,
                status_code=400,
            )

    elif str(error.validation_error) == "type object argument after ** must be a mapping, not NoneType":
        return send_api_response(message="Empty request body", status_code=400)
    else:
        error = str(error.validation_error)
        return send_api_response(
            message=str(error.replace("__init__() ", "")),
            success=False,
            status_code=400,
        )
