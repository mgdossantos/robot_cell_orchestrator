Feature: Pick operation

  Scenario: Vision fails and pick goes to ERROR
    Given the cell is in READY state
    And the vision always fails
    And the robot never fails
    And the gripper never slips
    When I execute a pick command
    Then the cell state should be ERROR
    And the error reason should be "vision_no_detection"
    And the vision failure counter should be incremented