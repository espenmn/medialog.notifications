from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from Products.statusmessages.interfaces import IStatusMessage
from zope import schema
from plone.autoform import directives
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from datetime import datetime, timedelta   
from plone import api
from plone.app.textfield import RichText, RichTextValue
from plone.app.z3cform.widget import RichTextFieldWidget 
from plone.stringinterp.interfaces import IStringInterpolator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# from plone.supermodel.directives import fieldset

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

class INotifyAddAction(Interface):
    """Interface for the configurable aspects of a notify action.
    This is also used to create add and edit forms, below.
    """
    
        
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
    
   # fieldset('date',
    #     label=u'Dates',
    #     fields=['relative_time', 'effective_date']
    # ) 
    
    
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
        # request = self.context.REQUEST
        portal = api.portal.get()
        obj = self.event.object
        interpolator = IStringInterpolator(obj)
        message = interpolator(self.element.message.raw)
        message_type = self.element.message_type
        message_users = self.element.message_users
        time_filter =  self.element.time_filter 
        if time_filter:
            effective_date = None
        else:
            effective_date = self.element.effective_date
        show_title =  self.element.show_title
        
        if not effective_date and not time_filter and self.element.relative_time:
            # today_date = datetime.now().date()
            relative_time = self.element.relative_time
            effective_date = datetime.combine(datetime.now().date(), relative_time )
            if relative_time < datetime.now().time():
                effective_date = effective_date + timedelta(days=1)
        
        container =  portal.get('notifications', portal)
            
        
        # add users from 'variable field'
        if self.element.additional_users:
            more_users = interpolator(self.element.additional_users)
            if type(more_users) == str:
                userlist = more_users.split(", ")
                for user in userlist:
                    # Check if user exist
                    if api.user.get(username=user):
                        message_users.add(f"user:{user}")
                        
        if self.element.user_filter:
            userlist = api.user.get_users()
            for user in userlist:
                message_users.add(f"user:{user}")
            
        
        #TO DO: Should we both add notify or should be just save it.
        obj = api.content.create(
            type='Notification',
            title='Notification',
            # message = message, 
            message  = RichTextValue(message),
            message_type = message_type,
            show_title =  show_title,
            message_users = message_users,
            message_assigned = [],
            effective_date = effective_date,
            container=container
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
    form = NotifyAddEditForm