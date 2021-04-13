Feature: The customer service back-end
    As a Customer Squad
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        |    customer_id     |   name    |    address              | phone_number  |  email                |  credit_card   |
        |    1               |   sam     |    123 palm springs rd  | 555-682-5832  |  sam@gnocci.com       |  VISA          |
        |    2               |   steph   |    456 flay st          | 555-902-3948  |  steph@bobbyflay.com  |  VISA          |
        |    3               |   kelly   |    789 miami ave        | 555-102-2948  |  kelly@catan.com      |  VISA          |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "customer_id" to "1"
    And I set the "name" to "Seba"
    And I set the "address" to "123 chile st"
    And I set the "phone_number" to "555-123-2364"
    And I set the "email" to "seba@franksinatra.com"
    And I set the "credit_card" to "VISA"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "customer_id" field
    And I press the "Clear" button
    Then the "customer_id" field should be empty
    And the "name" field should be empty
    And the "address" field should be empty
    And the "phone_number" field should be empty
    And the "email" field should be empty
    And the "credit_card" field should be empty
    When I paste the "customer_id" field
    And I press the "search" button
    Then I should see "Seba" in the "name" field
    Then I should see "123 chile st" in the "address" field
    Then I should see "555-123-2364" in the "phone_number" field
    Then I should see "seba@franksinatra.com" in the "email" field
    Then I should see "VISA" in the "credit_card" field