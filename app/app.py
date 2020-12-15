""" Idemia Microservice Lambda Chalice Functions """
import re
from uuid import UUID
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
        UUID(data.get("uuid"))
    except (ValidationError, ValueError) as validation_error:
        return Response(
            body={"error": str(validation_error)},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # proxy request to Idemia API
    try:
        idemia_service.register(data)
        return Response(
            body={"status": "User registered."},
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except NotImplementedError as ni_error:
        return Response(
            body={"error": str(ni_error)},
            status_code=503,
            headers={"Content-Type": "application/json"},
        )


@app.route("/locations", methods=["GET"])
def locations_get():
    """
    Locations Function. Receives a zip code and returns a list of local IPP locations.
    """
    param = app.current_request.query_params

    # validate query parameter
    try:
        zipcode = param["zip"]
        if not re.search(r"^\d{5}(?:[-\s]\d{4})?$", zipcode.strip()):
            raise ValueError("The string %s is NOT a valid ZipCode" % zipcode)
    except (KeyError, TypeError, ValueError) as error:
        return Response(
            body={"error": str(error)},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # proxy request to Idemia API
    try:
        idemia_service.locations(zipcode)
        return Response(
            body={"locations": []},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except NotImplementedError as ni_error:
        return Response(
            body={"error": str(ni_error)},
            status_code=503,
            headers={"Content-Type": "application/json"},
        )


@app.route("/enrollment", methods=["GET"])
def status_get():
    """
    Fetch Status Function. Returns a user's status based on a given query parameter UUID.
    """
    param = app.current_request.query_params

    # validate query parameter
    try:
        uuid = param["uuid"]
        UUID(uuid)
    except (KeyError, TypeError, ValueError) as error:
        return Response(
            body={"error": str(error)},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # proxy request to Idemia API
    try:
        idemia_service.status_get(uuid)
        return Response(
            body={"status": "No Status Available."},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except NotImplementedError as ni_error:
        return Response(
            body={"error": str(ni_error)},
            status_code=503,
            headers={"Content-Type": "application/json"},
        )


@app.route("/enrollment", methods=["PUT"])
def status_put():
    """
    Update Status Function. Receives a UEID as a query parameter and a status in the request body.
    Updates the user's status corresponding to the UEID to the new status provided.
    """
    data = app.current_request.json_body
    param = app.current_request.query_params

    # validate query parameter and request body
    try:
        ueid = param["ueid"]
        if not re.search(r"[A-Z0-9]{10}", ueid.strip()):
            raise ValueError("The string %s is NOT a valid UEID" % ueid)
        validate(data, STATUS_SCHEMA)
    except (KeyError, ValidationError, TypeError, ValueError) as error:
        return Response(
            body={"error": str(error)},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # proxy request to Idemia API
    try:
        idemia_service.status_update(ueid, data)
        return Response(
            body={}, status_code=204, headers={"Content-Type": "application/json"}
        )
    except NotImplementedError as ni_error:
        return Response(
            body={"error": str(ni_error)},
            status_code=503,
            headers={"Content-Type": "application/json"},
        )
