"""Unit tests for IGroups plugin"""

from unittest import TestCase

from Products.AngelPas.plugin import MultiPlugin
from Products.PluggableAuthService.PropertiedUser import PropertiedUser

plugin_id = 'angel_pas'


class TestGroupsForPrincipal(TestCase):
    def setUp(self):
        self._plugin = MultiPlugin(plugin_id)
    
    def test_groups_for_principal(self):
        import pdb;pdb.set_trace()
        self.failUnlessEqual(self._plugin.getGroupsForPrincipal(PropertiedUser('alh245')), ('TR_200506S1_ALH245_001',))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGroupsForPrincipal))
    return suite
