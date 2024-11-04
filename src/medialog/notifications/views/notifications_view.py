# -*- coding: utf-8 -*-

# from medialog.notifications import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from Products.CMFCore.utils import getToolByName

def is_current_user_in_principals(context, principals):
    # Get the current user
    user = api.user.get_current()
    user_id = user.getId()
    
    # Get the groups tool
    portal_groups = getToolByName(context, 'portal_groups')
    
    # Check if the current user is in the selected principals
    if user_id in principals:
        return True
    
    # Check if the user is in any of the selected groups
    user_groups = portal_groups.getGroupsByUserId(user_id)
    user_group_ids = [group.getId() for group in user_groups]
    
    # If any selected principal matches a group the user is in, return True
    if any(group_id in principals for group_id in user_group_ids):
        return True


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
        #TO Do: search for 'principal'
        # Not filter in template
        # user = api.user.get_current()
        # user_id = user.getId()
        return self.context.portal_catalog(portal_type=['Notification'])
        
    # def batch(self):
    #     batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=40);
    #     return batch
        
