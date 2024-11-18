# # -*- coding: utf-8 -*-
# from plone.supermodel import model
# from zope import schema
# from zope.component import adapts
# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
# from zope.interface import Interface
# from plone.app.users.userdataschema import UserDataPanel
 
# # from medialog.notifications import _

# class IEnhancedUserDataSchema(model.Schema):
#     notifications = schema.TextLine(
#         title=('label_notifications', default=u'Notifications Setting'),
#         description=('help_notifications',
#                       default=u"When do you want notifications"),
#         required=False,
#         )
    

# class UserDataPanelExtender(extensible.FormExtender):
#     adapts(Interface, IDefaultBrowserLayer, UserDataPanel)
#     def update(self):
#         fields = field.Fields(IEnhancedUserDataSchema)
#         fields = fields.omit('accept') # Users have already accepted.
#         self.add(fields)