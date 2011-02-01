# -*- coding: utf-8 -*-
import os
from slobtree import Index
from lettuce import after, before, step, world


@after.each_scenario
@before.each_scenario
def clean_up(scenario):
    world.index = None
    try:
        os.unlink('test.slob')
    except: pass


@step(u'Given I have a new Index')
def given_i_have_a_new_index(step):
    world.index = Index('test.slob')


@step(u"When I insert key '(.*)' with data '(.*)'")
def when_i_insert_key_with_data(step, key, val):
    world.index.insert(key, val)


@step(u"Then the index file should contain '(.*)'")
def then_the_index_file_should_contain(step, expected_contents):
    expected_contents = expected_contents.replace('\\n', '\n')
    real_contents = open('test.slob').read()
    assert real_contents == expected_contents, 'Got """%s"""' % real_contents


@step(u"Given I have an Index with data '(.*)'")
def given_i_have_an_index_with_data(self, data):
    data = data.replace('\\n', '\n')
    open('test.slob', 'w').write(data)
    world.index = Index('test.slob')


@step(u"When I search for key '(.*)'")
def when_i_search_for_key(self, key):
    world.result = world.index.search(key)


@step(u"Then I should get '(.*)'")
def then_i_should_get(self, expected_value):
    assert world.result == expected_value, 'Expected %s' % expected_value
