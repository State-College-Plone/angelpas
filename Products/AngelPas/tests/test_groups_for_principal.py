"""Unit tests for IGroups plugin"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import MockNetworkingUnitTest, plugin_id
from Products.AngelPas.tests.test_xml import alh245_groups
from Products.PluggableAuthService.PropertiedUser import PropertiedUser


class TestGroupsForPrincipal(MockNetworkingUnitTest):
    def test_groups_for_principal(self):
        groups = list(self._plugin.getGroupsForPrincipal(PropertiedUser('alh245')))
        groups.sort()
        self.failUnlessEqual(groups, alh245_groups)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGroupsForPrincipal))
    return suite
