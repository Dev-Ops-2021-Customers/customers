Feature: The customer service back-end
    As a Customer Squad
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        |   name    |    address              | phone_number  |  email                |  credit_card   |
        |   sam     |    123 palm springs rd  | 555-682-5832  |  sam@gnocci.com       |  VISA          |
        |   steph   |    456 flay st          | 555-902-3948  |  steph@bobbyflay.com  |  VISA          |
        |   kelly   |    789 miami ave        | 555-102-2948  |  kelly@catan.com      |  VISA          |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "name" to "Seba"
    And I set the "address" to "123 chile st"
    And I set the "phone_number" to "555-123-2364"
    And I set the "email" to "seba@franksinatra.com"
    And I set the "credit_card" to "VISA"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "name" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "address" field should be empty
    And the "phone_number" field should be empty
    And the "email" field should be empty
    And the "credit_card" field should be empty
    When I paste the "name" field
    And I press the "search" button
    Then I should see "Seba" in the "name" field
    Then I should see "123 chile st" in the "address" field
    Then I should see "555-123-2364" in the "phone_number" field
    Then I should see "seba@franksinatra.com" in the "email" field
    Then I should see "VISA" in the "credit_card" field

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "sam" in the results
    And I should see "steph" in the results
    And I should see "kelly" in the results

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "name" to "sam"
    And I press the "Search" button
    Then I should see "sam" in the "name" field
    Then I should see "123 palm springs rd" in the "address" field
    Then I should see "555-682-5832" in the "phone_number" field
    Then I should see "sam@gnocci.com" in the "email" field
    And I should see "VISA" in the "credit_card" field
    When I change "name" to "samuel"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "samuel" in the "name" field

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I change "id" to "1"
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"

Scenario: Retrieve a Customer
    When I visit the "Home Page"
    And I set the "name" to "Sebastian"
    And I set the "address" to "123 baby st"
    And I set the "phone_number" to "555-124-2564"
    And I set the "email" to "sebastian@cutebaby.com"
    And I set the "credit_card" to "VISA"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    When I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "address" field should be empty
    And the "phone_number" field should be empty
    And the "email" field should be empty
    And the "credit_card" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "Sebastian" in the "name" field
    Then I should see "123 baby st" in the "address" field
    Then I should see "555-124-2564" in the "phone_number" field
    Then I should see "sebastian@cutebaby.com" in the "email" field
    Then I should see "VISA" in the "credit_card" field

Scenario: Deactivate a Customer
    When I visit the "Home Page"
    And I copy the "id" field
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Deactivate" button
    Then I should see the message "Customer deactivated."
    And I should see "False" in the "Active" dropdown

Scenario: Activate a Customer
    When I visit the "Home Page"
    And I copy the "id" field
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Deactivate" button
    And I press the "Activate" button
    Then I should see the message "Customer activated."
    And I should see "True" in the "Active" dropdown
