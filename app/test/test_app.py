""" Tests for app.py """
import json
from http import HTTPStatus
from chalice.test import Client
from pytest import fixture
from app import app


@fixture(name="client_fixture")
def test_client():
    """ Test fixture for creating a chalice Client """
    with Client(app) as client:
        yield client


# Enrollment registration tests
def test_enrollment_register_function_bad_request_empty_body(client_fixture):
    """ Ensure the enrollment function returns a 400 Bad Request on bad/empty requests """
    # empty request
    response = client_fixture.http.post("/enrollment")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_enrollment_register_function_bad_request_invalid_body(client_fixture):
    """ Ensure the enrollment function returns a 400 Bad Request on bad/empty requests """
    # invalid body
    reg_invalid = {"uuid": 0, "firstName": 0, "lastName": 0, "emailAddress": 0}
    response = client_fixture.http.request(
        method="POST",
        path="/enrollment",
        headers={"Content-Type": "application/json"},
        body=json.dumps(reg_invalid),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_enrollment_register_function_bad_request_invalid_uuid(client_fixture):
    """ Ensure the enrollment function returns a 400 Bad Request on bad/empty requests """
    # invalid uuid
    reg_invalid = {
        "uuid": "c7b82090-172f-11eb-adc1-",
        "firstName": "Peter",
        "lastName": "Shumate",
        "emailAddress": "test@email.com",
    }
    response = client_fixture.http.request(
        method="POST",
        path="/enrollment",
        headers={"Content-Type": "application/json"},
        body=json.dumps(reg_invalid),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_enrollment_register_not_implemented(client_fixture):
    """ Ensure the enrollment function returns a 503 Service Unavailable on succesful requests """
    reg_valid = {
        "uuid": "c7b82090-172f-11eb-adc1-0242ac120002",
        "firstName": "Peter",
        "lastName": "Shumate",
        "emailAddress": "test@email.com",
    }
    response = client_fixture.http.request(
        method="POST",
        path="/enrollment",
        headers={"Content-Type": "application/json"},
        body=json.dumps(reg_valid),
    )
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE


# Location fetch tests
def test_locations_get_function_bad_request_no_parameter(client_fixture):
    """ Ensure the location function returns a 400 Bad Request on bad/empty requests """
    # empty request
    response = client_fixture.http.get("/locations")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_locations_get_function_bad_request_bad_parameter(client_fixture):
    """ Ensure the location function returns a 400 Bad Request on bad/empty requests """
    # invalid zipcode (integers)
    response = client_fixture.http.get("/locations?zip=223122")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_locations_get_function_bad_request_bad_parameter_string(client_fixture):
    """ Ensure the location function returns a 400 Bad Request on bad/empty requests """
    # invalid zipcode (characters)
    response = client_fixture.http.get("/locations?zip=asdas")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_locations_not_implemented(client_fixture):
    """ Ensure the location function returns a 503 Service Unavailable on succesful requests """
    response = client_fixture.http.get("/locations?zip=22312")
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE


# Status fetch tests
def test_status_get_function_bad_request_empty(client_fixture):
    """ Ensure the get status function returns a 400 Bad Request on bad/empty requests """
    # empty request
    response = client_fixture.http.get("/enrollment")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_status_get_function_bad_request_invalid(client_fixture):
    """ Ensure the get status function returns a 400 Bad Request on bad/empty requests """
    # invalid uuid
    response = client_fixture.http.get("/enrollment?uuid=4c4605ec-3662-11eb-adc1-")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_status_get_function_not_implemented(client_fixture):
    """ Ensure the get status function returns a 503 Service Unavailable on succesful requests """
    response = client_fixture.http.get(
        "/enrollment?uuid=4c4605ec-3662-11eb-adc1-0242ac120002"
    )
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE


# Status update tests
def test_status_put_function_bad_request_no_parameter_no_body(client_fixture):
    """ Ensure the update function returns a 400 Bad Request on bad/empty requests """
    # empty request
    response = client_fixture.http.put("/enrollment")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_status_put_function_bad_request_invalid_parameter_no_body(client_fixture):
    """ Ensure the update function returns a 400 Bad Request on bad/empty requests """
    # invalid ueid and no status body
    response = client_fixture.http.put("/enrollment?ueid=UZTX12BH1")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_status_put_function_bad_request_valid_parameter_invalid_body(client_fixture):
    """ Ensure the update function returns a 400 Bad Request on bad/empty requests """
    # valid ueid and invalid body
    status = {"ippstatus": 0}
    response = client_fixture.http.request(
        method="PUT",
        path="/enrollment?ueid=UZTX12BH1K",
        headers={"Content-Type": "application/json"},
        body=json.dumps(status),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_status_put_function_not_implemented(client_fixture):
    """ Ensure the update function returns a 503 Service Unavailable on succesful requests """
    status = {"ippstatus": "User completed and passed IPP event."}
    response = client_fixture.http.request(
        method="PUT",
        path="/enrollment?ueid=UZTX12BH1K",
        headers={"Content-Type": "application/json"},
        body=json.dumps(status),
    )
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
