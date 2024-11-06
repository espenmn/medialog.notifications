# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api

import datetime
from DateTime import DateTime


 

class NotificationViewlet(ViewletBase):

    # def update(self):
    #     self.message = self.get_message()


    #TO DO, cache (?)
    def count_items(self):
        today = DateTime()
        
        user = api.user.get_current()
        user_id = user.getId()
        items =  self.context.portal_catalog(portal_type=['Notification'], assigned_to=user_id, effective={"query": today, "range": "max"})
        
        
        if items:
            return len(items)
        
        return None
        
 
    def index(self):
        return super(NotificationViewlet, self).render()
