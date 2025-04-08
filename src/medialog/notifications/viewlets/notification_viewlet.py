# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import datetime

 

class NotificationViewlet(ViewletBase):
    
    def update(self):
        self.user = self.get_user()
        self.items = self.count_items()

    # #TO DO, cache (?)
    def get_user(self):
        user = api.user.get_current()
        user_id = user.getId()
        
        if user_id:
            return user.getProperty("fullname")
        
        #TO DO: What do we do for 'anon'?
        return 'anon'

    def count_items(self):
        today = datetime.now()        
        user = api.user.get_current()
        user_id = user.getId()
        items =  self.context.portal_catalog(portal_type=['Notification'], notification_assigned=user_id, effective={"query": today, "range": "max"})
                
        if items:
            return len(items)
        
        return None
        
 
    def index(self):
        return super(NotificationViewlet, self).render()


