"""Tests for error handling"""

from Products.AngelPas.tests.base import UnitTest
from Products.AngelPas.plugin import AngelDataError


class TestErrors(UnitTest):
    def test_unparseable(self):
        self.failUnlessRaises(AngelDataError, self._plugin._roster_tree, "You can't parse this!")
    
    def test_api_failure(self):
        self.failUnlessRaises(AngelDataError, self._plugin._roster_tree, """<?xml version="1.0"?>
  <result><error>Bad course ID.</error></result>""")
    
    def test_no_error_message(self):
        self.failUnlessRaises(AngelDataError, self._plugin._roster_tree, """<?xml version="1.0"?>
  <result></result>""")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestErrors))
    return suite
