# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

# TO DO, should probably be 'PATCH'

@implementer(IExpandableElement)
@adapter(Interface, Interface)
class RemoveNotification(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        # result = {
        #     'remove_notification': {
        #         '@id': '{}/@remove_notification'.format(
        #             self.context.absolute_url(),
        #         ),
        #     },
        # }
        
        #TO DO: Probably remove this part and above
        # if not expand:
        #     return result

        
        # TO DO: Not sure why / if we should use try
        try:
            user = api.user.get_current()
            self.context.message_users = self.context.message_users.remove(user)
            # TO DO: How can we refresh page
            return True
        except Exception as e:
            print(e)
            return False
             
        
        
        # return True


class RemoveNotificationGet(Service):

    def reply(self):
        service_factory = RemoveNotification(self.context, self.request)
        return service_factory(expand=True)['remove_notification']
