# -*- coding: utf-8 -*-

# from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from medialog.notifications.content.notification import INotification


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(INotification)  # ADJUST THIS!
def message_assigned_indekser(obj):
    """Calculate and return the value for the indexer"""
    return obj.message_assigned
