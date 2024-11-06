from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from Products.statusmessages.interfaces import IStatusMessage
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from plone import api
from plone.app.textfield import RichText

from plone.stringinterp.interfaces import IStringInterpolator

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class INotifyAddAction(Interface):
    """Interface for the configurable aspects of a notify action.
    This is also used to create add and edit forms, below.
    """
    
    message_type = schema.Choice(
        title=_("Message type"),
        description=_("Select the type of message to display."),
        values=("info", "warning", "error"),
        required=True,
        default="info",
    )
    
    message = RichText(
        title=_("Message"),
        description=_("The message shown to the user. NOTE: You can use  '${}' variables from"),
        required=True,
        max_length=500,
    )
    
    message_users = schema.Set(
        title=_("label_notify_users", default="Notify users"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Principals"),
    )
    
    # message_assigned = schema.List(
    #     title=_("Mark message as read"),
    #     required=False,
    #     value_type=schema.TextLine(),
        
    # )
    
    
    

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
        request = self.context.REQUEST
        portal = api.portal.get()
        org_message = _(self.element.message)
        message = IStringInterpolator(self.context)(org_message)
        message_type = self.element.message_type
        message_users = self.element.message_users
        
        #TO DO: Should we both add notify or should be just save it.
        obj = api.content.create(
            type='Notification',
            title='Notification',
            message = message,
            message_type = message_type,
            message_users = message_users,
            message_assigned = [],
            container=portal
        )
        
        # IStatusMessage(request).addStatusMessage(message, type=message_type)
        
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
    form = NotifyAddAddForm