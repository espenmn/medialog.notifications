# -*- coding: utf-8 -*-
from plone import api


def handler(obj, event):
    """ Event handler
    """
    #TO DO
    # Add all users to 'read field'
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
    
    userset =  set(users)


    obj.assigned_to = list(userset)
    # import pdb; pdb.set_trace()
    # obj.reindexObject('assigned_to')
    
    # return True
    