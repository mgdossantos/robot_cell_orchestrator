
from dataclasses import dataclass
import random,time
from app.domain import Pose

class VisionService:
    def __init__(self,p_fail:float=0.30):
        self.p_fail = p_fail

    def get_pick_pose(self):
        time.sleep(0.02)
        if random.random() < self.p_fail:
            return None
        else:
            x = round(random.uniform(0.10, 0.40), 3)
            y = round(random.uniform(-0.20, 0.20), 3)
            theta = round(random.uniform(-3.14, 3.14), 3)

            return Pose(x=x, y=y, theta=theta)


class RobotDriver:
    def __init__(self,p_fail:float=0.5):
        self.p_fail=p_fail


    def home(self):
        time.sleep(0.05)
        if random.random() < self.p_fail:
            return False
        return True

    def move_to(self,pose:Pose):

        time.sleep(0.05)
        if random.random() < self.p_fail:
            return False
        return True



class Gripper:
    def __init__(self,p_slip:float=0.15):
        self.p_slip=p_slip
        self._closed:bool= False


    def open(self):
        time.sleep(0.02)
        self._closed= False


    def close(self):
        time.sleep(0.02)
        self._closed= True

    def has_part(self):
        # Se está aberto, não tem peça
        if not self._closed:
            return False

        # Se está fechado, a peça pode escorregar
        if random.random() < self.p_slip:
            return False

        return True