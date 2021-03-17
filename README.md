# customers

NYU DevOps Customers Team

The customers resource is a representation of the customer accounts of the eCommerce site.

## To run the Flask app locally

```
vagrant up
vagrant ssh
cd /vagrant/
FLASK_APP=service:app flask run -h 0.0.0.0
```
To run on your own machine, you can see by visiting: http://localhost:5000/

## Run File

```
vagrant up
vagrant ssh
cd /vagrant
```

## Testing
- Unit tests: `cd /vagrant/` -> `nosetests`

## Shutdown Vagrant
```
exit
vagrant halt
```

## API Routes

#### **Create** 
- **POST** `/customers` 

#### **Read** 
- **GET** `/customers/{customer_id}`

#### **Update**
- **PUT** `/customers/{customer_id}`

#### **Delete**
- **DELETE** `/customers/{customer_id}`

#### **List**
- **GET** `/customers`
