"""Tests for communication with ANGEL"""

import commands
import re

from Products.AngelPas.tests.base import UnitTest


class TestNetworking(UnitTest):
    def setUp(self):
        super(TestNetworking, self).setUp()
        status, output = commands.getstatusoutput("""security find-generic-password -l 'ANGEL API' -g login.keychain""")
        password = re.findall('^password: "(.+)"$', output, re.MULTILINE)[0]
        if not status:
            config = self._plugin._config
            config['username'] = 'PSUAPI_LA001'
            config['password'] = password
            config['url'] = 'https://cmsdev1.ais.psu.edu/api/default.asp'
        else:
            raise StandardException("""No Keychain item found called "ANGEL API". That's where I expected to find the ANGEL API password.""")
    
    def test_fetch(self):
        self.failUnlessEqual(self._plugin._roster_xml('2008_09_SP-AA-ACCTG-Kolbe_Test-001'), '(Put the good XML here once we actually have access.)')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNetworking))
    return suite
