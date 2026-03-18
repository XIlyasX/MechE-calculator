from solver import Solver
from models import Beam, Section, PinnedSupport, RollerSupport
from cli import get_beam_dimensions, get_loads


def main():
    length, height, width,E, intervals = get_beam_dimensions()
    loads = get_loads(length)

    section = Section(height, width, E)
    beam = Beam(length, intervals)

    for load in loads:
        beam.add_load(load)
    
    beam.add_support(PinnedSupport(0))
    beam.add_support(RollerSupport(length))

    solver = Solver(beam, section)
    solver.solve()
        

if __name__ == "__main__":
    main()