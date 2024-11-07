# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapter
from plone.stringinterp.adapters import BaseSubstitution
# from plone import api


@adapter(Interface)
class NotificationTo(BaseSubstitution):
    category = "Users"
    description = "Notification To"

    def safe_call(self):
        if hasattr(self.context, 'message_assigned'):
            return ", ".join(self.context.message_assigned)
        return ''



