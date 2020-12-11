""" Sample Chalice "hello world" application """
import json
from chalice import Chalice, Response
from jsonschema import validate, ValidationError
from chalicelib import REG_SCHEMA, STATUS_SCHEMA, idemia_service

with open(".chalice/config.json") as config_file:
    CONFIG = json.load(config_file)

if "app_name" not in CONFIG:
    raise KeyError("No 'app_name' configured in app/.chalice/config.json")

APP_NAME = CONFIG.get("app_name")

# Chalice currently requires app.py to have 'app' (lowercase) available
app = Chalice(app_name=APP_NAME)


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
    except ValidationError as e:
        return Response(
            body={"error": str(e)},
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
    except Exception as e:
        return Response(
            body={"error": str(e)},
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
    except KeyError as e:
        return Response(
            body={"error": str(e)},
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
    except Exception as e:
        return Response(
            body={"error": str(e)},
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
    except KeyError as e:
        return Response(
            body={"error": str(e)},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # proxy request to Idemia API
    try:
        idemia_service.locations(zip)
        return Response(
            body={"status": "No Status Available."},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        return Response(
            body={"error": str(e)},
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
        validate(data, STATUS_SCHEMA)
    except (KeyError, ValidationError) as e:
        return Response(
            body={"error": str(e)},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # proxy request to Idemia API
    try:
        idemia_service.status_update(ueid, data)
        return Response(
            body={}, status_code=204, headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return Response(
            body={"error": str(e)},
            status_code=503,
            headers={"Content-Type": "application/json"},
        )
