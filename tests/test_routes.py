"""
TestCustomerModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db, Customer
from service.routes import app, init_db

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_customer(self, customer_name="Alex"):
        """ Create a new Customer """
        test_customer = Customer(
            name=customer_name,
            address="Washington Square Park",
            phone_number="555-555-1234",
            email="alex@jr.com",
            credit_card="VISA"
        )
        return test_customer 

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_create_customer(self):
        """ Create a new Customer """
        test_customer = self._create_customer("Alex")
        logging.debug(test_customer)
        resp = self.app.post(
            "/customers", json=test_customer.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Customers Demo REST API Service")

    def test_get_customer_list(self):
        """ Get a list of Customers """
        customer = self._create_customer("Alex")
        customer.create()
        customer = self._create_customer("Sally")
        customer.create()
        customer = self._create_customer("John")
        customer.create()
        resp = self.app.get("/customers")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 3)

    def test_update_customer(self):
        """ Update an existing Customer """
        # create a customer to update
        test_customer = self._create_customer("Alex")
        
        resp = self.app.post(
            "/customers", json=test_customer.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # update the customer
        new_customer = resp.get_json()
        logging.debug(new_customer)
        new_customer["address"] = "unknown"
        resp = self.app.put(
            "/customers/{}".format(new_customer["id"]),
            json=new_customer,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer["address"], "unknown")
    
        # # Make sure location header is set
        # location = resp.headers.get("Location", None)
        # self.assertIsNotNone(location)
        # # Check the data is correct
        # new_customer = resp.get_json()
        # self.assertEqual(new_customer["name"], test_customer.name, "Names do not match")
        # self.assertEqual(
        #     new_customer["category"], test_customer.category, "Categories do not match"
        # )
        # self.assertEqual(
        #     new_customer["available"], test_customer.available, "Availability does not match"
        # )
        # # Check that the location header was correct
        # resp = self.app.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_customer = resp.get_json()
        # self.assertEqual(new_customer["name"], test_customer.name, "Names do not match")
        # self.assertEqual(
        #     new_customer["category"], test_customer.category, "Categories do not match"
        # )
        # self.assertEqual(
        #     new_customer["available"], test_customer.available, "Availability does not match"
        # )