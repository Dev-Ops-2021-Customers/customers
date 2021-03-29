"""
Models for Customer

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class Customer(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    credit_card = db.Column(db.String(63), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<CustomersModel %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id, 
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "credit_card": self.credit_card,
            "active": self.active
            }

    def deserialize(self, data):
        """
        Deserializes a CustomersModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.address = data["address"]
            self.phone_number = data["phone_number"]
            self.email = data["email"]
            self.credit_card = data["credit_card"]
            self.active = True
        except KeyError as error:
            raise DataValidationError(
                "Invalid CustomersModel: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid CustomersModel: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the CustomersModels in the database """
        logger.info("Processing all CustomersModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a CustomersModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a CustomersModel by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all CustomersModels with the given name

        Args:
            name (string): the name of the CustomersModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
