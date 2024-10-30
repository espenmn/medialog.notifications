# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s medialog.notifications -t test_notification.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src medialog.notifications.testing.MEDIALOG_NOTIFICATIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/medialog/notifications/tests/robot/test_notification.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Notification
  Given a logged-in site administrator
    and an add Notification form
   When I type 'My Notification' into the title field
    and I submit the form
   Then a Notification with the title 'My Notification' has been created

Scenario: As a site administrator I can view a Notification
  Given a logged-in site administrator
    and a Notification 'My Notification'
   When I go to the Notification view
   Then I can see the Notification title 'My Notification'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Notification form
  Go To  ${PLONE_URL}/++add++Notification

a Notification 'My Notification'
  Create content  type=Notification  id=my-notification  title=My Notification

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Notification view
  Go To  ${PLONE_URL}/my-notification
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Notification with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Notification title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
