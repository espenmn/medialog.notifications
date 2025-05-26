# mentioning_behavior.py
from zope.interface import Interface, implementer

class IMentioningBehavior(Interface):
    """Behavior interface"""

class IMentioningBehaviorMarker(Interface):
    """Marker interface applied to instances"""

@implementer(IMentioningBehavior)
class MentioningBehavior:
    def __init__(self, context):
        self.context = context
