from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.utils import www_directory

manage_addAngelPasForm = PageTemplateFile('add.pt', www_directory)

def manage_addAngelPas(self, id, title='', REQUEST=None):
    """Add an AngelPas plugin to a Pluggable Authentication Service."""
    plugin = MultiPlugin(id, title)
    self._setObject(plugin.getId(), plugin)
    
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace?manage_tabs_message=AngelPas+added.' % self.absolute_url())
