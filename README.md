# Robot Cell Orchestrator (FastAPI)

This project implements a simplified backend orchestration layer for an industrial robotic cell.
It simulates vision detection, robot motion, and gripper behavior, and exposes a REST API using
FastAPI to execute and monitor pick-and-place cycles.

The goal of the project is to demonstrate backend design, state-machine-driven orchestration,
and fault handling for robotic systems without relying on real hardware.

---

## Motivation

Robotic systems are inherently complex and failure-prone. This project was created to showcase
how software engineering principles such as explicit state management, separation of concerns,
and centralized error handling can be applied to robotics backends.

The focus of this repository is not real-time control, but rather:
- Backend orchestration logic
- Clear state transitions
- Robust handling of failures
- API-driven control of robotic operations

---

## Architecture Overview

The system is organized into four main layers:

- **Domain**  
  Core data structures and state definitions.

- **Services**  
  Simulated external systems such as vision, robot motion, and gripper control.

- **Orchestrator**  
  The central state machine responsible for coordinating operations and enforcing valid behavior.

- **API (FastAPI)**  
  A REST interface used to control and monitor the robotic cell.

High-level flow:

Vision → Robot → Gripper  
↳ Controlled by Orchestrator  
↳ Exposed via FastAPI endpoints

---

## Project Structure

```
app/
├── __init__.py
├── domain.py        # State definitions, Pose, and CellContext
├── services.py      # VisionService, RobotDriver, Gripper (simulated hardware)
├── orchestrator.py  # State machine and orchestration logic
└── main.py          # FastAPI application and HTTP endpoints
```

---

## Domain Model

The robotic cell is modeled as an explicit state machine with the following states:

- IDLE
- HOMING
- READY
- PICKING
- PLACING
- ERROR

All runtime information is stored in a single `CellContext` object, including:
- current cell state
- last error reason
- successful and failed cycle counters
- vision, robot, and gripper failure counters
- whether the gripper is currently holding a part

This explicit model improves traceability, debuggability, and testability.

---

## Services (Simulated Hardware)

The system includes lightweight simulations of external components:

- **VisionService**
  - Returns a pick pose or `None`
  - Supports probabilistic failures
  - Used with retry logic at the orchestration layer

- **RobotDriver**
  - Simulates `home()` and `move_to(pose)`
  - Includes probabilistic motion failures

- **Gripper**
  - Maintains open/closed state
  - Simulates part slipping when closed
  - Provides a `has_part()` sensor abstraction

Each service is intentionally simple to keep the focus on orchestration logic.

---

## Orchestration Logic

The `Orchestrator` class is responsible for coordinating all operations.

Key responsibilities:
- Enforce valid commands based on the current state
- Execute retries for vision detection
- Handle robot and gripper failures consistently
- Update system metrics and state transitions
- Centralize error handling

Supported operations:
- `home()`
- `pick()`
- `place()`
- `run_cycle()` (home → pick → place)
- `reset()`

---

## Failure Handling Strategy

Failures are handled centrally by the orchestrator.

- Hardware-related failures transition the system to the ERROR state
- Failure counters are incremented for traceability
- Vision detection supports configurable retries
- Invalid commands are rejected without corrupting system state
- Error reasons are stored explicitly in the context

This approach mirrors common industrial practices for robust system behavior.

---

## API Endpoints

### Health & State
- `GET /health`  
  Returns a simple health check response.

- `GET /state`  
  Returns the current CellContext, including state and counters.

### Commands
- `POST /home`  
  Homes the robot and transitions the cell to READY.

- `POST /pick`  
  Executes the pick operation with vision retries and gripper validation.

- `POST /place`  
  Executes the place operation and completes a cycle.

- `POST /run_cycle`  
  Executes a full cycle: home → pick → place.

- `POST /reset`  
  Resets the system from ERROR or IDLE to a safe initial state.

All endpoints return structured JSON responses indicating success or failure.

---

## Running the Application

### Requirements
- Python 3.10+
- fastapi
- uvicorn

### Install dependencies
```bash
pip install fastapi uvicorn
```

### Run the server
```bash
uvicorn app.main:app --reload
```

### API Documentation
Open your browser at:
http://127.0.0.1:8000/docs

Swagger UI allows interactive testing of all endpoints.

---

## Example Workflow

A typical workflow using the API:

1. POST /home
2. POST /pick
3. POST /place

Alternatively, a full cycle can be executed with:
- POST /run_cycle

The system returns structured responses describing the outcome of each operation.
---
## Behavior-Driven Testing (BDD)
This project includes automated tests using **pytest-bdd** to validate system behavior under different scenarios.

### What is Covered

Each aspect of the system is validated through explicit BDD scenarios:

#### Vision failures and retry logic

~~~gherkin
Scenario: Vision fails and pick goes to ERROR
  Given the cell is in READY state
  And the vision always fails
  When I execute a pick command
  Then the cell state should be ERROR
  And the error reason should be "vision_no_detection"
~~~

#### Robot motion failures

~~~gherkin
Scenario: Robot fails to move during pick
  Given the cell is in READY state
  And the vision always succeeds
  And the robot always fails
  And the gripper never slips
  When I execute a pick command
  Then the cell state should be ERROR
  And the error reason should be "robot_move_failed"
~~~

#### Gripper failures (slipping)

~~~gherkin
Scenario: Gripper slips after successful move
  Given the cell is in READY state
  And the vision always succeeds
  And the robot never fails
  And the gripper always slips
  When I execute a pick command
  Then the cell state should be ERROR
  And the error reason should be "grip_failed"
~~~

#### Invalid state transitions

~~~gherkin
Scenario: Pick called when cell is not READY
  Given the cell is in PICKING state
  When I execute a pick command
  Then the cell state should be ERROR
  And the error reason should be "not_ready"
~~~

#### Successful pick execution

~~~gherkin
Scenario: Pick succeeds when all components work
  Given the cell is in READY state
  And the vision always succeeds
  And the robot never fails
  And the gripper never slips
  When I execute a pick command
  Then the cell state should be READY
  And the robot should hold a part
~~~

#### Full cycle execution

~~~gherkin
Scenario: Full cycle succeeds
  Given the cell is in READY state
  And the vision always succeeds
  And the robot never fails
  And the gripper never slips
  When I execute a full cycle
  Then the cell state should be READY
  And the cycle counter should be incremented
~~~

---

### Running Tests

Install dependencies:

~~~bash
pip install pytest pytest-bdd pytest-cov
~~~

Run tests:

~~~bash
python -m pytest -q
~~~

Run with coverage:

~~~bash
python -m pytest --cov=app --cov-report=html
~~~

---

### Why BDD?

BDD ensures:

- Clear mapping between requirements and behavior  
- Deterministic testing (no randomness in tests)  
- Better readability and maintainability  
- Easier debugging of failure cases  
  
## Next Steps

Possible extensions to this project include:
- Structured logging and metrics
- Recovery strategies from the ERROR state
- Integration with real robotic hardware or ROS

---

## Notes

This project is intentionally simplified to focus on backend architecture,
state machines, and fault handling rather than real-time control.
