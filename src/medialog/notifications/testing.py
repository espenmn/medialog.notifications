# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import medialog.notifications


class MedialogNotificationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=medialog.notifications)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.notifications:default')


MEDIALOG_NOTIFICATIONS_FIXTURE = MedialogNotificationsLayer()


MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_NOTIFICATIONS_FIXTURE,),
    name='MedialogNotificationsLayer:IntegrationTesting',
)


MEDIALOG_NOTIFICATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_NOTIFICATIONS_FIXTURE,),
    name='MedialogNotificationsLayer:FunctionalTesting',
)


MEDIALOG_NOTIFICATIONS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MEDIALOG_NOTIFICATIONS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='MedialogNotificationsLayer:AcceptanceTesting',
)
