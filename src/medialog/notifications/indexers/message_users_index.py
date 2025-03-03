# -*- coding: utf-8 -*-

# from plone.app.contenttypes.interfaces import IDocument
from medialog.notifications.content.notification import INotification
# from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from plone import api


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not be indexed here!')




def get_groups(message_groups):
    users = []
    for entry in message_groups:
        groupmembers = api.user.get_users(groupname=entry)
        for groupmember in groupmembers:
            users.append(groupmember.getId())
    
    return set(users)
                

def get_users(message_users):
    users = []
    for entry in message_users:
        users.append(entry)
          
    return set(users)
    

@indexer(INotification)  # ADJUST THIS!
def message_usersIndexer(obj):
    """Calculate and return the value for the indexer"""
    # get all users of all groups
    # return all users
    users = []
    
    if obj.message_users:
        for entry in obj.message_users:
            users.append(entry)
    
    if obj.message_groups:
        for entry in obj.message_groups:
            groupmembers = api.user.get_users(groupname=entry)
            for groupmember in groupmembers:
                users.append(groupmember.getId())
        
    if users:
        return set(users)
    
    