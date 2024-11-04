# -*- coding: utf-8 -*-

# from medialog.notifications import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class INotificationView(Interface):
    """ Marker Interface for INotificationView"""


class NotificationView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('notification_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
