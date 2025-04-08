# -*- coding: utf-8 -*-

# from medialog.notifications import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from DateTime import DateTime

from plone.app.contenttypes.browser.collection import CollectionView

class INotificationsView(Interface):
    """ Marker Interface for INotificationsView"""


class NotificationsCollectionView(CollectionView):
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
            return {'fullname':user.getProperty("fullname"), 'id': user_id}
        #TO DO: What do we do for 'anon'?
        return {'fullname': 'anon', 'id': None}
    
    @property
    def show_all(self):
        showall = self.request.get('show_all', 0)
        return showall

    #TO DO: Filter batch on  'read' / 'unread'         
    # def get_items(self):
    #     show_all = self.show_all
    #     user = api.user.get_current().getId() 
    #     today = DateTime()
        
    #     if not show_all:
    #         return self.context.portal_catalog(portal_type=['Notification'], notification_assigned=user, effective={"query": today, "range": "max"}, sort_on="created", sort_order="reverse")
    #     else:
    #         return self.context.portal_catalog(portal_type=['Notification'], notify_users=user, effective={"query": today, "range": "max"}, sort_on="created", sort_order="reverse")
        
        



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
            return {'fullname':user.getProperty("fullname"), 'id': user_id}
        #TO DO: What do we do for 'anon'?
        return {'fullname': 'anon', 'id': None}
    
    @property
    def show_all(self):
        showall = self.request.get('show_all', 0)
        return showall
        
    def get_items(self):
        show_all = self.show_all
        user = api.user.get_current().getId() 
        today = DateTime()
        
        if not show_all:
            return self.context.portal_catalog(portal_type=['Notification'], notification_assigned=user, effective={"query": today, "range": "max"}, sort_on="created", sort_order="reverse")
        else:
            return self.context.portal_catalog(portal_type=['Notification'], notify_users=user, effective={"query": today, "range": "max"}, sort_on="created", sort_order="reverse")
        
        