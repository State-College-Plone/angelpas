AngelPas
========

Description
-----------

AngelPas integrates ANGEL-dwelling course sections with Plone's user-and-group
machinery.

Each section gives rise to several groups:

* One for each team, name like "Philosophy 101 Section 1: Team A"

* One of people with the Instructor role within a section: "Philosophy 101
  Section 1: Instructors"

* One of people with the Student role within a section: "Philosophy 101
  Section 1: Students"

* One of people with the Writer role within a section: "Philosophy 101
  Section 1: Writers"

* One named for the section itself, "Philosophy 101 Section 1", which is a
  union of everyone in the above groups.

Groups that have no members are hidden to cut down on noise, since you can't add
anyone to them through Plone anyway.

The users belonging to the above groups are manifested as Plone users, complete
with full names if ANGEL provides them. They can be assigned privileges and
group memberships within Plone using its normal facilities.

For performance reasons, the information fetched from ANGEL is cached for an
hour. To clear the cache, restart Plone.


Installation
------------

Installation is like that of any other PAS plugin. The only gotcha is that
AngelPas's Properties plugin must come before Plone's mutable_properties plugin.

1. Install AngelPas, for example by dropping it in your *products* folder.

2. In the *acl_users* folder within your Plone site, add an *AngelPas Plugin*.

3. Click the new plugin, and fill out the API username and password, the IDs
   of the course sections to use, etc. Click *Save Changes*.

4. Click the plugin's *Activate* tab, and check all the boxes. Click *Update*.

5. Click the *Activate* tab again, then click the *Propertes* link next to the
   checkbox (not the tab at the top of the screen).

6. Move the AngelPas plugin above the *mutable_properties* plugin. Without
   this step, mutable_properties will obscure ANGEL's provided full names with an
   empty string.


Use
---

When AngelPas has trouble communicating with the ANGEL server, it logs an error
at the level ERROR. For example...

    ERROR Products.AngelPas ANGEL roster request returned an error: Not
    authenticated

It then allows Plone to continue without presenting an error to the user. This
at least allows the site to continue functioning at a reduced level while ANGEL
is unavailable. It is advisable to monitor your logs to catch ANGEL problems
especially after changing AngelPas settings.


Troubleshooting
---------------

An error like this...

    ERROR Products.AngelPas ANGEL roster request returned an error: Not authenticated

...can indicate, at Penn State anyway, that your IP address is not allowed to
access ANGEL. Contact the ANGEL administrators.


Authors
-------

Erik Rose and Eric Steele of the WebLion group at Penn State University

Thanks to Joe Deluca's RosterSynch plugin for inspiration!


Support
-------

Contact the WebLion team at support@weblion.psu.edu or join our IRC channel,
#weblion on irc.freenode.net. The `WebLion wiki <http://weblion.psu.edu/trac/weblion>`_ is full of good stuff.

Please report bugs using the
`WebLion issue tracker <https://weblion.psu.edu/trac/weblion/newticket?component=AngelPas&version=1.0>`_.


Version History
---------------

1.0b1
    * So it begins. No known bugs but hasn't seen a lot of real-world testing.
