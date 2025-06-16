# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface

from zope.interface import Interface
from Acquisition import aq_inner
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IMailSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import adapter, getUtility
from zope.interface.interfaces import ComponentLookupError
from zope.interface import implementer, Interface
from plone import api
# from datetime import datetime
from DateTime import DateTime
from plone.protect.utils import safeWrite


class IEmailNotificationView(Interface):
    """ Marker Interface for IEmailNotificationView"""


class EmailNotificationView(BrowserView):
    def __call__(self):
        #1 check login ?
        #2 check new notifications
        #3 maybe store the date, alternatively run this once a day
        #4 Find/Batch 'notification users' ?
        #5 Send email
        #6 Should email be just 'reminder' or should it include the notifications in the email?      
        #now = datetime.now()
        # import logging
        # logger = logging.getLogger(__file__)
        
        registry = getUtility(IRegistry)
        self.mail_settings = registry.forInterface(IMailSchema, prefix="plone")
        
        self.mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not self.mailhost:
            raise ComponentLookupError(
                "You must have a Mailhost utility to \
            execute this action"
            )

        self.email_charset = self.mail_settings.email_charset
        
        # To do 'check on date = last 24 hours
        # Is it best to loop users or loop notifications?
        for user in  api.user.get_users():
          brains = self.context.portal_catalog(portal_type=['Notification'], notification_assigned = user.id, effective = {'query': [DateTime() - 1], 'range': 'min'}  # Last 24 hours
)
          
          messages = ''
          count = 0

          if brains:
            for brain in brains:
              count += 1
              messages +=  brain.getObject().message.output
              messages += '<p>----------------------</p>'
              # Alternatively, just add the type and date ??
              
            messagetext = f"""<div class="notification-viewlet portalMessage statusmessage statusmessage-info alert alert-info">
                      <a title="see noticitions" href="{api.portal.get().absolute_url()}/notifications">
                           You have <b>{count}</b> new notification(s). <b>Click to see</b></a>
                  </div>""" + messages
 
          
           
            self.send_mail(user, messagetext)
        
        #4 Update date in registry?
            
        return  True
                            
      
    def send_mail(self, user, message):
      # interpolator = IStringInterpolator(object)
      self.recipients = user.getProperty('email')
                        
      if self.recipients:
          # print('sending mail')
          # TO DO use plona.api to send email ?        
          
          api.portal.send_email(
                recipient       = self.recipients,
                subject         = "Messages",
                body            = MIMEText(message, 'html', _charset='UTF-8')
          )         
          # melding = message
          # message = f"\n{interpolator(melding)!s}"
          # outer = MIMEMultipart('alternative')
          # outer['To'] = self.recipients
          # outer['From'] = self.mail_settings.email_from_address
          # outer['Subject'] =  "You got messages"
          # outer.epilogue = ''
          # html_text = MIMEText(message, 'html', _charset='UTF-8')
          # self.mailhost.send(outer.as_string())
          # Finally send mail.
         
         



#interpolator = IStringInterpolator(obj)
