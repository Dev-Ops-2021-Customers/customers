## Travis CI
[![Build Status](https://travis-ci.com/Dev-Ops-2021-Customers/customers.svg?branch=main)](https://travis-ci.com/Dev-Ops-2021-Customers/customers)
[![codecov](https://codecov.io/gh/Dev-Ops-2021-Customers/customers/branch/main/graph/badge.svg?token=CJVZ16WGW1)](https://codecov.io/gh/Dev-Ops-2021-Customers/customers)



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
honcho start
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

#### **Find by Name**
- **GET** `/customers?name={search criteria}`

#### **Deactivate**
- **PUT** `/customers/{}/deactivate`

#### **Activate**
- **PUT** `/customers/{}/activate`
