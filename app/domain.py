from enum import Enum
from dataclasses import dataclass

class CellState(str,Enum):
    IDLE = "idle"
    HOMING = "homing"
    READY = "ready"
    PICKING = "picking"
    PLACING = "placing"
    ERROR= "error"
    RECOVERING = "recovering"

@dataclass
class Pose:
    x :float
    y : float
    theta :float

@dataclass
class CellContext:
    state :CellState =CellState.IDLE
    last_error: str = None
    cycles_ok : int  = 0
    cycles_failed: int = 0
    vision_failures:int =0
    robot_failures:int = 0
    gripper_failures: int =0

    has_part: bool = False