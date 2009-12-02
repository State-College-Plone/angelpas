import logging
from time import time
from urllib import urlopen, urlencode

from persistent.dict import PersistentDict
from elementtree import ElementTree
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from plone.memoize import ram
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.group import IGroupIntrospection
import Products.PlonePAS.plugins.group as PlonePasGroupPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupEnumerationPlugin, IGroupsPlugin, IUserEnumerationPlugin, IPropertiesPlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.permissions import ManageUsers
from xml.parsers.expat import ExpatError

from Products.AngelPas.tests.mocks import _roster_xml as mock_roster_xml
from Products.AngelPas.utils import www_directory

# Constants describing user rights within a section:
_rights_map = {
        '32': 'Instructors',
        '16': 'Writers',
        '2': 'Students'
    }

logger = logging.getLogger('Products.AngelPas')


class AngelDataError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg


class MultiPlugin(BasePlugin):
    security = ClassSecurityInfo()
    meta_type = 'AngelPas Plugin'
        
    ## PAS interface implementations: ############################
    
    # IGroupEnumerationPlugin:
    security.declarePrivate('enumerateGroups')
    def enumerateGroups(self, id=None, title=None, exact_match=False, sort_by=None, max_results=None, **kw):
        # Though title is not (that I know of) guaranteed to be unique or immutable, it probably will be for the set of groups brought into a Plone site. Only by using the title as the group ID can we get Plone to show titles in the Users & Groups control panel's Groups tab, and we have to do that, as the IDs are totally unfriendly. Code for treating ID and title separately is in r9501.
        group_ids = []
        
        # Build list of group IDs we should return:
        if exact_match:  # Should this be case-sensitive?
            title_or_id = title or id
            if title_or_id and title_or_id in self._groups:
                group_ids.append(title_or_id)
        else:  # Do case-insensitive containment searches. Searching on '' returns everything.
            if title is not None:
                title_lower = title.lower()
            if id is not None:
                id_lower = id.lower()
            for each_group in self._groups:
                each_group_lower = each_group.lower()
                if (id is None and title is None) or (id is not None and id_lower in each_group_lower) or (title is not None and title_lower in each_group_lower):
                    group_ids.append(each_group)
        
        # For each gathered group ID, flesh out a group info record:
        plugin_id = self.getId()
        group_infos = [{'id': gid, 'pluginid': plugin_id} for gid in group_ids]
        
        # Sort. (We always sort. We explicitly support sorting by ID, but nothing says we can't sort on it when it's not requested, too. This makes the Groups tab of the Users & Groups control panel look nicer.)
        group_infos.sort(key=lambda x: x['id'])
        
        # Truncate, if requested:
        if max_results is not None:
            del group_infos[max_results:]
        
        return tuple(group_infos)
    
    # IUserEnumerationPlugin (so IGroupIntrospection's methods will actually return users):
    def enumerateUsers(self, id=None, login=None, exact_match=False, sort_by=None, max_results=None, fullname=None, **kw):
        user_ids = set()  # tuples of (user ID, login)
        
        # Build list of user IDs we should return:
        if exact_match:  # Should this be case-sensitive?
            if login:
                if login in self._users:
                    user = self._getPAS().getUser(login)  # Is this going to call our enumerator and always be True or something? Apparently not in Plone, but see the test_exact_match_by_id test in test_user_enumeration.
                    user_id = user and user.getId() or login  # If user doesn't exist, it's a user we're dynamically manifesting, so we can assume id == login.
                    user_ids.add((user_id, login))
            if id:
                if id in self._users:  # TODO: IHNI if this block makes sense.
                    user_ids.add((id, id))
        else:  # Do case-insensitive containment searches. Searching on '' returns everything.
            if login is not None:
                login_lower = login.lower()
            if id is not None:
                id_lower = id.lower()
            if fullname is not None:
                fullname_lower = fullname.lower()
            for k, user_info in self._users.iteritems():  # TODO: Pretty permissive. Should we be searching against logins AND IDs? We might also optimize to avoid redundant tests of None-ship.
                k_lower = k.lower()
                if (id is None and login is None and fullname is None) or \
                   (id is not None and id_lower in k_lower) or \
                   (login is not None and login_lower in k_lower) or \
                   (fullname is not None and fullname_lower in user_info['fullname'].lower()):
                    user_ids.add((k, k))
        
        # For each gathered user ID, flesh out a user info record:
        plugin_id = self.getId()
        user_infos = [{'id': x, 'login': y, 'pluginid': plugin_id} for (x, y) in user_ids]
        
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
    _createGroup = PlonePasGroupPlugin.GroupManager._createGroup  # This is here only so _findGroup can call it.
    
    def getGroupById(self, group_id, default=None):
        if group_id in self._groups:
            plugins = self._getPAS()._getOb('plugins')
            return self._findGroup(plugins, group_id, None)
        else:
            return default

    def getGroups(self):
        return [self.getGroupById(x) for x in self.getGroupIds()]

    def getGroupIds(self):
        return list(self._groups)

    def getGroupMembers(self, group_id):
        """Return a list of usernames of the members of the group."""
        # As of Plone 3.3rc4, roles assigned to supergroups don't filter down to the members of subgroups, so we cannot nest groups to good effect.
        return [id for (id, info) in self._users.iteritems() if group_id in info['groups']]  # TODO: don't linear scan over users
    
    # IPropertiesPlugin:
    def getPropertiesForUser(self, user, request=None):
        login = user.getUserName()
        is_group = getattr(user, 'isGroup', lambda: None)()
        
        if is_group:
            if login in self._groups:
                return {'title': login}  # title == id == login. Yuck. See comments under enumerateGroups().
        else:
            u = self._users.get(login)
            if u:
                ret = {'fullname': u['fullname']}
                email_domain = self._config['email_domain']
                if email_domain:
                    ret['email'] = '%s@%s' % (login, email_domain)
                return ret
        return {}
    
    ## Helper methods: ######################
    
    @property
    def _users(self):
        """Return a mapping where the keys are Access Account IDs (considered equivalent to login names) and the values are user info records.
        
        Example:
            
            {'fsmith':
                {'groups': set(['Edison Services Demo Course', 'Some Other Demo Course']),
                 'fullname': 'Francis Wimbledoofer Smith'  # optional
                }
            }
        
        """
        return self._angel_data[0]
    
    @property
    def _groups(self):
        """Return a set of group titles (which are used as group IDs).
        
        The logical group hierarchy isn't exposed to PAS, since roles assigned to supergroups don't filter down to the members of subgroups as of Plone 3.3rc4. Instead, we flatten everything out, telling PAS that a member of a course section's Instructors group is also a member of the course section's general group, for example.
        
        Example:
            
            set(['Philsophy 101 Section 1',
                 'Philsophy 101 Section 1: Team A',
                 'Philsophy 101 Section 1: Instructors'])
        
        """
        return self._angel_data[1]
    
    security.declarePrivate('_roster_xml')
    def _roster_xml(self, section_id):
        """Return the raw XML of the given section, raising an AngelDataError on error."""
        #return mock_roster_xml(self, section_id)
        config = self._config
        query = urlencode({
                'APIUSER': config['username'],
                'APIPWD': config['password'],
                'STRCOURSE_ID': section_id
            })
        try:
            try:
                f = urlopen('%s?APIACTION=PSU_TEAMLISTXML2&%s' % (config['url'], query))
                xml = f.read()
            except IOError, e:
                raise AngelDataError('An error occurred while communicating with the ANGEL server: %s' % e.strerror)
        finally:  # stupid Python 2.4 and its lack of try...except...finally
            f.close()
        return xml
    
    security.declarePrivate('_roster_tree')
    def _roster_tree(self, xml):
        """Return the parsed XML tree given raw XML from an ANGEL API call, raising an AngelDataError on error."""
        # Parse:
        try:
            tree = ElementTree.fromstring(xml)
        except ExpatError:
            raise AngelDataError('The roster request returned a non-XML response:\n%s' % xml)
        
        # Test for API-level success:
        success_node = tree.find('./success')
        if not success_node:
            error = tree.findtext('./error', None)
            if error:
                raise AngelDataError('ANGEL roster request returned an error: %s' % error)
            else:
                raise AngelDataError('ANGEL roster request failed but returned no error message. Is the API URL correct?')
        
        return tree
    
    @property
    def _angel_data(self):
        """Return the (possibly cached) user and group info from ANGEL as a 2-item tuple: (users, groups).
        
        See _users() and _groups() docstrings for details of each.
        
        On failure, return empty info (so at least people can log into the site using other PAS plugins) and log the failure at level ERROR.
        
        """
        
        @ram.cache(lambda *args: (self._config['url'], self._config['sections'], time() // (60 * 60)))
        def get_data():
            """Return the user and group info from ANGEL as a 2-item tuple: (users, groups).
            
            Throw AngelDataError on failure.
            
            """
            users = {}
            groups = set()
            for s in self._config['sections']:
                tree = self._roster_tree(self._roster_xml(s))
                
                # Add to groups:
                section_title = tree.findtext('.//roster/course_title')
                groups.add(section_title)
                
                for member in tree.getiterator('member'):
                    # Add this group to the member's user info record, also filling out member info like full name as we go:
                    user_id = member.findtext('user_id').lower()
                    fullname = ' '.join([y for y in [member.findtext(x) for x in ('fname', 'mname', 'lname')] if y])
                    if fullname.isupper():  # Penn State's systems return an ugly all-caps name. Title-case it.
                        fullname = fullname.title()
                    u = users.setdefault(user_id, {'groups': set(), 'fullname': fullname})
                    u['groups'].add(section_title)
                    if not u['fullname']:
                        u['fullname'] = fullname
                    
                    # Put the person in the Instructors, Writers, or Students groups if appropriate:
                    rights = member.findtext('course_rights')  # They're not admitting these are bit fields, so we won't treat them as such.
                    addendum = _rights_map.get(rights)
                    ## First, note that this new group exists:
                    if addendum:
                        group_title = '%s: %s' % (section_title, addendum)
                        groups.add(group_title)
                        ## Then, note the user belongs to this group:
                        users[user_id]['groups'].add(group_title)
                    
                    # Put the person in the right team groups:
                    for team in member.getiterator('team'):
                        if team.text:
                            group_title = '%s: %s' % (section_title, team.text)
                            groups.add(group_title)
                            users[user_id]['groups'].add(group_title)
            
            return users, groups
        
        try:
            users, groups = get_data()
        except AngelDataError, e:
            users, groups = {}, set()
            logger.error(e.msg)
        return users, groups

    ## ZMI crap: ############################
    
    def __init__(self, id, title=None):
        BasePlugin.__init__(self)
        self._setId(id)
        self.title = title
        self._config = PersistentDict({'url': 'https://cmsdev1.ais.psu.edu/api/default.asp', 'username': '', 'password': '', 'sections': ['SP200809-UP-ADMIN-Kolbe_Test-001'], 'email_domain': 'psu.edu'})
    
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
        for f in ['url', 'username', 'password', 'sections', 'email_domain']:
            self._config[f] = REQUEST.form[f]
        return REQUEST.RESPONSE.redirect('%s/manage_config' % self.absolute_url())


implementedInterfaces = [IGroupEnumerationPlugin, IGroupsPlugin, IGroupIntrospection, IUserEnumerationPlugin, IPropertiesPlugin]
classImplements(MultiPlugin, *implementedInterfaces)
InitializeClass(MultiPlugin)  # Make the security declarations work.
