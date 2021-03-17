# customers

NYU DevOps Customers Team

## To run the Flask app locally

```
vagrant up
vagrant ssh
cd /vagrant/
```
To run on your own machine, you can see by visiting: http://localhost:5000/

## Testing
- Unit tests: `cd /vagrant/` -> `nosetests`

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
