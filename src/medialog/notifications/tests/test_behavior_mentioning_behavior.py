# -*- coding: utf-8 -*-
from medialog.notifications.behaviors.mentioning_behavior import IMentioningBehaviorMarker
from medialog.notifications.testing import MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class MentioningBehaviorIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_mentioning_behavior(self):
        behavior = getUtility(IBehavior, 'medialog.notifications.mentioning_behavior')
        self.assertEqual(
            behavior.marker,
            IMentioningBehaviorMarker,
        )
