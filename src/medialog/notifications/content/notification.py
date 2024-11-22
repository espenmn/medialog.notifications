# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.namedfile import field as namedfile
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from plone import api
from plone.api.portal import getRequest
from medialog.notifications import _
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.autoform.directives import read_permission, write_permission
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.interface import provider

PATTERN_OPTIONS = {
    "tiny": {
            "menu": {
            "edit": {
                "items": "undo redo",
                "title": "Edit",
            },
            "format": {
                "items": "bold italic underline | formats",
                "title": "Format",
            },
            "insert": {"items": "hr", "title": "Insert"},
            "table": {
                "items": "",
                "title": "Table",
            },
            "tools": {
                "items": "code",
                "title": "Tools",
            },
            "view": {
                "items": "",
                "title": "View",
            },
        },
        "menubar": ["edit", "table", "format", "toolsview", "insert"],
        "toolbar": "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | plonelink  unlink | ",
        "plugins": [
            "hr",
            "lists",
            "nonbreaking",
            "noneditable",
            "pagebreak",
            "paste",
            "code",
            "link"
        ],
        "style_formats": [
            {
                "items": [
                    {"format": "h2", "title": "Header 2"},
                    {"format": "h3", "title": "Header 3"},
                    {"format": "h4", "title": "Header 4"},
                    {"format": "h5", "title": "Header 5"},
                    {"format": "h6", "title": "Header 6"},
                ],
                "title": "Headers",
            },
            {
                "items": [
                    {"format": "p", "title": "Paragraph"},
                    {"format": "blockquote", "title": "Blockquote"},
                    {"format": "div", "title": "Div"},
                    {"format": "pre", "title": "Pre"},
                ],
                "title": "Block",
            },
            {
                "items": [
                    {"format": "bold", "icon": "bold", "title": "Bold"},
                    {"format": "italic", "icon": "italic", "title": "Italic"},
                    {
                        "format": "underline",
                        "icon": "underline",
                        "title": "Underline",
                    },
                    {
                        "format": "strikethrough",
                        "icon": "strikethrough",
                        "title": "Strikethrough",
                    },
                    {
                        "format": "superscript",
                        "icon": "superscript",
                        "title": "Superscript",
                    },
                    {
                        "format": "subscript",
                        "icon": "subscript",
                        "title": "Subscript",
                    },
                    {"format": "code", "icon": "code", "title": "Code"},
                ],
                "title": "Inline",
            },
            {
                "items": [
                    {
                        "format": "alignleft",
                        "icon": "alignleft",
                        "title": "Left",
                    },
                    {
                        "format": "aligncenter",
                        "icon": "aligncenter",
                        "title": "Center",
                    },
                    {
                        "format": "alignright",
                        "icon": "alignright",
                        "title": "Right",
                    },
                    {
                        "format": "alignjustify",
                        "icon": "alignjustify",
                        "title": "Justify",
                    },
                ],
                "title": "Alignment",
            },
            {
                "items": [
                    {
                        "classes": "listing",
                        "selector": "table",
                        "title": "Listing",
                    }
                ],
                "title": "Tables",
            },
        ],
        "height": 300,
    
    }
} 

@provider(IContextAwareDefaultFactory)
def message_to(context=None):
    """Default factory for the to field."""
    request = getRequest()
    message_to = request.get('message_to', None)  # Get 'date' parameter from request
    if message_to and message_to != 'admin' and api.user.get(userid=message_to):
        # To do: DO we need to find/check user?
        # return as set?
        return {message_to}
    return None  # Fallback i

def filter_factory():
    if message_to():
        return False
    return True


class INotification(model.Schema):
    """ Marker interface and Dexterity Python Schema for Notification
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:
    # model.load('notification.xml')

    # directives.write_permission(message='cmf.ManagePortal')
    read_permission(message_type='cmf.ModifyPortalContent')
    write_permission(message_type='cmf.ModifyPortalContent')
    message_type = schema.Choice(
        title=_("Message type"),
        description=_("Select the type of message to display."),
        values=("info", "warning", "error", "basic"),
        required=True,
        default="info",
    )
    
    
    directives.widget(
        "message",
        RichTextFieldWidget,
        pattern_options=PATTERN_OPTIONS,
    )
    
    read_permission(message='cmf.ModifyPortalContent')
    write_permission(message='cmf.ModifyPortalContent')
    message = RichText(
        title=_("Message"),
        description=_("The message shown to the user. NOTE: You can use  '${}' variables (see below))"),
        required=True,
    )
    
    read_permission(user_filter='cmf.ModifyPortalContent')
    write_permission(user_filter='cmf.ModifyPortalContent')
    user_filter = schema.Bool(
        title=_("label_user_filter", default="Show to all"),
        defaultFactory=filter_factory,
        required=False,
    )
    
    read_permission( message_users='cmf.ModifyPortalContent')
    write_permission( message_users='cmf.ModifyPortalContent')
    message_users = schema.Set(
        title=_("label_notify_users", default="Notify users"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Users"),
        defaultFactory=message_to
    )
    
    read_permission(message_groups='cmf.ModifyPortalContent')
    write_permission(message_groups='cmf.ModifyPortalContent')
    message_groups = schema.Set(
        title=_("label_notify_groups", default="Choose Groups"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Groups"),
    )
    
    read_permission(additional_users='cmf.ModifyPortalContent')
    write_permission(additional_users='cmf.ModifyPortalContent')
    additional_users = schema.TextLine(
        title=_("Additional notification user(s)"),
        description=_("Use  '${}' variables list below (for example ${user_id} )"),
        required=False
    )

    read_permission(time_filter='cmf.ModifyPortalContent')
    write_permission(time_filter='cmf.ModifyPortalContent')
    time_filter = schema.Bool(
        title=_("label_time_filter", default="Show immidiately"),
        default=True,
        required=False, 
    )
    
    read_permission(relative_time='cmf.ModifyPortalContent')
    write_permission(relative_time='cmf.ModifyPortalContent')
    relative_time = schema.Time(
        title=_("Time of day"),
        description=_("(From) what time of day, hours:minutes)"),
        required=False, 
        
    )
    
    # directives.widget(
    #     "test",
    #     pattern_options= {"data-pat-depends": "condition: not time_filter" }
         
    # )
    # test = schema.Time(
    #     title=_("Test"),
    #     required=False,  
    # )
    
    read_permission(effective_date='cmf.ModifyPortalContent')
    write_permission(effective_date='cmf.ModifyPortalContent')
    effective_date = schema.Date(
        title=_("Specific date to show notification"),
        description=_("Effective date."), 
        required=False, 
    )    
    
    #Maybe a condition would be better ??
    #If so, it is possible to see who has not seen the Notification
    directives.mode(message_assigned='hidden')
    message_assigned = schema.List(
        title=_("Assigned to (who should see this)"),
        required=False,
        value_type=schema.TextLine(),
        default=[],
        missing_value=[]
    )
    
    directives.mode(show_title='hidden')
    show_title = schema.Bool(
        title=_("Show message type (Title)"),
        required=False,
    )
    
    
    # show_title = schema.Bool(
    #     title=_("Show message type Title)"),
    #     required=False,
    # )
    
    

@implementer(INotification)
class Notification(Item):
    """ Content-type class for INotification
    """
