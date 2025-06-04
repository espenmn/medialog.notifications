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
            
    if found_usernames:
        referenceid = obj.UID()
        reference_id = f"notification-{referenceid}"
        for username in found_usernames:
            if api.user.get(username=username):
                notify_users.add(username)
                
        portal = api.portal.get()                
        container =  portal.get('notifications', portal)

        # Now, create notification
        # make sure user is not 'mentioned again'
        # Check if it exist
        # IF not, add user to notificy users
        portal = api.portal.get()
        container = portal.get('notifications', portal)

        #  Use api.content.find to check if item with this ID exists in the container
        results = api.content.find(id=reference_id, path={'query': '/'.join(container.getPhysicalPath()), 'depth': 1})

        if results:
            object = results[0].getObject()

            # Avoid re-notifying existing users
            existing_notify_users = set(object.notify_users or [])
            new_notify_users = notify_users - existing_notify_users

            if new_notify_users:
                object.notify_users = list(notify_users),
                object.reindexObject()
        else:
            # Create new notification
            object = api.content.create(
                type='Notification',
                title=f'Mentions{obj.Title()}',
                id=reference_id,
                message = RichTextValue(
                    f'You have been mentioned in a document that has been modified: <a href="{obj.absolute_url()}">Check here</a>',
                    'text/html',
                    'text/html'
                ),
                notification_type='info',
                notify_users=list(notify_users),
                notification_assigned=[],
                container=container,
            )
            
            
        
        
        #obj = api.content.create(
        #    type='Notification',
        #    title='Mentions',
        #    id=c,
        #    message  = RichTextValue('You have been mentioned'),
        #    notification_type = 'info',
        ##    notify_users = notify_users,
        #    notification_assigned = [],
        #    container=container,
        #)
        
        
        
        #Probably need more permissions?
        for user_id in notify_users:
            api.user.grant_roles(
                username=user_id,
                obj=object,
                roles=['Reader'],
            )                 


        # if isinstance(event, ObjectAddedEvent):
        #     # Do soemthing else