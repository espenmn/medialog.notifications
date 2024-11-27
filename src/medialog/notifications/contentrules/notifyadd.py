from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
# from z3c.form import interfaces
from plone import api
from plone.autoform import directives
from plone.app.textfield import RichTextValue
# from plone.app.z3cform.widget import RichTextFieldWidget 
from plone.stringinterp.interfaces import IStringInterpolator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
 
# from Products.statusmessages.interfaces import IStatusMessage
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from datetime import datetime, timedelta   

# from plone.supermodel.directives import fieldset

from medialog.notifications.content.notification import INotification, PATTERN_OPTIONS

class INotifyAddAction(INotification):
    """Interface for the configurable aspects of a notify action.
    This is also used to create add and edit forms, below.
    We reuse the fields from INotification
    And might add one more ?
    """
    directives.order_before(additional_users='time_filter')
    additional_users = schema.TextLine(
        title=_("Additional notification user(s)"),
        description=_("Use  '${}' variables list below (for example ${user_id} )"),
        required=False
    )
    

@implementer(INotifyAddAction, IRuleElementData)
class NotifyAddAction(SimpleItem):
    """The actual persistent implementation of the notify action element."""

    message = ""
    message_type = ""

    element = "plone.actions.NotifyAdd"
    
    #TO DO: Should we both add notify or should be just save it.

    @property
    def summary(self):
        return _(
            "Notify with message ${message}",
            mapping=dict(message=self.message.output),
        )


@adapter(Interface, INotifyAddAction, Interface)
@implementer(IExecutable)
class NotifyAddActionExecutor:
    """The executor for this action.

    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        

    def __call__(self):
        # request = self.context.REQUEST
        portal = api.portal.get()                
        container =  portal.get('notifications', portal)
        obj = self.event.object
        interpolator = IStringInterpolator(obj)
        message = interpolator(self.element.message.raw)
        message_type = self.element.message_type
        message_users = self.element.message_users
        show_title =  self.element.show_title
        time_filter =  self.element.time_filter         
        user_filter = self.element.user_filter 
        additional_users = self.element.additional_users  
        relative_time  = self.element.relative_time  
        effective_date =  self.element.effective_date
        message_groups = self.element.message_groups


        # Will will do all the logic in handlers
        obj = api.content.create(
            type='Notification',
            title='Notification',
            message  = RichTextValue(message),
            message_type = message_type,
            show_title =  show_title,
            message_users = message_users,
            message_groups = message_groups,
            message_assigned = [],
            time_filter = time_filter,
            user_filter = user_filter ,
            effective_date = effective_date,
            additional_users = additional_users,  
            relative_time = relative_time ,
            container=container,
        )
        
        return True


class NotifyAddAddForm(ActionAddForm):
    """An add form for notifyadd rule actions."""

    schema = INotifyAddAction
    label = _("Add Notify Content Action")
    description = _("A notify action saves a message to the user.")
    form_name = _("Configure element")
    Type = NotifyAddAction
    
    template = ViewPageTemplateFile("templates/notification.pt")


class NotifyAddAddFormView(ContentRuleFormWrapper):
    form = NotifyAddAddForm


class NotifyAddEditForm(ActionEditForm):
    """An edit form for notifyadd rule actions.

    z3c.form does all the magic here.
    """

    schema = INotifyAddAction
    label = _("Edit NotifyAdd Action")
    description = _("A notify action can show a message to the user.")
    form_name = _("Configure element")
    
    template = ViewPageTemplateFile("templates/notification.pt")


class NotifyAddEditFormView(ContentRuleFormWrapper):
    form = NotifyAddEditForm