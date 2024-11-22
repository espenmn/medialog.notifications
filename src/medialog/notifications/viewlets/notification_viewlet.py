# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# import datetime
# from DateTime import DateTime
# from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from datetime import datetime
# import DateTime

# from zope.interface import alsoProvides


 

class NotificationViewlet(ViewletBase):
    
    template = ViewPageTemplateFile('notification-viewlet.pt')

    # def update(self):
    #     self.message = self.get_message()

    # #TO DO, cache (?)
    def get_user(self):
        user = api.user.get_current()
        user_id = user.getId()
        
        if user_id:
            return user.getProperty("fullname")
        
        #TO DO: What do we do for 'anon'?
        return 'anon'

    #TO DO, cache (?)
    def count_items(self):
        today = datetime.now()
        
        user = api.user.get_current()
        user_id = user.getId()
        items =  self.context.portal_catalog(portal_type=['Notification'], message_assigned=user_id, effective={"query": today, "range": "max"})
        
        
        if items:
            return len(items)
        
        return None
        
 
    # def index(self):
    #     return super(NotificationViewlet, self).render()
