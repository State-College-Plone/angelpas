from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin
from Products.AngelPas.plugin import MultiPlugin
from Products.AngelPas.utils import www_directory
from Products.AngelPas.zmi import manage_addAngelPasForm, manage_addAngelPas

try:
    registerMultiPlugin(MultiPlugin.meta_type)
except RuntimeError:
    # Don't explode upon re-registering the plugin:
    pass

def initialize(context):
    context.registerClass(MultiPlugin,
                          permission=add_user_folders,
                          constructors=(manage_addAngelPasForm,
                                        manage_addAngelPas),
                          visibility=None,
                          icon='%s/multiplugin.gif' % www_directory
                         )
