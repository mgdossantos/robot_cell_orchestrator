from app.services import VisionService, RobotDriver,Gripper
from app.domain import CellContext, CellState,Pose

class Orchestrator ():
    def __init__(self,ctx:CellContext,vision,robot,gripper):
        self.ctx= ctx
        self.vision = vision
        self.robot=robot
        self.gripper = gripper
    def _fail(self,reason:str)->dict:
        self.ctx.state = CellState.ERROR
        self.ctx.last_error = reason
        self.ctx.cycles_failed+=1

        return{
            "ok": False,
            "reason": reason,
            "state": self.ctx.state
        }
    def home(self):
        if self.ctx.state== CellState.PICKING or CellState.PLACING:
            self._fail("cannot_home_while_busy")
        self.ctx.state = CellState.HOMING

        ok=self.robot.home()
        if not ok:
            self.ctx.robot_failures+=1
            return (self._fail("robot home failed"))
        self.ctx.state = CellState.READY
        self.ctx.last_error = None
        return{
            "ok": True,
            "state": self.ctx.state
        }
    def pick(self,max_vision_retries:int = 2):
        if self.ctx.state != CellState.READY:
            return {"ok": False, "reason": "not_ready", "state": self.ctx.state}
        self.ctx.state = CellState.PICKING


        pose = None
        for _ in range(max_vision_retries + 1):
            pose = self.vision.get_pick_pose()
            if pose is not None:
                break
            self.ctx.vision_failures += 1

        if pose is None:
            return self._fail("vision_no_detection")

        if not self.robot.move_to(pose):
            self.ctx.robot_failures+=1
            return self._fail("robot_move_failed")

        # fechar gripper e verificar peça
        self.gripper.close()
        self.ctx.has_part = self.gripper.has_part()

        if not self.ctx.has_part:
            self.ctx.gripper_failures += 1
            return self._fail("grip_failed")

        # sucesso: volta pra READY
        self.ctx.state = CellState.READY
        self.ctx.last_error = None

        return {"ok": True, "state": self.ctx.state, "picked_pose": pose}
    def place(self,place_pose:Pose=Pose(0.5,0.0,0.0)):
        if self.ctx.state != CellState.READY:
            return(self._fail("not_ready"))

        if self.ctx.has_part:
            self.ctx.state = CellState.PLACING
        else:
            return(self._fail("no_part_to_place"))

        if not self.robot.move_to(place_pose):
            self.ctx.robot_failures+=1
            return self._fail("robot_move_failed")

        # abrir gripper e verificar peça
        self.gripper.open()
        self.ctx.has_part = False
        # sucesso: volta pra READY
        self.ctx.state = CellState.READY
        self.ctx.cycles_ok+=1

        return {"ok": True, "state": self.ctx.state, "placed_pose": place_pose}

    def run_cycle(self, max_vision_retries: int = 2):
        if self.ctx.state == CellState.IDLE:
            r_home=self.home()
            if not r_home.get("ok", False):
                return r_home
        if self.ctx.state!=CellState.READY:
            return {"ok": False, "reason": "not_ready_for_cycle", "state": self.ctx.state}
        r_pick=self.pick()
        if not r_pick.get("ok",False):
            return r_pick

        r_place = self.place()
        return r_place

    def reset(self) -> dict:
        self.ctx.state = CellState.IDLE
        self.ctx.last_error = None
        self.ctx.has_part = False
        return {"ok": True, "state": self.ctx.state}
