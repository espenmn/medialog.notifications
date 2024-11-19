# from plone.app.users.browser.account import AccountPanelForm
# from plone.app.users.browser.account import AccountPanelSchemaAdapter
# from plone.base import PloneMessageFactory as _
# from Products.CMFCore.utils import getToolByName
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# from zope.interface import Interface
# from zope.schema import Choice
# rom  plone.app.users.browser import personalpreferences
# from  plone.app.users.browser.personalpreferences import PersonalPreferencesPanel, IPersonalPreferences
# from zope import schema
 

# class ICPersonalPreferences(schema):
#     """Provide schema for personalize form."""

#     wysiwyg_editor = Choice(
#         title=_("label_wysiwyg_editor", default="Wysiwyg editor"),
#         description=_("help_wysiwyg_editor", default="Wysiwyg editor to use."),
#         vocabulary="plone.app.vocabularies.AvailableEditors",
#         required=False,
#     )

#     language = Choice(
#         title=_("label_laxe", default="Laxe"),
#         description=_("help_preferred_language", "Your preferred language."),
#         vocabulary="plone.app.vocabularies.AvailableContentLanguages",
#         required=False,
#     )
    
 

# class PersonalPreferencesPanelAdapter(AccountPanelSchemaAdapter):
#      schema = ICPersonalPreferences


# class PersonalPreferencesPanel(AccountPanelForm):
#     """Implementation of personalize form that uses z3c.form."""

#     form_name = _("legend_personal_details", "Personal Details")
#     schema = ICPersonalPreferences

   


# class PersonalPreferencesConfiglet(PersonalPreferencesPanel):
#     """Control panel version of the personal preferences panel"""

#     template = ViewPageTemplateFile("account-configlet.pt")
    
#     tab = "userprefsx"