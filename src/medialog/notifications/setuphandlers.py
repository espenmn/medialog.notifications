# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone.base.interfaces import constrains
from plone.base.interfaces.constrains import IConstrainTypes
from plone.base.interfaces.constrains import ISelectableConstrainTypes

import plone.api

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
#from plone import api
# import os

import plone.api
# from zope.component.hooks import setSite

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "medialog.notifications:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["medialog.notifications.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = plone.api.portal.get()
    
    # portal_memberdata = getToolByName(portal, "portal_memberdata")
    # if not portal_memberdata.hasProperty("notifications"):
    #     portal_memberdata.manage_addProperty(id="notifications", value="", type="string")

    _create_content(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def _create_content(portal):
        
    if not portal.get('notifications', False):
        note_folder = plone.api.content.create(
            type='Folder',
            container=portal,
            id='notifications',
            title='Notifications',
            exclude_from_nav=True,
            default_page='notifications-collection',
        )
        
        if not note_folder.get('notifications-collection', False):
            notification_collection = plone.api.content.create(
                type='Collection',
                container=note_folder,
                id='notifications-collection',
                title='Notifications',
                layout='notifications-collection-view',
                query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Notification']},
                         {'i': 'notification_assigned', 'o': 'plone.app.querystring.operation.string.currentUser', 'v': ''}, 
                         ],
                limit=2000,
                item_count=500,
            )
        
        
        
        # Dont publish folder, it should not be possible to show other peoples notes
        # plone.api.content.transition(obj=portal['notifications'], transition='publish')
        
        #note_folder = portal.get('notifications', False)
        behaviour = constrains.ISelectableConstrainTypes(note_folder)
        behaviour.setConstrainTypesMode(constrains.ENABLED)
        behaviour.setImmediatelyAddableTypes(['Notification'])
        behaviour.setLocallyAllowedTypes(['Notification'])

        #That is probably all
            
            