# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


from medialog.notifications import _


class INotification(model.Schema):
    """ Marker interface and Dexterity Python Schema for Notification
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:
    # model.load('notification.xml')


    message = schema.TextLine(
        title=_("Message"),
        description=_("The message to send to the user."),
        required=True,
    )

    message_type = schema.Choice(
        title=_("Message type"),
        description=_("Select the type of message to display."),
        values=("info", "warning", "error"),
        required=True,
        default="info",
    )
    
    message_users = schema.Set(
        title=_("label_notify_users", default="Notify users"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Principals"),
    )
    
    message_read = schema.Bool(
        title=_("Mark message as read"),
        required=False,
    )
    
    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # TO DO: Hide field (at least for 'normal users')
    message_read = schema.Bool(
        title=_("Mark message as read"),
        required=False,
        
    )
 

@implementer(INotification)
class Notification(Item):
    """ Content-type class for INotification
    """
