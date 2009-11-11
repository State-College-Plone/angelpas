"""Unit tests for IGroups plugin"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import AngelUnitTest, plugin_id
from Products.PluggableAuthService.PropertiedUser import PropertiedUser


class TestGroupsForPrincipal(AngelUnitTest):
    def test_groups_for_principal(self):
        groups = list(self._plugin.getGroupsForPrincipal(PropertiedUser('alh245')))
        groups.sort()
        self.failUnlessEqual(groups, ['001', '002'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGroupsForPrincipal))
    return suite
