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
        self.failUnlessEqual(self._plugin._roster_xml('SP200809-UP-ADMIN-Kolbe_Test-001'), """<?xml version="1.0"?>\r\n<result><success><roster><referer></referer><security>ok</security>  <course_title>Kolbe Test Course</course_title>\r\n  <course_id>SP200809-UP-ADMIN-Kolbe_Test-001</course_id>\r\n  <member>\r\n    <user_id>JSM298</user_id>\r\n    <course_rights>2</course_rights>\r\n<team></team>\r\n    <fname>JENNIFER SUSAN</fname>\r\n    <mname></mname>\r\n    <lname>MULLEN</lname>\r\n    <confidential>0</confidential>\r\n  </member>\r\n  <member>\r\n    <user_id>LDK107</user_id>\r\n    <course_rights>2</course_rights>\r\n<team></team>\r\n    <fname>LARRY DWAYNE</fname>\r\n    <mname></mname>\r\n    <lname>KOLBE</lname>\r\n    <confidential>0</confidential>\r\n  </member>\r\n  <member>\r\n    <user_id>LDK107ADM</user_id>\r\n    <course_rights>32</course_rights>\r\n<team></team>\r\n    <fname></fname>\r\n    <mname></mname>\r\n    <lname></lname>\r\n    <confidential>0</confidential>\r\n  </member>\r\n  <member>\r\n    <user_id>LKOLBE</user_id>\r\n    <course_rights>64</course_rights>\r\n<team></team>\r\n    <fname></fname>\r\n    <mname></mname>\r\n    <lname></lname>\r\n    <confidential>0</confidential>\r\n  </member>\r\n  <member>\r\n    <user_id>SAR126</user_id>\r\n    <course_rights>2</course_rights>\r\n<team></team>\r\n    <fname></fname>\r\n    <mname></mname>\r\n    <lname></lname>\r\n    <confidential>0</confidential>\r\n  </member>\r\n  <member>\r\n    <user_id>XIK5000</user_id>\r\n    <course_rights>2</course_rights>\r\n    <team>Students</team>\r\n    <fname>Test</fname>\r\n    <mname></mname>\r\n    <lname>Kolbe</lname>\r\n    <confidential>0</confidential>\r\n  </member>\r\n</roster></success></result>""")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNetworking))
    return suite
