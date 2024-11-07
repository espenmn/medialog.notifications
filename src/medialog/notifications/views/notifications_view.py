# -*- coding: utf-8 -*-

# from medialog.notifications import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from DateTime import DateTime
 

class INotificationsView(Interface):
    """ Marker Interface for INotificationsView"""


class NotificationsView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('notifications_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    # #TO DO, cache (?)
    def get_user(self):
        user = api.user.get_current()
        user_id = user.getId()
        
        if user_id:
            return user_id
        
        #TO DO: What do we do for 'anon'?
        return 'anon'
    
        
    
    #TO DO, cache (?)
    def get_items(self):
        user = self.get_user()
        # Not filter in template
        #user = api.user.get_current()
        today = DateTime()
        
        return self.context.portal_catalog(portal_type=['Notification'], message_assigned=user, effective={"query": today, "range": "max"}, sort_on="created", sort_order="reverse")
        
        