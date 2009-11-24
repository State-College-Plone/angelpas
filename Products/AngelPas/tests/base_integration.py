"""Base class for integration tests"""

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.AngelPas.plugin import MultiPlugin, implementedInterfaces
from Products.AngelPas.tests.base import plugin_id, test_sections, monkeypatch, unmonkeypatch

PloneTestCase.installProduct('AngelPas')
PloneTestCase.setupPloneSite(products=['AngelPas'])


class IntegrationTest(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        monkeypatch(MultiPlugin)

        # Install an AngelPas plugin:
        acl_users = self._acl_users
        constructors = acl_users.manage_addProduct['AngelPas']  # http://wiki.zope.org/zope2/ObjectManager
        constructors.manage_addAngelPas(plugin_id, title='AngelPas Plugin')
        
        # Activate it:
        plugins = acl_users['plugins']
        for interface in implementedInterfaces:
            plugins.activatePlugin(interface, plugin_id)  # plugins is a PluginRegistry
        
        # Configure it:
        self._plugin._config['sections'] = test_sections
    
    def afterTearDown(self):
        unmonkeypatch(MultiPlugin)
    
    @property
    def _acl_users(self):
        """Return the acl_users folder in the Plone site."""
        return getToolByName(self.portal, 'acl_users')
    
    @property
    def _plugin(self):
        return self._acl_users[plugin_id]
