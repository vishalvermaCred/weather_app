from http import HTTPStatus
from quart import Blueprint, current_app as app
from quart_schema import validate_request, validate_querystring

from app.location_manager.service import locationManager
from app.settings import BASE_ROUTE, SERVICE_NAME
from app.utils import send_api_response
from app.validator import (
    AddLocation,
    PutLocation,
)

bp = Blueprint(SERVICE_NAME, __name__, url_prefix=BASE_ROUTE)
LOGGER_KEY = "app.routes"


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
    locations_data = await location_manager.fetchLocations()
    if locations_data.get("error"):
        return send_api_response(
            f"error in fetching location: {locations_data.get('error')}",
            False,
            status_code=locations_data.get("status_code"),
        )
    
    if not locations_data.get("data"):
        return send_api_response(
            f"city with given location_id does not exists",
            False,
            status_code=HTTPStatus.BAD_REQUEST.value
        )
    
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
    locations_data = await location_manager.fetchLocations()
    if locations_data.get("error"):
        return send_api_response(
            f"error in fetching location: {locations_data.get('error')}",
            False,
            status_code=locations_data.get("status_code"),
        )
    
    if not locations_data.get("data"):
        return send_api_response(
            f"city with given location_id does not exists",
            False,
            status_code=HTTPStatus.BAD_REQUEST.value
        )
    
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