# -*- coding: utf-8 -*-
from plone import api
from plone.stringinterp.interfaces import IStringInterpolator
from datetime import datetime, timedelta   
from zope.lifecycleevent import ObjectAddedEvent


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
    

def handler(obj, event):
    """ Event handler
    """
    # NOTE: if you modify the Notificaion, users who have read the Noteification are re-added
    message_users =  obj.message_users 
    
    
    # add users from 'variable field'
    if obj.additional_users:
        interpolator = IStringInterpolator(obj)
        more_users = interpolator(obj.additional_users)
        if type(more_users) == str:
            userlist = more_users.split(", ")
            for user in userlist:
                # Check if user exist
                if api.user.get(username=user):
                    message_users.add(user)
    
    if obj.user_filter:
        #Add all users
        userlist = api.user.get_users()
        for user in userlist:
            message_users.add(user.id)  
            
    message_assigned =  get_users(message_users).union(get_groups(obj.message_groups))
    
    for user_id in message_assigned:
        api.user.grant_roles(
            username=user_id,
            obj=obj,
            roles=['Reader'],
        )
    
                               
    
    time_filter= obj.time_filter
    if time_filter:
        # Publish it immidiately
        effective_date = None
    else:
        effective_date = obj.effective_date
    
    if not effective_date and not time_filter and obj.relative_time:
            relative_time = obj.relative_time
            effective_date = datetime.combine(datetime.now().date(), relative_time )
            if relative_time < datetime.now().time():
                effective_date = effective_date + timedelta(days=1)
        

    obj.message_assigned = list(message_assigned)
    obj.effective_date= effective_date
    obj.reindexObject()
    #Maybe reindex just the fields? # return True
    