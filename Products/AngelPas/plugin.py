import logging
import os
from time import time

from persistent.dict import PersistentDict
from elementtree import ElementTree
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from plone.memoize import ram
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.group import IGroupIntrospection
import Products.PlonePAS.plugins.group as PlonePasGroupPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupEnumerationPlugin, IGroupsPlugin, IUserEnumerationPlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.permissions import ManageUsers
from Products.AngelPas.utils import www_directory, tests_directory
from zope.interface import implements


class MultiPlugin(BasePlugin):
    security = ClassSecurityInfo()
    meta_type = 'AngelPas Plugin'
        
    ## PAS interface implementations: ############################
    
    # IGroupEnumerationPlugin:
    security.declarePrivate('enumerateGroups')
    def enumerateGroups(self, id=None, title=None, exact_match=False, sort_by=None, max_results=None, **kw):
        group_ids = []
        
        # Build list of group IDs we should return:
        if exact_match:  # Should this be case-sensitive?
            if id:
                if id in self._groups:
                    group_ids.append(id)
            elif title:
                for k, v in self._groups.iteritems():
                    if v['title'] == title:
                        group_ids.append(k)
                        break  # when exact_match is True, we may only return 1. This is unpredictable, though, since the dict is unordered and title may not be unique. In practice, it may not be a problem.
        else:  # Do case-insensitive containment searches. Searching on '' returns everything.
            for k, v in self._groups.iteritems():
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
    
    # IUserEnumerationPlugin (so IGroupIntrospection's methods will actually return users):
    def enumerateUsers(self, id=None, login=None, exact_match=False, sort_by=None, max_results=None, **kw):
        user_ids = []
        
        # Build list of user IDs we should return:
        if exact_match:  # Should this be case-sensitive?
            if id:
                if id in self._users:
                    user_ids.append(id)
            if login:
                raise NotImplementedError("We have yet to figure out what to do about login names. It's probably hard to get them.")
        else:  # Do case-insensitive containment searches. Searching on '' returns everything.
            for k in self._users:
                k_lower = k.lower()
                if (id is not None and id.lower() in k_lower) or (login is not None and login.lower() in k_lower):
                    user_ids.append(k)
        
        # For each gathered user ID, flesh out a user info record:
        plugin_id = self.getId()
        user_infos = [{'id': uid, 'login': uid, 'pluginid': plugin_id} for uid in user_ids]  # TODO: Stop making bad assumption that ID and login name are the same.
        
        # Sort, if requested:
        if sort_by in ['id', 'login']:
            user_infos.sort(key=lambda x: x[sort_by])
        
        # Truncate, if requested:
        if max_results is not None:
            del user_infos[max_results:]
        
        return tuple(user_infos)
    
    # IGroupsPlugin:
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        return tuple(self._users.get(principal.getId(), {}).get('groups', set()))
    
    # IGroupIntrospection:
    _findGroup = PlonePasGroupPlugin.GroupManager._findGroup
    _createGroup = PlonePasGroupPlugin.GroupManager._createGroup

    def getGroupById(self, group_id, default=None):
        if group_id in self._groups:
            plugins = self._getPAS()._getOb('plugins')
            return self._findGroup(plugins, group_id, None)
        else:
            return default

    def getGroups(self):
        return [self.getGroupById(x) for x in self.getGroupIds()]

    def getGroupIds(self):
        return self._groups.keys()

    def getGroupMembers(self, group_id):
        """Return a list of usernames of the members of the group."""
        return [id for (id, info) in self._users.iteritems() if group_id in info['groups']]  # TODO: don't linear scan over users
            
    ## Helper methods: ######################
    
    @property
    def _users(self):
        """Return a mapping where the keys are user IDs and the values are group into records.
        
        Example:
            
            {'fsmith':
                {'groups': set(['TR_200506S1_ALH245_001', 'TR_200506S1_ALH245_002'])}
            }
        
        """
        return self._angel_data[0]
    
    @property
    def _groups(self):
        """Return a mapping of group IDs to group info records.
        
        Example:
        
            {'TR_200506S1_ALH245_001':
                {'title': 'Edison Services Demo Course'}
            }
        
        """
        return self._angel_data[1]
    
    security.declarePrivate('_roster_xml')
    def _roster_xml(self, section_id):
        """Return the roster XML of the given section."""
        # TODO: Call Angel API for roster xml. Get the address from self._config.
        f = open(os.path.join(tests_directory, '%s.xml' % section_id), 'r')
        try:
            xml = f.read()
        finally:
            f.close()
        return xml
    
    @property
    @ram.cache(lambda *args: time() // (60 * 60))
    def _angel_data(self):
        """Return the user and group info from ANGEL as a 2-item tuple: (users, groups).
        
        See _users() and _groups() docstrings for details of each.
        """
        def group_title_from_tree(tree):
            return tree.findtext('.//roster/course_title')
            
        def group_id_from_tree(tree):
            return tree.findtext('.//roster/course_id')
            
        def users_from_tree(tree):
            """Return an iterator of userids."""
            return ((member.findtext('user_id').lower() for member in tree.getiterator('member')))
        
        users = {}
        groups = {}
        for s in self._config['sections']:
            tree = ElementTree.fromstring(self._roster_xml(s))  # may raise xml.parsers.expat.ExpatError
            
            # Make a group info record:
            groups[s] = {'title': group_title_from_tree(tree)}
            
            # Add this group to each member's user info record:
            group_id = group_id_from_tree(tree)
            for u in users_from_tree(tree):
                users.setdefault(u, {'groups': set()})['groups'].add(group_id) 
        return users, groups

    ## ZMI crap: ############################
    
    def __init__(self, id, title=None):
        BasePlugin.__init__(self)

        self._setId(id)
        self.title = title
        self._config = PersistentDict({'url': 'https://cmsdev1.ais.psu.edu/api/default.asp', 'username': '', 'password': '', 'sections': []})

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
        for f in ['url', 'username', 'password', 'sections']:
            self._config[f] = REQUEST.form[f]
        return REQUEST.RESPONSE.redirect('%s/manage_config' % self.absolute_url())
    

implementedInterfaces = [IGroupEnumerationPlugin, IGroupsPlugin, IGroupIntrospection, IUserEnumerationPlugin]
classImplements(MultiPlugin, *implementedInterfaces)
InitializeClass(MultiPlugin)  # Make the security declarations work.
