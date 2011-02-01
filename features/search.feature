Feature: Search for data in an index
  In order to find data in the index
  As a programmer
  I want to be able to search the index

  Scenario: Search for an existing key in a single-item index
    Given I have an Index with data '\n{"data":[["foo","bar"]]}'
    When I search for key 'foo'
    Then I should get 'bar'