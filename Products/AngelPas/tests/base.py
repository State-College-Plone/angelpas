"""A testing base class providing some common functionality"""

from unittest import TestCase

from Products.AngelPas.plugin import MultiPlugin

plugin_id = 'angel_pas'


class AngelUnitTest(TestCase):
    """Instantiates an ANGEL PAS plugin and fills out some sample data."""
    
    def setUp(self):
        self._plugin = MultiPlugin(plugin_id)
        self._plugin._config['sections'] = ['001', '002', '113']
