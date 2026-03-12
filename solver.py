import numpy as np

from utils import extract_absolute_value, extract_min_and_max

class Solver:
    def __init__(self, beam, section):
        self.beam = beam
        self.section = section

    def compute_reactions(self):
        if not hasattr(self, '_reactions'):
            r_right = sum(load.equivalent_magnitude() * load.equivalent_position() for load in self.beam.loads) / self.beam.length
            r_left = sum(load.equivalent_magnitude() for load in self.beam.loads) - r_right
            self._reactions = (r_left, r_right)
        return self._reactions
    
    def compute_shear(self):
        r_left, r_right = self.compute_reactions()

        x = self.beam.discretize()
        V = r_left - sum(load.shear_contribution(x) for load in self.beam.loads)
        return V

    def compute_moment(self):
        if not hasattr(self, '_moment'):
            r_left, r_right = self.compute_reactions()
            x = self.beam.discretize()
            M = x * r_left - sum(load.moment_contribution(x) for load in self.beam.loads)
            self._moment = M
        return self._moment

    def compute_stress(self):
        c = self.section.height / 2
        I = self.section.width * self.section.height**3 / 12

        return self.compute_moment() * c / I
    
    def solve(self):
        beam = self.beam.discretize()
        r_left, r_right = self.compute_reactions()
        shear = self.compute_shear()
        moment = self.compute_moment()
        stress = self.compute_stress()

        (abs_stress, abs_stress_pos) = extract_absolute_value(stress, beam)
        (min_shear,max_shear) = extract_min_and_max(shear)
        ((min_moment, min_moment_pos),( max_moment, max_moment_pos)) = extract_min_and_max(moment, beam)

        print(f"""
              Left reaction: {r_left}N
              Right reaction: {r_right}N
              Beam: {beam}
              Shear: {shear}
              Moment: {moment}
              Stress: {stress}
              min shear: {min_shear}N
              max shear: {max_shear}N
              min moment: {min_moment}Nm
              at: {min_moment_pos}m
              max moment: {max_moment}Nm
              at: {max_moment_pos}m
              absolute stress: {abs_stress}Pa
              at: {abs_stress_pos}m
              """)