# -*- coding: utf-8 -*-
from plone import api
from plone.stringinterp.interfaces import IStringInterpolator
from datetime import datetime, timedelta   
from zope.lifecycleevent import ObjectAddedEvent


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
    

def handler(obj, event):
    """ Event handler
    """
    # NOTE: if you modify the Notificaion, users who have read the Noteification are re-added
    notify_users =  obj.notify_users or set()
    
    
    # add users from 'variable field'
    additional_users = getattr(obj, 'additional_users', None)
    if additional_users:
        interpolator = IStringInterpolator(obj)
        more_users = interpolator(additional_users)
        if type(more_users) == str:
            userlist = more_users.split(", ")
            for user in userlist:
                # Check if user exist
                if api.user.get(username=user):
                    notify_users.add(user)
    
    if obj.user_filter:
        #Add all users
        userlist = api.user.get_users()
        for user in userlist:
            notify_users.add(user.id)  
            
    notification_assigned =  get_users(notify_users).union(get_groups(obj.notify_groups or set()))
    
    for user_id in notification_assigned:
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
        

    obj.notification_assigned = list(notification_assigned)
    obj.effective_date= effective_date
    obj.reindexObject()
    #Maybe reindex just the fields? # return True
    