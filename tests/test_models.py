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
#  C U S T O M E R   M O D E L   T E S T   C A S E S
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

    def _create_customer(self, customer_name="Alex"):
        """ Create a new Customer """
        return Customer(
            name=customer_name,
            address="Washington Square Park",
            phone_number="555-555-1234",
            email="alex@jr.com",
            credit_card="VISA",
            active = True
        )
            # added active = True to the _create_customer definition

    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = self._create_customer()
            customers.append(test_customer)
        return customers

        # return test_customer 

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
            credit_card="VISA",
            active = True
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

 
    def test_update_a_customer(self):
        """ Update a Customer """
        customer = self._create_customer()
        customer.create()
        logging.debug(customer)
        self.assertEqual(customer.id, 1)
        # Change it an save it
        customer.address = "Union Square"
        original_id = customer.id
        customer.save()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.address, "Union Square")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, 1)
        self.assertEqual(customers[0].address, "Union Square")

    def test_delete_a_customer(self):
        """ Delete a Customer """
        customer = self._create_customer()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)
        
    def test_serialize_a_customer(self):
        """ Test serialization of a Customer """
        customer = self._create_customer()
        customer.create()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], customer.name)
        self.assertIn("address", data)
        self.assertEqual(data["address"], customer.address)
        self.assertIn("phone_number", data)
        self.assertEqual(data["phone_number"], customer.phone_number)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("credit_card", data)
        self.assertEqual(data["credit_card"], customer.credit_card)

    def test_deserialize_a_customer(self):
        """ Test deserialization of a Customer """
        data = {
            "id": 1,
            "name": "Alex",
            "address": "Washington Square Park",
            "phone_number": "555-555-1234",
            "email": "alex@jr.com",
            "credit_card": "VISA"
        }
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "Alex")
        self.assertEqual(customer.address, "Washington Square Park")
        self.assertEqual(customer.phone_number, "555-555-1234")
        self.assertEqual(customer.email, "alex@jr.com")
        self.assertEqual(customer.credit_card, "VISA")
    
    #Missing data is the credit_card
    def test_deserialize_missing_data(self):
        """ Test deserialization of a Customer, missing data"""
        data = {
            "id": 1,
            "name": "Alex",
            "address": "Washington Square Park",
            "phone_number": "555-555-1234",
            "email": "alex@jr.com",
        }
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_find_or_404(self):
        """ Find or throw 404 error """
        customer = self._create_customer()
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)

        # Fetch it back
        customer = Customer.find_or_404(customer.id)
        self.assertEqual(customer.id, 1)

    def test_find_customer(self):
        """ Find a Customer by ID """
        customers = self._create_customers(3)
        for customer in customers:
            customer.create()
        logging.debug(customer)
        # make sure they got saved
        self.assertEqual(len(Customer.all()), 3)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.name, customers[1].name)
    
