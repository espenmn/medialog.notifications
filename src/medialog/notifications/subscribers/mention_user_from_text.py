# -*- coding: utf-8 -*-
from plone import api
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectAddedEvent
from plone.app.textfield import RichTextValue
from plone.dexterity.interfaces import IDexterityContent
from zope.schema import getFields
from plone.dexterity.utils import iterSchemata
from zope.schema import getFieldsInOrder



import re

MENTION_RE = re.compile(r'@([^\s@][^\s]*)')

def handler(obj, event):
    """ Event handler. Checks if user is mentioned in text.
    If so, a Notification is added
    """
    
    # Maybe find fields from control panel ?
    fields_to_check = ['text', 'body', 'full_explanation', 'notes', 'Description', 'description']
    found_usernames = set()
    notify_users = []
    # if IDexterityContent.providedBy(obj):
    #     schema = obj.getTypeInfo().lookupSchema()
    
    for field in fields_to_check:
        for schema in iterSchemata(obj):
            print('  %s' % schema)
            for field in getFieldsInOrder(schema):
                print('    %s\t%s' % field)                    
                if field in getFields(schema):
                    value = getattr(obj, field, '')
                    if isinstance(value, dict) and 'data' in value:  # RichText
                        value = value['data']
                    elif hasattr(value, 'output'):  # RichTextValue
                        value = value.output

                    if isinstance(value, str):
                        found_usernames.update(MENTION_RE.findall(value))
            
    if found_usernames:
        referenseid = obj.UID()
        referense_id = f"notification-{referenseid}"
        for username in found_usernames:
            if api.user.get(username=username):
                notify_users.append(username)
                
        portal = api.portal.get()                
        container =  portal.get('notifications', portal)

        # Now, create notification
        # make sure user is not 'mentioned again'
        # Check if it exist
        # IF not, add user to notificy users
        portal = api.portal.get()
        container = portal.get('notifications', portal)

        #  Use api.content.find to check if item with this ID exists in the container
        resulter = api.content.find(id=referense_id, path={'query': '/'.join(container.getPhysicalPath()), 'depth': 1})

        if resulter:
            objekt = resulter[0].getObject()

            # Avoid re-notifying existing users
            existing_notify_users = objekt.notify_users or []
            
            if notify_users != existing_notify_users:
                objekt.notify_users = notify_users,
                objekt.reindexObject()
        else:
            # Create new notification
            objekt = create_note(obj.Title(), referense_id, obj.absolute_url(), notify_users, container)
            
            
            
        #Probably need more permissions?
        # for user_id in notify_users:
        #     api.user.grant_roles(
        #         username=user_id,
        #         obj=object,
        #         roles=['Reader'],
        #     )                 


        # if isinstance(event, ObjectAddedEvent):
        #     # Do soemthing else
        
        # return True
        
        
def create_note(title, referense_id, url, notify_users, container):
    objekt = api.content.create(
                type='Notification',
                title=f'Mentions {title}',
                id=referense_id,
                message = RichTextValue(
                    f'You have been mentioned in a document that has been modified: <a href="{url}">Check here</a>',
                    'text/html',
                    'text/html'
                ),
                notification_type='mention',
                notify_users=notify_users,
                notification_assigned=[],
                container=container,
            )