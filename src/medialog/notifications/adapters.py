# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapter
from plone.stringinterp.adapters import BaseSubstitution
# from plone import api


@adapter(Interface)
class NotificationTo(BaseSubstitution):
    category = "Users"
    description = "Notification To"

    def safe_call(self):
        if hasattr(self.context, 'message_assigned'):
            return ", ".join(self.context.message_assigned)
        return ''


# # testing adding personal settings
# from plone.app.users.browser.personalpreferences import IPersonalPreferences
# from zope.interface import Interface
# from zope import schema


# class IEnhancedUserDataSchema(IPersonalPreferences):
#     """ Use all the fields from the default user data schema, and add various
#     extra fields.
#     """

#     buttonsEnabled = schema.Bool(title=u'Transition button widget.', 
#                                 default=True,
#                                 description=u'Uncheck to remove the transition button box from ALL pages.',
#                                 required=False
#                                 )  
    
    
# from plone.app.users.browser.personalpreferences import PersonalPreferencesPanelAdapter
# from zope.interface import implementer

# @implementer(IEnhancedUserDataSchema)
# class EnhancedUserDataPanelAdapter(PersonalPreferencesPanelAdapter):
#     """
#     """
    

#     def get_buttonEnabled(self):
#         return self.context.getProperty('buttonsEnabled', '')
#     def set_buttonsEnabled(self, value):
#         return self.context.setMemberProperties({'buttonsEnabled': value})
#     buttonsEnabled = property(get_buttonEnabled, set_buttonsEnabled)
