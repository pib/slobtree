Feature: Insert data into an index
  In order to save data into the index
  As a programmer
  I want to insert data

  Scenario: First insert
    Given I have a new Index
    When I insert key 'foo' with data 'bar'
    Then the index file should contain '\n{"data":[["foo","bar"]]}'

  Scenario: Two inserts
    Given I have a new Index
    When I insert key 'foo' with data 'bar'
    When I insert key 'bar' with data 'baz'
    Then the index file should contain '\n{"data":[["foo","bar"]]}\n{"data":[["bar","baz"],["foo","bar"]]}'
