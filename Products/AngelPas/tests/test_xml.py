"""Unit tests for the XML parsing and transformation"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import AngelUnitTest


class TestXml(AngelUnitTest):
    """Test a representative piece of the sample data to make sure XML parsing and transformation to the in-memory data formats worked."""
    
    def test_users(self):
        u = self._plugin._users
        self.failUnlessEqual(u['alh245']['groups'], set(['002', '001']))
        self.failUnlessEqual(u['smj11']['groups'], set(['002', '113']))

    def test_groups(self):
        g = self._plugin._groups
        self.failUnlessEqual(g['002']['title'], 'Demo Course 2')
        self.failUnlessEqual(g['113']['title'], 'Funny-titled 3')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXml))
    return suite
