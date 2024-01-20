from http import HTTPStatus
from quart import Blueprint, current_app as app
from quart_schema import validate_request, validate_querystring

from app.location_manager.service import locationManager
from app.weather_manager.service import weatherManager
from app.settings import BASE_ROUTE, SERVICE_NAME
from app.utils import send_api_response
from app.validator import (
    AddLocation,
    PutLocation,
    GetHistory,
)

bp = Blueprint(SERVICE_NAME, __name__, url_prefix=BASE_ROUTE)
LOGGER_KEY = "app.location_manager.routes"


@bp.route("/public/health", methods=["GET"])
async def health_check():
    """
    health api of weather service to check if service is working fine or not.
    """
    return {"message": "OK"}


@bp.route("/locations", methods=["GET"])
@bp.route("/locations/<location_id>", methods= ["GET"])
async def get_locations(**kwargs):
    """
    API to get the list of all locations added
    """
    app.logger.info(f"{LOGGER_KEY}.get_locations")
    location_manager = locationManager(kwargs)
    locations_data = await location_manager.fetchLocations()
    if locations_data.get("error"):
        return send_api_response(
            f"user signup failed: {locations_data.get('error')}",
            False,
            status_code=locations_data.get("status_code"),
        )
    
    return send_api_response(
        f"all locations added by user",
        True,
        data= locations_data.get("data"),
        status_code= HTTPStatus.OK.value
    )


@bp.route("/locations", methods=["POST"])
@validate_request(AddLocation)
async def add_locations(data: AddLocation):
    """
    API to add locations
    """
    app.logger.info(f"{LOGGER_KEY}.add_locations")
    payload = data.dict()
    location_manager = locationManager(payload)

    # check if city already exists
    city_details = await location_manager.fetchLocations()
    if city_details.get("error"):
        return send_api_response(
            city_details.get("error"),
            False,
            status_code=city_details.get("status_code")
        )
    
    # return error if city exists
    if city_details.get("data"):
        return send_api_response(
            f"city {payload['city']} already exists",
            False,
            data=city_details.get("data"),
            status_code=HTTPStatus.BAD_REQUEST.value
        )
    
    # add to the Database  
    add_location_response = await location_manager.addLocation()
    if add_location_response.get("error"):
        return send_api_response(
            add_location_response.get("error"),
            False, 
            status_code=add_location_response.get("status_code")
        )

    return send_api_response(
        f"location added successfully",
        True,
        data=add_location_response.get("data"),
        status_code= HTTPStatus.OK.value
    )


@bp.route("/locations/<location_id>", methods=["PUT"])
@validate_request(PutLocation)
async def put_location(data:PutLocation, **kwargs):
    """
    API to PUT the new location in-place of an old location
    """
    app.logger.info(f"{LOGGER_KEY}.put_location")
    data = data.dict()
    payload = {**data, **kwargs}
    location_manager = locationManager(payload)

    # check if location exists for given location id
    locations_data = await location_manager.fetchLocations()
    if locations_data.get("error"):
        return send_api_response(
            f"error in fetching location: {locations_data.get('error')}",
            False,
            status_code=locations_data.get("status_code"),
        )
    
    # if location does not exists return error
    if not locations_data.get("data"):
        return send_api_response(
            f"city with given location_id does not exists",
            False,
            status_code=HTTPStatus.BAD_REQUEST.value
        )
    
    # update location
    put_location_response = await location_manager.putLocation()
    if put_location_response.get("error"):
        return send_api_response(
            f"error in updating the location: {put_location_response.get('error')}",
            False,
            status_code=put_location_response.get("status_code")
        )
    
    return send_api_response(
        f"location updated successfully",
        True,
        data=put_location_response.get('data'),
        status_code= HTTPStatus.OK.value
    )


@bp.route("/locations/<location_id>", methods=["DELETE"])
async def delete_location(**kwargs):
    """
    API to delete the location against the location_id
    """
    app.logger.info(f"{LOGGER_KEY}.delete_location")
    location_manager = locationManager(kwargs)

    # check if location exists for given location id
    locations_data = await location_manager.fetchLocations()
    if locations_data.get("error"):
        return send_api_response(
            f"error in fetching location: {locations_data.get('error')}",
            False,
            status_code=locations_data.get("status_code"),
        )
    
    #  if location does not exists return error
    if not locations_data.get("data"):
        return send_api_response(
            f"city with given location_id does not exists",
            False,
            status_code=HTTPStatus.BAD_REQUEST.value
        )
    
    # delete the location
    delete_location_response = await location_manager.deleteLocation()
    if delete_location_response.get("error"):
        return send_api_response(
            f"error in deleting the location: {delete_location_response.get('error')}",
            False,
            status_code=delete_location_response.get("status_code")
        )
    
    return send_api_response(
        f"location deleted successfully",
        True,
        status_code= HTTPStatus.OK.value
    )


@bp.route("/weather/<location_id>", methods=["GET"])
async def get_forecast(**kwargs):
    """
    get forecast using third api and store the result
    """
    app.logger.info(f"{LOGGER_KEY}.get_forecast")
    weather_manager = weatherManager(kwargs)

    # fetches the current forecast
    forecast_data_response = await weather_manager.getForecast()
    if forecast_data_response.get("error"):
        return send_api_response(
            f"failed to fetch the forecast: {forecast_data_response.get('error')}",
            False,
            status_code=forecast_data_response.get("status_code")
        )
    
    return send_api_response(
        f"forecast fetched",
        True,
        data= forecast_data_response.get("data"),
        status_code=HTTPStatus.OK.value
    )


@bp.route("/history/<location_id>", methods=["GET"])
@validate_querystring(GetHistory)
async def get_history(**kwargs):
    """
    get the history of last 7 or 15 or 30 days
    """
    app.logger.info(f"{LOGGER_KEY}.get_history")
    query_args = kwargs.get("query_args")
    query_args = query_args.dict()
    query_args['location_id'] = kwargs.get("location_id")

    weather_manager = weatherManager(query_args)
    history_data_response = await weather_manager.getHistory()
    if history_data_response.get("error"):
        return send_api_response(
            f"Failed to fetch the history: {history_data_response['error']}",
            False,
            status_code=history_data_response.get("status_code")
        )

    return send_api_response(
        f"history fetched successfully",
        True,
        data = history_data_response['data'],
        status_code=HTTPStatus.OK.value
    )