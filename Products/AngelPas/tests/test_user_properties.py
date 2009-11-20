"""Unit tests for user property provider plugin"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import AngelUnitTest
from Products.PluggableAuthService.PropertiedUser import PropertiedUser


class TestProperties(AngelUnitTest):
    def test_user_properties(self):
        self.failUnlessEqual(self._plugin.getPropertiesForUser(PropertiedUser('alh245')), {'fullname': 'Amy Garbrick'})


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProperties))
    return suite
