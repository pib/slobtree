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

@step(u'Given I have a new, empty Index')
def given_i_have_a_new_empty_db(step):
    world.index = Index('test.slob')

@step(u'When I insert key "(.*)" with data "(.*)"')
def when_i_insert_key_group1_with_data_group2(step, key, val):
    world.index.insert(key, val)

@step(u"Then the index file should contain '(.*)'")
def then_the_index_file_should_contain(step, expected_contents):
    expected_contents = expected_contents.replace('\\n', '\n')
    real_contents = open('test.slob').read()
    assert real_contents == expected_contents, 'Got """%s"""' % real_contents

