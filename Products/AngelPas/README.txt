Description

    AngelPas lets you treat ANGEL-dwelling course sections as Plone groups. Thanks to Joe Deluca's RosterSynch plugin for inspiration.
    
    Each section can give birth to several groups:
    
    * One for each team, name like "Philosophy 101 Section 1: Team A"
    * A group containing people with the Instructor role within a section: "Philosophy 101 Section 1: Instructors"
    * A group containing people with the Writer role within a section: "Philosophy 101 Section 1: Writers"
    * A group containing people with the Student role within a section: "Philosophy 101 Section 1: Students"
    
    It doesn't bother making groups that have no members, since you can't add anyone to them through Plone anyway.

Installation

    Make sure my Properties Plugin comes before mutable_properties, or mutable_properties will scribble over my provided full names with ''.