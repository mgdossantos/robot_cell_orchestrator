# tests/conftest.py
import pytest

from app.domain import CellContext, CellState
from app.services import VisionService, RobotDriver, Gripper
from app.orchestrator import Orchestrator


@pytest.fixture
def ctx() -> CellContext:
    # Estado inicial padrão do teste pode ser sobrescrito no step
    return CellContext(state=CellState.READY)


@pytest.fixture
def vision_always_fails() -> VisionService:
    # p_fail=1.0 => sempre retorna None
    return VisionService(p_fail=1.0)


@pytest.fixture
def robot_never_fails() -> RobotDriver:
    # p_fail=0.0 => sempre retorna True
    return RobotDriver(p_fail=0.0)


@pytest.fixture
def gripper_never_slips() -> Gripper:
    # p_slip=0.0 => has_part() quase sempre True quando fechado
    # (na nossa implementação, 0.0 => nunca escorrega)
    return Gripper(p_slip=0.0)


@pytest.fixture
def orch(ctx: CellContext, vision_always_fails: VisionService, robot_never_fails: RobotDriver, gripper_never_slips: Gripper) -> Orchestrator:
    return Orchestrator(
        ctx=ctx,
        vision=vision_always_fails,
        robot=robot_never_fails,
        gripper=gripper_never_slips,
    )