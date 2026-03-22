from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

from solver import Solver
from models import Beam, Section, PinnedSupport, RollerSupport, PointLoad, DistributedLoad

from fastapi.middleware.cors import CORSMiddleware

# -----------------------
# 1. Create the app
# -----------------------
app = FastAPI()


# for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# 2. Define input schema
# -----------------------
class LoadInput(BaseModel):
    type: Literal["point", "distributed"]
    magnitude: float = Field(gt=0)
    position: float = Field(ge=0)
    end: float | None = None   # only for distributed

class SolveRequest(BaseModel):
    length: float = Field(gt=0)
    height: float = Field(gt=0)
    width: float = Field(gt=0)
    E: float = Field(gt=0)
    intervals: int = Field(gt=0, le=10000)
    loads: list[LoadInput]

class SolveResponse(BaseModel):
    x: list[float]
    shear: list[float]
    moment: list[float]
    deflection: list[float]
    stress: list[float]



# -----------------------
# 3. Root endpoint (test)
# -----------------------
@app.get("/")
def root():
    return {"message": "API is working"}


# -----------------------
# 4. Main endpoint
# -----------------------
@app.post("/solve", response_model=SolveResponse)
def solve_beam(data: SolveRequest):

    beam = Beam(data.length, data.intervals)
    section = Section(data.height, data.width, data.E)

    beam.add_support(PinnedSupport(0))
    beam.add_support(RollerSupport(data.length))

    for load in data.loads:
        if load.type == "point":
            beam.add_load(PointLoad(load.magnitude, load.position))
        elif load.type == "distributed":
            if load.end is None or load.end <= load.position:
                raise HTTPException(
                    status_code=422,
                    detail="end must be greater than position")
            beam.add_load(DistributedLoad(load.magnitude, load.position, load.end))

    solver = Solver(beam, section)
    return SolveResponse(
        x=beam.discretize().tolist(),
        shear=solver.compute_shear().tolist(),
        moment=solver.compute_moment().tolist(),
        deflection=solver.compute_deflection().tolist(),
        stress=solver.compute_stress().tolist()
)