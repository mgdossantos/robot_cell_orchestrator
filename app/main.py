from fastapi import FastAPI

from app.domain import CellContext
from app.services import VisionService, RobotDriver, Gripper
from app.orchestrator import Orchestrator

app = FastAPI()

# instâncias (injeção de dependência simples)
ctx = CellContext()
vision = VisionService()
robot = RobotDriver()
gripper = Gripper()

orch = Orchestrator(ctx, vision, robot, gripper)
@app.get("/health")
def health():
    return{
        "status": "ok"
    }

@app.get("/state")
def state():
    return ctx.__dict__

@app.post("/run_cycle")
def run_cycle():
    return orch.run_cycle()

@app.post("/home")
def home():
    return orch.home()

@app.post("/reset")
def reset():
    return orch.reset()

@app.post("/pick")
def pick():
    return orch.pick()


@app.post("/place")
def place():
    return orch.place()

