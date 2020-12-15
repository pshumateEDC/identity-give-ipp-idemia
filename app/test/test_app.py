""" Tests for app.py """
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
def test_enrollment_register_function_bad_request(client_fixture):
    """ Ensure the enrollment function returns a 400 Bad Request on bad/empty requests """
    response = client_fixture.http.post("/enrollment")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    reg_invalid = {"uuid": 0, "firstName": 0, "lastName": 0, "emailAddress": 0}
    response = client_fixture.http.post("/enrollment", body=reg_invalid)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_enrollment_register_not_implemented(client_fixture):
    """ Ensure the enrollment function returns a 503 Service Unavailable on succesful requests """
    reg_valid = '{ "uuid": "c7b82090-172f-11eb-adc1-0242ac120002", "firstName": "Peter", "lastName": "Shumate", "emailAddress": "test@email.com" }'
    response = client_fixture.http.post("/enrollment", body=reg_valid)
    print(response.body)
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE


# Location fetch tests
def test_locations_get_function(client_fixture):
    """ Ensure the location function returns a 400 Bad Request on bad/empty requests """
    response = client_fixture.http.get("/locations")
    assert response.status_code == HTTPStatus.BAD_REQUEST


# Status fetch tests
def test_status_get_function(client_fixture):
    """ Ensure the get status function returns a 400 Bad Request on bad/empty requests """
    response = client_fixture.http.get("/enrollment")
    assert response.status_code == HTTPStatus.BAD_REQUEST


# Status update tests
def test_status_put_function(client_fixture):
    """ Ensure the get update function returns a 400 Bad Request on bad/empty requests """
    response = client_fixture.http.put("/enrollment")
    assert response.status_code == HTTPStatus.BAD_REQUEST
