"""A testing base class providing some common functionality"""

import os
from unittest import TestCase

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.utils import tests_directory
from Products.AngelPas.tests.mocks import _roster_xml

plugin_id = 'angel_pas'
test_sections = ['001', '002', '113']

def monkeypatch(plugin_class):
    """Replace the networking code with stuff that returns test data, since very few machines can get through ANGEL's firewall."""
    global _original_roster_xml
    _original_roster_xml = plugin_class._roster_xml
    plugin_class._roster_xml = _roster_xml

def unmonkeypatch(plugin_class):
    """Put the networking code back."""
    plugin_class._roster_xml = _original_roster_xml


class UnitTest(TestCase):
    """Instantiates an ANGEL PAS plugin and fills out some sample data."""
    
    def setUp(self):
        self._plugin = MultiPlugin(plugin_id)
        self._plugin._config['sections'] = test_sections


class MockNetworkingUnitTest(UnitTest):
    """Instantiates an ANGEL PAS plugin and rigs it to return sample data and fake network interaction."""
    
    def setUp(self):
        monkeypatch(MultiPlugin)
        super(MockNetworkingUnitTest, self).setUp()
    
    def tearDown(self):
        super(MockNetworkingUnitTest, self).tearDown()
        unmonkeypatch(MultiPlugin)
