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


def get_groups(notify_groups):
    users = []
    for entry in notify_groups:
        groupmembers = api.user.get_users(groupname=entry)
        for groupmember in groupmembers:
            users.append(groupmember.getId())
    
    return set(users)
                

def get_users(notify_users):
    users = []
    for entry in notify_users:
        users.append(entry)
          
    return set(users)
    

@indexer(INotification)  # ADJUST THIS!
def notify_usersIndexer(obj):
    """Calculate and return the value for the indexer"""
    # get all users of all groups
    # return all users
    users = []
    
    if obj.notify_users:
        for entry in obj.notify_users:
            users.append(entry)
    
    if obj.notify_groups:
        for entry in obj.notify_groups:
            groupmembers = api.user.get_users(groupname=entry)
            for groupmember in groupmembers:
                users.append(groupmember.getId())
        
    if users:
        return users
        # import pdb; pdb.set_trace()
        # #res = [x for sublist in users for x in sublist]  
        # userset = set(users)
        # list(userset)
        # return list(set(users))
    