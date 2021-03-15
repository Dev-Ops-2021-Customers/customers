"""
Test cases for Customer Model

"""
import logging
import unittest
import os
from service.models import Customer, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  CUSTOMER   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomer(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """
        customer = Customer(
            name="Alex",
            address="Washington Square Park",
            phone_number="555-555-1234",
            email="alex@jr.com",
            credit_card="VISA"
            )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "Alex")
        self.assertEqual(customer.address, "Washington Square Park")
        self.assertEqual(customer.phone_number, "555-555-1234")
        self.assertEqual(customer.email, "alex@jr.com")
        self.assertEqual(customer.credit_card, "VISA")

    def test_add_a_customer(self):
        """ Create a customer and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(
            name="Alex",
            address="Washington Square Park",
            phone_number="555-555-1234",
            email="alex@jr.com",
            credit_card="VISA"
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_delete_a_customer(self):
        """ Delete a Customer """
        customer = Customer(
            name="Alex",
            address="Washington Square Park",
            phone_number="555-555-1234",
            email="alex@jr.com",
            credit_card="VISA"
        )
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)
