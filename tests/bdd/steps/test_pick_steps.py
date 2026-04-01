# tests/steps/test_pick_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then

from app.domain import CellState

scenarios("../pick.feature")


@given("the cell is in READY state")
def cell_ready(ctx):
    ctx.state = CellState.READY


@given("the vision always fails")
def vision_always_fails(vision_always_fails):
    # Fixture already enforces p_fail=1.0
    return vision_always_fails

@given("the vision always succeeds")
def vision_always_succeeds_step(vision_always_succeeds, orch):
    orch.vision = vision_always_succeeds

@given("the robot never fails")
def robot_never_fails(robot_never_fails):
    # Fixture already enforces p_fail=0.0
    return robot_never_fails


@given("the gripper never slips")
def gripper_never_slips(gripper_never_slips):
    # Fixture already enforces p_slip=0.0
    return gripper_never_slips


@when("I execute a pick command")
def execute_pick(orch, ctx):
    # Save counter before
    ctx._vision_failures_before = ctx.vision_failures  # small helper for the scenario
    orch.pick()

@when("I execute a full cycle")
def execute_cycle(orch, ctx):
    ctx._cycles_ok_before = ctx.cycles_ok
    orch.run_cycle()

@then("the cell state should be ERROR")
def state_should_be_error(ctx):
    assert ctx.state == CellState.ERROR


@then('the error reason should be "vision_no_detection"')
def reason_should_be_vision_no_detection(ctx):
    assert ctx.last_error == "vision_no_detection"


@then("the vision failure counter should be incremented")
def vision_counter_incremented(ctx):
    assert ctx.vision_failures > ctx._vision_failures_before

@then("the cell state should be READY")
def state_should_be_ready(ctx):
    from app.domain import CellState
    assert ctx.state == CellState.READY

@then("the cycle counter should be incremented")
def cycle_counter_incremented(ctx):
    assert ctx.cycles_ok > ctx._cycles_ok_before

