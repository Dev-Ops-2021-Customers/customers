"""
Customers Service

This service will create, add, update, list, read, and delete customer profiles.
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flasgger import Swagger
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

# Configure Swagger before initilaizing it
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Customer Demo REST API Service",
            "description": "This is a sample Customer server.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

# Initialize Swagger after configuring it
Swagger(app)

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

######################################################################
# G E T  I N D E X
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    # return (
    #     jsonify(
    #         name="Customers Demo REST API Service",
    #         version="1.0",
    #     ),
    #     status.HTTP_200_OK
    # )
    return app.send_static_file('index.html')

######################################################################
# C R E A T E  A  C U S T O M E R
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    ---
    tags:
      - Customers
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: data
          required:
            - name
            - address
            - phone_number
            - email
            - credit_card
            - activate
          properties:  
            name:
                type: string
                description: the customers's name
            address:
                type: string
                description: the address of customer (e.g., 55 Washington Way)
            phone_number:
                type: string
                description: the phone number of customer (e.g., 555-156-1557)          
            email:
                type: string
                description: the email of customer (e.g., swagger@test.com)
            credit_card:
                type: string
                description: the credit card of customer (e.g., VISA)
            active:
                type: string
                description: the status of customer (e.g., active)
    responses:
      201:
        description: Customer created
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Bad Request (the posted data was not valid)
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers", customer_id=customer.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# R E T R I E V E  A  C U S T O M E R
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    ---
    tags:
      - Customers
    produces:
      - application/json
    parameters:
      - name: customer_id
        in: path
        description: ID of customer to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Customer returned
        schema:
          $ref: '#/definitions/Customer'
      404:
        description: Customer not found
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# D E L E T E  A  C U S T O M E R
######################################################################

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer
    This endpoint will delete a Customer based the id specified in the path
     ---
    tags:
      - Customers
    description: Deletes a Customer from the database
    parameters:
      - name: customer_id
        in: path
        description: ID of customer to delete
        type: integer
        required: true
    responses:
      204:
        description: Customer deleted
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# L I S T  A L L  C U S T O M E R S
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """ Returns all of the Customers 
    This endpoint will return all Customers unless a query parameter is specified
    ---
    tags:
      - Customers
    description: The Customers endpoint allows you to query Customers by name
    parameters:
      - name: name
        in: query
        description: the name of Customer you are looking for
        required: false
        type: string
    definitions:
      Customer:
        type: object
        properties:
          customer_id:
            type: integer
            description: unique id assigned internally by service
          name:
            type: string
            description: the customers's name
          address:
            type: string
            description: the address of customer (e.g., 55 Washington Way)
          phone_number:
            type: string
            description: the phone number of customer (e.g., 555-156-1557)          
          email:
            type: string
            description: the email of customer (e.g., swagger@test.com)
          credit_card:
            type: string
            description: the credit card of customer (e.g., VISA)
          active:
            type: string
            description: the status of customer (e.g., active)

    responses:
      200:
        description: An array of Customers
        schema:
          type: array
          items:
            schema:
              $ref: '#/definitions/Customer'
    """
    app.logger.info("Request for customer list")
    customers = []
    name = request.args.get("name")
    if name:
        customers = Customer.find_by_name(name)
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customers
    This endpoint will update a Customer based the body that is posted
    ---
    tags:
      - Customers
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: customer_id
        in: path
        description: ID of customer to update
        type: integer
        required: true
      - in: body
        name: body
        schema:  
          required:
            - name
            - address
            - phone_number
            - email
            - credit_card
          properties:
            name:
                type: string
                description: the customers's name
            address:
                type: string
                description: the address of customer (e.g., 55 Washington Way)
            phone_number:
                type: string
                description: the phone number of customer (e.g., 555-156-1557)          
            email:
                type: string
                description: the email of customer (e.g., swagger@test.com)
            credit_card:
                type: string
                description: the credit card of customer (e.g., VISA)
    responses:
      200:
        description: Customer Updated
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Bad Request (the posted data was not valid)
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DEACTIVATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/deactivate", methods=["PUT"])
def deactivate(customer_id):
    """
    Deactivate a Customer
    This endpoint will deactivate a Customer
    ---
    tags:
      - Customers
    description: Deactivates a Customer
    parameters:
      - name: customer_id
        in: path
        description: ID of customer to deactivate
        type: integer
        required: true
    responses:
      200:
        description: Customer Deactivated
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Bad Request (the posted data was not valid)
    """
    app.logger.info('Request to deactivate customer with id: %s', customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        app.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found".format(customer_id))
    customer.user_id = customer_id
    customer.active = False
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# ACTIVATE A CUSTOMER
######################################################################

@app.route("/customers/<int:customer_id>/activate", methods=["PUT"])
def activate(customer_id):
    """
    Activate a Customer
    This endpoint will activate a Customer
    ---
    tags:
      - Customers
    description: Activates a Customer
    parameters:
      - name: customer_id
        in: path
        description: ID of customer to activate
        type: integer
        required: true
    responses:
      200:
        description: Customer Activated
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Bad Request (the posted data was not valid)
    """
    app.logger.info('Request to activate customer with id: %s', customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        app.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found".format(customer_id))
    customer.customer_id = customer_id
    customer.active = True
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Customer.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))