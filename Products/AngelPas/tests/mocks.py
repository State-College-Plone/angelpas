"""Mocked out functions for testing"""

import os

from Products.AngelPas.utils import tests_directory

def _roster_xml(self, section_id):
    """Return the roster XML of the given section."""
    f = open(os.path.join(tests_directory, 'xml', '%s.xml' % section_id), 'r')
    try:
        xml = f.read()
    finally:
        f.close()
    return xml
