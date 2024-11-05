# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from plone.protect.utils import safeWrite


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
        userid = f'user:{user.id}'
        if userid in obj.message_users:
            safeWrite(obj, self.request)
            obj.message_users = obj.message_users.remove(userid)
            if obj.message_read == None:
                [userid]
            else:    
                obj.message_read.append(user.id)
        
        self.request.response.redirect(self.request.get_header("referer"))
        # return True

