""" Idemia Microservice Lambda Chalice Functions """
import re
from uuid import UUID
from http import HTTPStatus
from chalice import Chalice, Response
from jsonschema import validate, ValidationError
from chalicelib import REG_SCHEMA, STATUS_SCHEMA, idemia_service

app = Chalice(app_name="ipp-idemia")


class BadRequestErrorResponse(Response):
    """ Response sub class for Bad Request status codes """

    def __init__(self, body: dict):
        super().__init__(body=body, status_code=HTTPStatus.BAD_REQUEST)


class UnavailableErrorResponse(Response):
    """ Response sub class for Service Unavailable status codes """

    def __init__(self, body: dict):
        super().__init__(body=body, status_code=HTTPStatus.SERVICE_UNAVAILABLE)


class NoContentResponse(Response):
    """ Response sub class for No Content status codes """

    def __init__(self):
        super().__init__(body={}, status_code=HTTPStatus.NO_CONTENT)


class OkResponse(Response):
    """ Response sub class for OK status codes """

    def __init__(self, body: dict):
        super().__init__(body=body, status_code=HTTPStatus.OK)


class UnsupportedResponse(Response):
    """ Response sub class for Unsupported Media Type status codes """

    def __init__(self, body: dict):
        super().__init__(body=body, status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)


@app.route("/enrollment", methods=["POST"])
def enrollment_register():
    """
    Pre-Enrollment Registration Function. Receives an enrollment applicant and registers said
    applicant with the Idemia IPP service.
    """
    data = app.current_request.json_body

    if data is None:
        return UnsupportedResponse(
            {"error": "Request body is not in application/json format"}
        )

    # validate request body
    try:
        validate(data, REG_SCHEMA)
    except ValidationError:
        return BadRequestErrorResponse({"error": "Invalid Request Body"})

    # validate UUID
    try:
        UUID(data.get("uuid"))
    except ValueError:
        return BadRequestErrorResponse({"error": "Invalid UUID"})

    # proxy request to Idemia API
    try:
        idemia_service.register(data)
    except NotImplementedError as ni_error:
        return UnavailableErrorResponse({"error": str(ni_error)})

    return OkResponse({"status": "User Registered"})


@app.route("/locations", methods=["GET"])
def locations_get():
    """
    Locations Function. Receives a zip code and returns a list of local IPP locations.
    """
    param = app.current_request.query_params

    # check for existing query parameter
    if param is None:
        return BadRequestErrorResponse({"error": "Query parameters not found"})

    # validate query parameter
    if "zip" not in param:
        return BadRequestErrorResponse(
            {"error": "'zip' not found as a query parameter"}
        )
    zipcode = param["zip"]

    # validate zip code with regex that matches 5 digit US Zip Codes or Zip + 4
    if not re.fullmatch(r"^\d{5}(-\d{4})?$", zipcode):
        return BadRequestErrorResponse({"error": f"Invalid Zip code format: {zipcode}"})

    # proxy request to Idemia API
    try:
        idemia_service.locations(zipcode)
    except NotImplementedError as ni_error:
        return UnavailableErrorResponse({"error": str(ni_error)})

    return OkResponse({"locations": []})


@app.route("/enrollment", methods=["GET"])
def status_get():
    """
    Fetch Status Function. Returns a user's status based on a given query parameter UUID.
    """
    param = app.current_request.query_params

    # check for existing query parameter
    if param is None:
        return BadRequestErrorResponse({"error": "Query parameters not found"})

    # validate query parameter
    if "uuid" not in param:
        return BadRequestErrorResponse(
            {"error": "'uuid' not found as a query parameter"}
        )
    uuid = param.get("uuid")

    # validate UUID
    try:
        UUID(uuid)
    except ValueError:
        return BadRequestErrorResponse({"error": f"Invalid UUID format: {uuid}"})

    # proxy request to Idemia API
    try:
        idemia_service.status_get(uuid)
    except NotImplementedError as ni_error:
        return UnavailableErrorResponse({"error": str(ni_error)})

    return OkResponse({"status": "No Status Available."})


@app.route("/enrollment", methods=["PUT"])
def status_put():
    """
    Update Status Function. Receives a UEID as a query parameter and a status in the request body.
    Updates the user's status corresponding to the UEID to the new status provided.
    """
    data = app.current_request.json_body
    param = app.current_request.query_params

    if data is None:
        return UnsupportedResponse(
            {"error": "Request body is not in application/json format"}
        )

    # check for existing query parameter
    if param is None:
        return BadRequestErrorResponse({"error": "Query parameters not found"})

    # validate query parameter and request body
    if "ueid" not in param:
        return BadRequestErrorResponse(
            {"error": "'ueid' not found as a query parameter"}
        )
    ueid = param.get("ueid")

    # validate UEID
    # no knowledge on exact limitations except for 10 character string with A-Z and 0-9 permitted
    if not re.search(r"[A-Z0-9]{10}", ueid.strip()):
        return BadRequestErrorResponse({"error": f"Invalid UEID format: {ueid}"})

    # validate request body
    try:
        validate(data, STATUS_SCHEMA)
    except ValidationError:
        return BadRequestErrorResponse({"error": "Invalid Request Body"})

    # proxy request to Idemia API
    try:
        idemia_service.status_update(ueid, data)
    except NotImplementedError as ni_error:
        return UnavailableErrorResponse({"error": str(ni_error)})

    return NoContentResponse
