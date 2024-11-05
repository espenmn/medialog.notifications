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


@indexer(INotification)  # ADJUST THIS!
# @indexer(IDexterityContainer)  # ADJUST THIS!
def message_usersIndexer(obj):
    """Calculate and return the value for the indexer"""
    # get all users of all groups
    # return all users
    users = []
    
    for entry in obj.message_users:
        #TO DO: very strange that this info is stored as string
        # Check if there is another vocabulary
        entrylist = entry.split(':')
        if entrylist[0] == 'group':
            groupmembers = api.user.get_users(groupname=entrylist[1])
            for groupmember in groupmembers:
                users.append(groupmember.getId())
                
        if entrylist[0] == 'user':
            users.append(entrylist[1])
    
    if users:
        return set(users)


 