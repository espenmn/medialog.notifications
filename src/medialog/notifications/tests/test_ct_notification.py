# -*- coding: utf-8 -*-
from medialog.notifications.content.notification import INotification  # NOQA E501
from medialog.notifications.testing import MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class NotificationIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_notification_schema(self):
        fti = queryUtility(IDexterityFTI, name='Notification')
        schema = fti.lookupSchema()
        self.assertEqual(INotification, schema)

    def test_ct_notification_fti(self):
        fti = queryUtility(IDexterityFTI, name='Notification')
        self.assertTrue(fti)

    def test_ct_notification_factory(self):
        fti = queryUtility(IDexterityFTI, name='Notification')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            INotification.providedBy(obj),
            u'INotification not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_notification_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Notification',
            id='notification',
        )

        self.assertTrue(
            INotification.providedBy(obj),
            u'INotification not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('notification', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('notification', parent.objectIds())

    def test_ct_notification_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Notification')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
