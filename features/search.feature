Feature: Search for data in an index
  In order to find data in the index
  As a programmer
  I want to be able to search the index

  Scenario: Search for an existing key in a single-item index
    Given I have an Index with data:
      """
      "
      "{"data":[["foo","bar"]]}
      """
    When I search for key 'foo'
    Then I should get 'bar'

  Scenario: Search for an nonexistant key in a single-item index
    Given I have an Index with data:
      """
      "
      "{"data":[["foo","bar"]]}
      """
    When I search for key 'blar'
    Then I should get None

  Scenario: Search for an existing key in a split index
    Given I have an Index with data:
      """
      "
      "{"data":[["foo","bar"]]}
      "{"data":[["bar","baz"]]}
      "{"keys":[["bar",27], ["foo",1]]}
      """
    Whe I search for key 'foo'
    Then I should get 'bar'

  Scenario: Search for an nonexistant key in a split index
    Given I have an Index with data:
      """
      "
      "{"data":[["foo","bar"]]}
      "{"data":[["bar","baz"]]}
      "{"keys":[["bar",27], ["foo",1]]}
      """
    When I search for key 'blar'
    Then I should get None
