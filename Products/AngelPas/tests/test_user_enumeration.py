"""Unit tests for group enumeration plugin"""

from Products.AngelPas.tests.base import plugin_id
from Products.AngelPas.tests.base_integration import IntegrationTest


class TestEnumeration(IntegrationTest):
# Has an infinite loop:
#     def test_exact_match_by_id(self):
#         self.failUnlessEqual(self._plugin.enumerateUsers(login='alh245', exact_match=True), ({'id': 'alh245', 'login': 'alh245', 'pluginid': plugin_id},))
    
    def test_fullname(self):
        """Test search by fullname, like Plone 3.1's U&G configlet search."""
        self.failUnlessEqual(self._plugin.enumerateUsers(fullname='garbrick'), ({'id': 'alh245', 'login': 'alh245', 'pluginid': plugin_id},))
    
    def test_find_all(self):
        """Make sure we get some users out of a wide-open search, such as called by a click to "Show All" in the Users & Groups configlet."""
        self.failUnless(len(self._plugin.enumerateUsers()) > 0)
    
    # TODO: borrow some other tests from test_group_enumeration.


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEnumeration))
    return suite
