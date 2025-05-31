# mentioning_behavior.py
from zope.interface import Interface, implementer
from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from plone.supermodel import model

# class IMentioningBehavior(Interface):
#    """Behavior interface"""
    
    
@provider(IFormFieldProvider)
class IMentioningBehavior(model.Schema):
    """Behavior interface with a schema.List field."""

    # form.mode(mentioned_users="hidden")
    mentioned_users = schema.List(
        title=u"Mentioned Users",
        value_type=schema.TextLine(),
        required=False,
        default=[]
    )
    
    # form.mode(reference_uid ="hidden")
    reference_id = schema.TextLine(
        title=u"Reference UID",
        required=False,
    )

class IMentioningBehaviorMarker(Interface):
    """Marker interface applied to instances"""

@implementer(IMentioningBehavior)
class MentioningBehavior:
    def __init__(self, context):
        self.context = context
        
 