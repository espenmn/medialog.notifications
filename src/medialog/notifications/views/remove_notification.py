# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from plone.protect.utils import safeWrite
import transaction

class IRemoveNotification(Interface):
    """ Marker Interface for IRemoveNotification"""


class RemoveNotification(BrowserView):
    
    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request
        

    def __call__(self):
        context = self.context
        user = api.user.get_current()
        item = self.request.get('item')
        obj  = api.content.get(UID=item) 
        if obj.message_read != None and user.id in obj.message_read:
            safeWrite(obj, self.request)
            readerlist = obj.message_read.remove(user.id)
            obj.message_read = readerlist or []
            obj.reindexObject('message_read')
            
        # if obj.message_read == None or obj.message_read == []:
        #     pass
        #     #delete object / redirect to delete page ??
            
        self.request.response.redirect(self.request.get_header("referer"))
        # return True
