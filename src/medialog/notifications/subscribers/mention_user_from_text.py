# -*- coding: utf-8 -*-
from plone import api
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectAddedEvent
from plone.dexterity.interfaces import IDexterityContent
from plone.app.textfield import RichTextValue

import re

MENTION_RE = re.compile(r'@([\w\-]+)')

def handler(obj, event):
    """ Event handler. Checks if user is mentioned in text.
    If so, a Notification is added
    """
    
    import pdb; pdb.set_trace()
 
    # Maybe find fields from control panel ?
    fields_to_check = ['text', 'description']
    found_usernames = set()
    notify_users = set()

    for field in fields_to_check:
        value = getattr(obj, field, '')
        if isinstance(value, dict) and 'data' in value:  # RichText
            value = value['data']
        elif hasattr(value, 'output'):  # RichTextValue
            value = value.output

        if isinstance(value, str):
            found_usernames.update(MENTION_RE.findall(value))

    # You can either store them in a custom field, annotation, or print them
    # For demonstration, we'll log them
    if found_usernames:
        for user in found_usernames:
            if api.user.get(username=user):
                notify_users.add(user)
                
        portal = api.portal.get()                
        container =  portal.get('notifications', portal)

        # Now, create notification
        # TO DO, make sure user is not 'mentioned again'
        
        obj = api.content.create(
            type='Notification',
            title='Mentions',
            message  = RichTextValue('You have been mentioned'),
            notification_type = 'info',
            notify_users = notify_users,
            notification_assigned = [],
            container=container,
        )
        
        #Probably need more permissions?
        for user_id in notify_users:
            api.user.grant_roles(
                username=user_id,
                obj=obj,
                roles=['Reader'],
            )                 


        # if isinstance(event, ObjectAddedEvent):
        #     # Do soemthing else