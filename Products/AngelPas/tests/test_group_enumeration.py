"""Unit tests for group enumeration plugin"""

from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.tests.base import AngelUnitTest, plugin_id


class TestEnumeration(AngelUnitTest):
    def test_exact_match_by_id(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(id='001', exact_match=True), ({'id': '001', 'pluginid': plugin_id},))
    
    def test_multiple_matches_by_id(self):
        """PAS says you must accept sequences of IDs."""
        self.failUnlessEqual(self._plugin.enumerateGroups(id=['001', '002'], exact_match=True), ({'id': '001', 'pluginid': plugin_id}, {'id': '002', 'pluginid': plugin_id}))
    
    def test_exact_match_by_title(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(title='Demo Course 1', exact_match=True), ({'id': '001', 'pluginid': plugin_id},))
    
    def test_inexact_match_by_id(self):
        # Testing sorting at the same time, while a teensy bit dirty, lets us compare tuples without having to sort them ourselves.
        self.failUnlessEqual(self._plugin.enumerateGroups(id='00', sort_by='id'), ({'id': '001', 'pluginid': plugin_id}, {'id': '002', 'pluginid': plugin_id}))
    
    def test_inexact_match_by_title(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(title='Course', sort_by='id'), ({'id': '001', 'pluginid': plugin_id}, {'id': '002', 'pluginid': plugin_id}))
    
    def test_max_results(self):
        self.failUnlessEqual(self._plugin.enumerateGroups(title='e', sort_by='id', max_results=2), ({'id': '001', 'pluginid': plugin_id}, {'id': '002', 'pluginid': plugin_id}))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEnumeration))
    return suite
