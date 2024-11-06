# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api
 

class NotificationViewlet(ViewletBase):

    # def update(self):
    #     self.message = self.get_message()


    #TO DO, cache (?)
    def count_items(self):
        user = api.user.get_current()
        user_id = user.getId()
        items =  self.context.portal_catalog(portal_type=['Notification'], message_read=user_id)
        
        if items:
            return len(items)
        
        return None
        
 
    def index(self):
        return super(NotificationViewlet, self).render()
