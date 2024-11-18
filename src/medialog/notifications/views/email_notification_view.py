# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface


class IEmailNotificationView(Interface):
    """ Marker Interface for IEmailNotificationView"""


class EmailNotificationView(BrowserView):
    def __call__(self):
        template = '''<li class="heading" i18n:translate="">
          Sample View
        </li>'''
        return template
