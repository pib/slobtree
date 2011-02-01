Feature: Insert data into an index
  In order to save data into the index
  As a programmer
  I want to insert data

  Scenario: First insert
    Given I have a new, empty Index
    When I insert key "foo" with data "bar"
    Then the index file should contain '\n{"data":[["foo","bar"]]}'