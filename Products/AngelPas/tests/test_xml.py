"""Unit tests for the XML parsing and transformation"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import MockNetworkingUnitTest


class TestXml(MockNetworkingUnitTest):
    """Test a representative piece of the sample data to make sure XML parsing and transformation to the in-memory data formats worked."""
    
    def test_user_group_assignments(self):
        u = self._plugin._users
        self.failUnlessEqual(u['alh245']['groups'], set(['Demo Course 2', 'Demo Course 1']))
        self.failUnlessEqual(u['smj11']['groups'], set(['Demo Course 2', 'Funny-titled 3']))

    def test_user_fullnames(self):
        u = self._plugin._users
        self.failUnlessEqual(u['alh245']['fullname'], 'Amy Garbrick')

    def test_groups(self):
        g = self._plugin._groups
        self.failUnlessEqual(self._plugin._groups, set(['Demo Course 1', 'Demo Course 2', 'Funny-titled 3']))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXml))
    return suite
