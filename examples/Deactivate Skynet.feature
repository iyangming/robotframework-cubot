Feature: Deactivate Skynet
    In order to save the world
    As a rebel leader I want Skynet be deactivated 

    Scenario: Should deactivate Skynet
        Given Skynet is available
        When SkyNet is deactivated
        Then Skynet is inactive
