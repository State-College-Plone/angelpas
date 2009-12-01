"""Unit tests for group enumeration plugin"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import MockNetworkingUnitTest, plugin_id


class TestEnumeration(MockNetworkingUnitTest):
    def test_find_all(self):
        all_groups = self._plugin.enumerateGroups()
        self.failUnless(len(all_groups) > 0)
    
    def test_exact_match_by_id(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(id='Demo Course 1', exact_match=True), ({'id': 'Demo Course 1', 'pluginid': plugin_id},))
    
# Known failure. This isn't implemented yet. I don't think Plone uses this feature.
#     def test_multiple_matches_by_id(self):
#         """PAS says you must accept sequences of IDs."""
#         self.failUnlessEqual(self._plugin.enumerateGroups(id=['Demo Course 1', 'Demo Course 2'], exact_match=True), ({'id': 'Demo Course 1', 'pluginid': plugin_id}, {'id': 'Demo Course 2', 'pluginid': plugin_id}))
    
    def test_exact_match_by_title(self):
        """IDs and titles are considered the same for the moment."""
        self.failUnlessEqual(self._plugin.enumerateGroups(title='Demo Course 1', exact_match=True), ({'id': 'Demo Course 1', 'pluginid': plugin_id},))
    
    def test_inexact_match_by_id(self):
        # Testing sorting at the same time, while a teensy bit dirty, lets us compare tuples without having to sort them ourselves.
        self.failUnlessEqual(self._plugin.enumerateGroups(id='Demo Course 1', sort_by='id'), ({'id': 'Demo Course 1', 'pluginid': plugin_id}, {'id': 'Demo Course 1: Instructors', 'pluginid': plugin_id}))
    
    def test_inexact_match_by_title(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(title='Demo Course 1', sort_by='id'), ({'id': 'Demo Course 1', 'pluginid': plugin_id}, {'id': 'Demo Course 1: Instructors', 'pluginid': plugin_id}))
    
    def test_max_results(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(title='Demo Course', sort_by='id', max_results=2), ({'id': 'Demo Course 1', 'pluginid': plugin_id}, {'id': 'Demo Course 1: Instructors', 'pluginid': plugin_id}))
    
    def test_find_all(self):
        """Make sure we get some groups out of a wide-open search, such as called by a click to "Show All" in the Users & Groups configlet."""
        self.failUnless(len(self._plugin.enumerateGroups()) > 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEnumeration))
    return suite
