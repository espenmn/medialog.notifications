# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from plone.app.textfield import RichText


from medialog.notifications import _


class INotification(model.Schema):
    """ Marker interface and Dexterity Python Schema for Notification
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:
    # model.load('notification.xml')

    # directives.write_permission(message='cmf.ManagePortal')
    message = RichText(
        title=_("Message"),
        description=_("The message to send to the user."),
        required=True,
    )

    # directives.write_permission(message_type='cmf.ManagePortal')
    message_type = schema.Choice(
        title=_("Message type"),
        description=_("Select the type of message to display."),
        values=("info", "warning", "error"),
        required=False,
        default="info",
    )
    
    # directives.write_permission(message_users='cmf.ManagePortal')
    message_users = schema.Set(
        title=_("label_notify_users", default="Notify users"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Principals"),
    )
    
    
    directives.mode(message_assigned='hidden')
    message_assigned = schema.List(
        title=_("Assigned to (who should see this)"),
        required=False,
        value_type=schema.TextLine(),
        default=[],
        missing_value=[]
    )
    
    show_title = schema.Bool(
        title=_("Show message type Title)"),
        required=False,
    )
    
    

@implementer(INotification)
class Notification(Item):
    """ Content-type class for INotification
    """
