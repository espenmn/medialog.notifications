# -*- coding: utf-8 -*-

# from medialog.notifications import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class INotificationsView(Interface):
    """ Marker Interface for INotificationsView"""


class NotificationsView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('notifications_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
