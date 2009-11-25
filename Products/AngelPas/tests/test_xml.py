"""Unit tests for the XML parsing and transformation"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import MockNetworkingUnitTest

alh245_groups = ['Demo Course 1', 'Demo Course 1: Instructors', 'Demo Course 2', 'Demo Course 2: Instructors']


class TestXml(MockNetworkingUnitTest):
    """Test a representative piece of the sample data to make sure XML parsing and transformation to the in-memory data formats worked."""
    
    def test_user_group_assignments(self):
        u = self._plugin._users
        self.failUnlessEqual(u['alh245']['groups'], set(alh245_groups))
        self.failUnlessEqual(u['smj11']['groups'], set(['Demo Course 2', 'Demo Course 2: Students', 'Demo Course 2: The A Team', 'Demo Course 2: The B Team', 'Funny-titled 3', 'Funny-titled 3: Writers', 'Funny-titled 3: The Q Team']))

    def test_user_fullnames(self):
        u = self._plugin._users
        self.failUnlessEqual(u['alh245']['fullname'], 'Amy Garbrick')

    def test_groups(self):
        self.failUnlessEqual(self._plugin._groups, set(['Demo Course 1', 'Demo Course 1: Instructors', 'Demo Course 2', 'Demo Course 2: Students', 'Demo Course 2: Instructors', 'Funny-titled 3', 'Funny-titled 3: Writers', 'Demo Course 2: The A Team', 'Demo Course 2: The B Team', 'Funny-titled 3: The Q Team']))

    def test_no_unnecessary_groups(self):
        """Make sure groups that have no members aren't created."""
        self.failIf('Funny-titled 3: Instructors' in self._plugin._groups)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXml))
    return suite
