# -*- coding: utf-8 -*-
import os
from slobtree import Index
from lettuce import after, before, step, world
from nose.tools import assert_equals

@after.each_scenario
@before.each_scenario
def clean_up(_scenario):
    world.index = None
    try:
        os.unlink('test.slob')
    except OSError:
        pass


@step(u'I have a new order (.*) Index')
def given_i_have_a_new_index_with_a_branching_factor_of(_self, b):
    world.index = Index('test.slob', branching_factor=int(b))


@step(u'I have a new Index')
def given_i_have_a_new_index(_self):
    world.index = Index('test.slob')


@step(u"I insert key '(.*)' with data '(.*)'")
def when_i_insert_key_with_data(_self, key, val):
    world.index.insert(key, val)


@step(u"I insert the following key/value pairs:")
def when_i_insert_the_following_key_value_pairs(self):
    for pair in self.hashes:
        world.index.insert(pair['key'], pair['value'])


@step(u"the index file should contain:")
def the_index_file_should_contain(self):
    real_contents = open('test.slob').read()
    assert_equals(real_contents, self.multiline)


@step(u"I have an Index with data:")
def i_have_an_index_with_data(self):
    open('test.slob', 'w').write(self.multiline)
    world.index = Index('test.slob')


@step(u"I search for key '(.*)'")
def i_search_for_key(_self, key):
    world.result = world.index.search(key)


@step(u"I should get '(.*)'")
def i_should_get(_self, expected_value):
    assert_equals(world.result, expected_value)


@step(u"I should get None")
def i_should_get_none(_self):
    assert_equals(world.result, None)
