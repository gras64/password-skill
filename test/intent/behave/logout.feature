Feature: logout
    Scenario: user logout english
        Given an English speaking user
        When the user says "Goodbye"
        Then "password-skill" should reply with "bye"
        Then mycroft should send the message "skillmanager.deactivate"
    Scenario: user logout german
        Given an English speaking user
        When the user says "ausloggen"
        Then "password-skill" should reply with "Auf wiedersehen"
        Then mycroft should send the message "skillmanager.deactivate"