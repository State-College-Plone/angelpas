"""Unit tests for IGroups plugin"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import MockNetworkingUnitTest, plugin_id
from Products.PluggableAuthService.PropertiedUser import PropertiedUser


class TestGroupsForPrincipal(MockNetworkingUnitTest):
    def test_groups_for_principal(self):
        groups = list(self._plugin.getGroupsForPrincipal(PropertiedUser('alh245')))
        groups.sort()
        self.failUnlessEqual(groups, ['Demo Course 1', 'Demo Course 2'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGroupsForPrincipal))
    return suite
