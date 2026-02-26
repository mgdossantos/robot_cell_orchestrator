# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from app.domain import CellContext,CellState
from app.services import VisionService, RobotDriver,Gripper
from app.orchestrator import Orchestrator
from fastapi import FastAPI
def main():
    # ctx = CellContext()
    # print(ctx.state)
    # print(ctx.cycles_ok)
    # print(ctx.last_error)
    # vsx = VisionService(0.3)
    # rbx = RobotDriver(0.1)
    #
    # for i in range(10):
    #     pose = vsx.get_pick_pose()
    #     if pose is None:
    #         print("Vision failed, skipping move")
    #         continue
    #
    #     ok = rbx.move_to(pose)
    #     print("Move OK?", ok)
    #
    #     g = Gripper(p_slip=0.3)
    #
    #     g.close()
    #     results = [g.has_part() for _ in range(20)]
    #     print(results)
    #
    #     g.open()
    #     print(g.has_part())  # deve ser sempre False

    # ctx = CellContext()
    #orch = Orchestrator(ctx, None, None, None)
    #
    # result = orch._fail("test_error")
    #
    # print(result)
    # print(ctx.state)
    # print(ctx.last_error)
    # print(ctx.cycles_failed)

    #ctx = CellContext()
    # robot = RobotDriver(p_fail=0.2)  # pra ver falhar às vezes
    # orch = Orchestrator(ctx, None, robot, None)
    #
    # for _ in range(5):
    #     print(orch.home(), ctx.state, ctx.last_error, ctx.robot_failures)

    ctx = CellContext()
    vision = VisionService(p_fail=0.3)
    robot = RobotDriver(p_fail=0.05)
    gripper = Gripper(p_slip=0.15)
    orch = Orchestrator(ctx, vision, robot, gripper)
    for _ in range(10):
        ctx.state = CellState.IDLE
        ctx.last_error = None
        ctx.has_part = False
        print(orch.run_cycle(), ctx.state, ctx.cycles_ok, ctx.cycles_failed)



if __name__ == '__main__':
    main()

