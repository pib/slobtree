Feature: Insert data into an index
  In order to save data into the index
  As a programmer
  I want to insert data

  Scenario: First insert
    Given I have a new Index
    When I insert key 'foo' with data 'bar'
    Then the index file should contain:
      """
      "
      "{"data":[["foo","bar"]]}
      """

  Scenario: Two inserts
    Given I have a new Index
    When I insert key 'foo' with data 'bar'
    When I insert key 'bar' with data 'baz'
    Then the index file should contain:
      """
      "
      "{"data":[["foo","bar"]]}
      "{"data":[["bar","baz"],["foo","bar"]]}
      """

  Scenario: Enough inserts to cause a branch
    Given I have a new order 5 Index
    When I insert the following key/value pairs:
      | key  | value  |
      | foo  | bar    |
      | bar  | baz    |
      | baz  | bazzer |
      | moo  | cow    |
      | meow | cat    |
      | woof | dog    |
    Then the index file should contain:
    """
    "
    "{"data":[["foo","bar"]]}
    "{"data":[["bar":"baz"],["foo","bar"]]}
    "{"data":[["bar":"baz"],["baz":"bazzer"],["foo","bar"]]}
    "{"data":[["bar":"baz"],["baz":"bazzer"],["foo","bar"],["moo","cow"]]}
    "{"data":[["bar":"baz"],["baz":"bazzer"],["foo","bar"],["meow","cat"],["moo","cow"]]}
    "{"data":[["bar":"baz"],["baz":"bazzer"],["foo","bar"]]}
    "{"data":[[["meow","cat"],["moo","cow"],["woof","dog"]]}
    "("keys":[["bar",276],["meow",332]]}'
    """
