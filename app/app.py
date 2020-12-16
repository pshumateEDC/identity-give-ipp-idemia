""" Idemia Microservice Lambda Chalice Functions """
import re
from uuid import UUID
from http import HTTPStatus
from chalice import Chalice, Response
from jsonschema import validate, ValidationError
from chalicelib import REG_SCHEMA, STATUS_SCHEMA, idemia_service

app = Chalice(app_name="ipp-idemia")


@app.route("/enrollment", methods=["POST"])
def enrollment_register():
    """
    Pre-Enrollment Registration Function. Receives an enrollment applicant and registers said
    applicant with the Idemia IPP service.
    """
    data = app.current_request.json_body

    # validate request body
    try:
        validate(data, REG_SCHEMA)
    except ValidationError:
        return response(HTTPStatus.BAD_REQUEST, {"error": "Invalid Request Body"})

    # validate UUID
    try:
        UUID(data.get("uuid"))
    except ValueError:
        return response(HTTPStatus.BAD_REQUEST, {"error": "Invalid UUID"})

    # proxy request to Idemia API
    try:
        idemia_service.register(data)
    except NotImplementedError as ni_error:
        return response(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(ni_error)})

    return response(HTTPStatus.CREATED, {"status": "User Registered"})


@app.route("/locations", methods=["GET"])
def locations_get():
    """
    Locations Function. Receives a zip code and returns a list of local IPP locations.
    """
    param = app.current_request.query_params

    # check for existing query parameter
    if param is None:
        return response(HTTPStatus.BAD_REQUEST, {"error": "Query parameters not found"})

    # validate query parameter
    if "zip" not in param:
        return response(
            HTTPStatus.BAD_REQUEST, {"error": "'zip' not found as a query parameter"}
        )
    zipcode = param["zip"]

    # validate zip code with regex that matches 5 digit US Zip Codes or Zip + 4
    if not re.fullmatch(r"^\d{5}(-\d{4})?$", zipcode):
        return response(
            HTTPStatus.BAD_REQUEST, {"error": f"Invalid Zip code format: {zipcode}"}
        )

    # proxy request to Idemia API
    try:
        idemia_service.locations(zipcode)
    except NotImplementedError as ni_error:
        return response(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(ni_error)})

    return response(HTTPStatus.OK, {"locations": []})


@app.route("/enrollment", methods=["GET"])
def status_get():
    """
    Fetch Status Function. Returns a user's status based on a given query parameter UUID.
    """
    param = app.current_request.query_params

    # check for existing query parameter
    if param is None:
        return response(HTTPStatus.BAD_REQUEST, {"error": "Query parameters not found"})

    # validate query parameter
    if "uuid" not in param:
        return response(
            HTTPStatus.BAD_REQUEST, {"error": "'uuid' not found as a query parameter"}
        )
    uuid = param.get("uuid")

    # validate UUID
    try:
        UUID(uuid)
    except ValueError:
        return response(
            HTTPStatus.BAD_REQUEST, {"error": f"Invalid UUID format: {uuid}"}
        )

    # proxy request to Idemia API
    try:
        idemia_service.status_get(uuid)
    except NotImplementedError as ni_error:
        return response(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(ni_error)})

    return response(HTTPStatus.OK, {"status": "No Status Available."})


@app.route("/enrollment", methods=["PUT"])
def status_put():
    """
    Update Status Function. Receives a UEID as a query parameter and a status in the request body.
    Updates the user's status corresponding to the UEID to the new status provided.
    """
    data = app.current_request.json_body
    param = app.current_request.query_params

    # check for existing query parameter
    if param is None:
        return response(HTTPStatus.BAD_REQUEST, {"error": "Query parameters not found"})

    # validate query parameter and request body
    if "ueid" not in param:
        return response(
            HTTPStatus.BAD_REQUEST, {"error": "'ueid' not found as a query parameter"}
        )
    ueid = param.get("ueid")

    # validate UEID
    # no knowledge on exact limitations except for 10 character string with A-Z and 0-9 permitted
    if not re.search(r"[A-Z0-9]{10}", ueid.strip()):
        return response(
            HTTPStatus.BAD_REQUEST, {"error": f"Invalid UEID format: {ueid}"}
        )

    # validate request body
    try:
        validate(data, STATUS_SCHEMA)
    except ValidationError:
        return response(HTTPStatus.BAD_REQUEST, {"error": "Invalid Request Body"})

    # proxy request to Idemia API
    try:
        idemia_service.status_update(ueid, data)
    except NotImplementedError as ni_error:
        return response(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(ni_error)})

    return response(HTTPStatus.NO_CONTENT, {})


def response(status_code, body):
    """ Helper function to eliminate duplicate code when generating an HTTP response """
    return Response(
        body=body,
        status_code=status_code,
        headers={"Content-Type": "application/json"},
    )
