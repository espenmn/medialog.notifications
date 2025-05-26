# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from zope.interface import implementer
from zope.component import adapter
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode
from plone.restapi.services import Service
from plone import api

@implementer(IExpandableElement)
@adapter(Interface, Interface)
class MentionsView(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        if not expand:
            return {
                'mentions_view': {
                    '@id': f"{self.context.absolute_url()}/@mentions_view"
                }
            }

        users = api.user.get_users()
        return [
            {
                "key": safe_unicode(user.getProperty('fullname') or user.getUserName()),
                "value": user.getUserName()
            }
            for user in users
        ]



class MentionsViewGet(Service):

    # def reply(self):
    #     service_factory = MentionsView(self.context, self.request)
    #     return service_factory(expand=True)['mentions_view']
    
    def reply(self):
        service_factory = MentionsView(self.context, self.request)
        return service_factory(expand=True)  # ✅ already a list, no ['mentions_view']

