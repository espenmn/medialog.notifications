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
import os
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.file import NamedBlobFile

from plone.base.interfaces import constrains
from plone.base.interfaces.constrains import IConstrainTypes
from plone.base.interfaces.constrains import ISelectableConstrainTypes

import pandas as pd
import openpyxl
from zope.lifecycleevent import modified
import plone.api
from zope.component.hooks import setSite

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
        )
        
        plone.api.content.transition(obj=portal['notifications'], transition='publish')
        
        #note_folder = portal.get('notifications', False)
        behaviour = constrains.ISelectableConstrainTypes(note_folder)
        behaviour.setConstrainTypesMode(constrains.ENABLED)
        behaviour.setImmediatelyAddableTypes(['Notification'])
        behaviour.setLocallyAllowedTypes(['Notification'])

        #That is probably all
            
            