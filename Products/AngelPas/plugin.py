import logging
import os
from time import time

from persistent.dict import PersistentDict
from elementtree import ElementTree
from AccessControl import ClassSecurityInfo
from BTrees.OOBTree import OOBTree
from Globals import InitializeClass
from plone.memoize import ram
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IGroupEnumerationPlugin, IGroupsPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.permissions import ManageUsers
from Products.AngelPas.utils import www_directory, tests_directory
from zope.interface import implements

logger = logging.getLogger('Products.AngelPas')


class MultiPlugin(BasePlugin):
    implements(IGroupEnumerationPlugin, IGroupsPlugin)
    security = ClassSecurityInfo()
    meta_type = 'AngelPas Plugin'
    
    _v_groups = {}  # {'TR_200506S1_ALH245_001': {'title': 'Edison Services Demo Course'}}
    _v_users_to_groups = OOBTree()
    
    ## PAS interface implementations: ############################

    security.declarePrivate('enumerateGroups')
    def enumerateGroups(self, id=None, title=None, exact_match=False, sort_by=None, max_results=None, **kw):
        group_ids = []
        
        # Build list of group IDs we should return:
        if exact_match:  # Should this be case-sensitive?
            if id:
                if id in self.groups:
                    group_ids.append(id)
            elif title:
                for k, v in self.groups.iteritems():
                    if v['title'] == title:
                        group_ids.append(k)
                        break  # when exact_match is True, we may only return 1. This is unpredictable, though, since the dict is unordered and title may not be unique. In practice, it may not be a problem.
        else:  # Do case-insensitive containment searches. Searching on '' returns everything.
            for k, v in self.groups.iteritems():
                if (id is not None and id.lower() in k.lower()) or (title is not None and title.lower() in v['title'].lower()):
                    group_ids.append(k)
        
        # For each gathered group ID, flesh out a group info record:
        plugin_id = self.getId()
        group_infos = [{'id': gid, 'pluginid': plugin_id} for gid in group_ids]
        
        # Sort, if requested:
        if sort_by == 'id':
            group_infos.sort(key=lambda x: x['id'])
        
        # Truncate, if requested:
        if max_results is not None:
            del group_infos[max_results:]
        
        return tuple(group_infos)
    
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        return tuple(self.users_to_groups.get(principal.getId(), ()))
        
            
    ## Helper methods: ######################
    
    @property
    def groups(self):
        # TODO: add smarts to calculate and cache groups. Perhaps convert to using memoize.
        return self._v_groups
    
    ## ZMI crap: ############################
    
    def __init__(self, id, title=None):
        BasePlugin.__init__(self)

        self._setId(id)
        self.title = title
        self._config = PersistentDict({'courses': []})

    # A method to return the configuration page:
    security.declareProtected(ManageUsers, 'manage_config')
    manage_config = PageTemplateFile('config.pt', www_directory)

    # Add a tab that calls that method:
    manage_options = ({'label': 'Options',
                       'action': 'manage_config'},) + BasePlugin.manage_options
    
    security.declareProtected(ManageUsers, 'config_for_view')
    def config_for_view(self):
        """Return a mapping of my configuration values, for use in a page template."""
        return dict(self._config)
    
    security.declareProtected(ManageUsers, 'manage_changeConfig')
    def manage_changeConfig(self, REQUEST=None):
        """Update my configuration based on form data."""
        self._config[courses] = REQUEST.form['courses']
        return REQUEST.RESPONSE.redirect('%s/manage_config' % self.absolute_url())

    @property
    @ram.cache(lambda *args: time() // (60 * 60))
    def users_to_groups(self):
        """Return a mapping where the keys are user IDs and the values are sets of group IDs that the user belongs to.
        
        Example: {'fsmith': set(['TR_200506S1_ALH245_001', 'TR_200506S1_ALH245_002'])}
        """
        #Loop over courses
        #Call Angel API for roster xml. Get the address from self._config, and make it default to PSU's.
        f = open(os.path.join(tests_directory, 'sample.xml'), 'r')
        try:
            users = self._users_from_angel_response(f.read())
        finally:
            f.close()
        return dict([(u, set(['TR_200506S1_ALH245_001'])) for u in users])
    
    def _group_title_from_angel_response(self, response):
        """Parse the XML response from Angel and pull out the group title."""
        tree = ElementTree.fromstring(response) #May raise xml.parsers.expat.ExpatError
        return tree.findtext('//roster/course_title')
        
    def _users_from_angel_response(self, response):
        """Parse the XML response from Angel and pull out a list of userids."""
        tree = ElementTree.fromstring(response) #May raise xml.parsers.expat.ExpatError
        
        users = []
        for member in tree.getiterator('member'):
            users.append(member.findtext('user_id').lower())
        return users

InitializeClass(MultiPlugin)  # Make the security declarations work.
