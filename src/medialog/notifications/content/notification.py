# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.namedfile import field as namedfile
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from medialog.notifications import _
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RichTextFieldWidget
from medialog.notifications.contentrules.notifyadd import PATTERN_OPTIONS

class INotification(model.Schema):
    """ Marker interface and Dexterity Python Schema for Notification
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:
    # model.load('notification.xml')

    # directives.write_permission(message='cmf.ManagePortal')
    message_type = schema.Choice(
        title=_("Message type"),
        description=_("Select the type of message to display."),
        values=("info", "warning", "error"),
        required=False,
        # default="info",
    )
    
    show_title = schema.Bool(
        title=_("Show message type (Title)"),
        required=False,
    )
    
    directives.widget(
        "message",
        RichTextFieldWidget,
        pattern_options=PATTERN_OPTIONS,
    )
    message = RichText(
        title=_("Message"),
        description=_("The message shown to the user. NOTE: You can use  '${}' variables (see below))"),
        required=True,
    )
    
    user_filter = schema.Bool(
        title=_("label_user_filter", default="Show to all"),
        default=True,
        required=False,
    )
    
    message_users = schema.Set(
        title=_("label_notify_users", default="Notify users"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Principals"),
    )
    
    additional_users = schema.TextLine(
        title=_("Additional notification user(s)"),
        description=_("Use  '${}' variables list below (for example ${user_id} )"),
        required=False
    )

    time_filter = schema.Bool(
        title=_("label_time_filter", default="Show immidiately"),
        default=True,
        required=False, 
    )
       
    relative_time = schema.Time(
        title=_("Time of day"),
        description=_("(From) what time of day, hours:minutes)"),
        required=False, 
    )
    
    effective_date = schema.Datetime(
        title=_("Specific date to show notification"),
        description=_("Effective date. Dont set this if you use time settings above."), 
        required=False, 
    )
    
    
    #directives.mode(message_assigned='hidden')
    message_assigned = schema.List(
        title=_("Assigned to (who should see this)"),
        required=False,
        value_type=schema.TextLine(),
        default=[],
        missing_value=[]
    )
    
    # show_title = schema.Bool(
    #     title=_("Show message type Title)"),
    #     required=False,
    # )
    
    

@implementer(INotification)
class Notification(Item):
    """ Content-type class for INotification
    """
