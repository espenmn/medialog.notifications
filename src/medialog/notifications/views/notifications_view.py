# -*- coding: utf-8 -*-

# from medialog.notifications import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class INotificationsView(Interface):
    """ Marker Interface for INotificationsView"""


class NotificationsView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('notifications_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    
    #TO DO, cache (?)
    def get_items(self):
        return self.context.portal_catalog(portal_type=['Notification'])
        
    # def batch(self):
    #     batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=40);
    #     return batch
        
