from chalice import Chalice, Response
from jsonschema import validate, ValidationError
from chalicelib import REG_SCHEMA, STATUS_SCHEMA, idemia_service

app = Chalice(app_name="give_idemia_microservice")


@app.route("/enrollment", methods=["POST"])
def enrollment_register():
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
    param = app.current_request.query_params

    # validate query parameter
    try:
        zip = param["zip"]
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
