"""Unit tests for IGroups plugin"""

from Products.AngelPas.tests.base_integration import IntegrationTest


class TestGroupIntrospection(IntegrationTest):
    def test_get_group_members(self):
        user_ids = self._plugin.getGroupMembers('Demo Course 1')
        self.failUnlessEqual(user_ids, ['alh245'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGroupIntrospection))
    return suite
