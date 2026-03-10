def main():
    length, height, width, intervals = get_beam_dimensions()
    loads = get_loads(length)

    section = Section(height, width)
    beam = Beam(length, intervals)

    for load in loads:
        beam.add_load(load)
    
    beam.add_support(PinnedSupport(0))
    beam.add_support(RollerSupport(length))

    solver = Solver(beam, section)
    solver.solve()

# Input handling

def get_beam_dimensions():
    while True:
        length = get_number("Enter the length of the beam: ")
        if length <= 0:
            print("Beam's length must be positive.\n")
            continue
        height = get_number("Enter the height of the beam: ")
        if height <= 0:
            print("Beam's height must be positive.\n")
            continue
        width = get_number("Enter the width of the beam: ")
        if width <= 0:
            print("Beam's width must be positive.\n")
            continue
        intervals = get_number("Enter number of intervals: ", int)
        if intervals <= 0:
            print("Number of intervals must be bigger than 0: ")
            continue
        break
    return length, height, width, intervals

def get_loads(length):
    while True:
        loads_number = get_number("Enter number of loads: ", int)
        if loads_number <= 0:
            print("number of loads must be at least 1")
            continue
        loads = []
        for i in range(loads_number):
            while True:
                load_type = input("Enter load type, P/D: ")
                if load_type  not in ("P","D"):
                    print("Enter P/D: ")
                    continue
                force = get_number(f"Enter magnitude #{i+1}: ") 
                position = get_number(f"Enter position of force #{i+1}: ")
                if not 0 <= position <= length:
                    print(f"Position must be between 0 and beam {length}.")
                    continue
                if load_type == "D":
                    while True:
                        end = get_number(f"Enter end position of force #{i +1}: ")
                        if position <= end <= length:
                            loads.append(DistributedLoad(force, position, end))
                            break
                        else:
                            print(f"Position must be between {position} and beam {length}.")  
                    break        
                else:
                    loads.append(PointLoad(force, position))
                    break
                
                    
    
        return loads
    
# Model and computation

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
        output = []

        for x in self.beam.discretize():
            V = r_left - sum(load.shear_contribution(x) for load in self.beam.loads)
            output.append(V)
        return output

    def compute_moment(self):
        if not hasattr(self, '_moment'):
            output = []
            r_left, r_right = self.compute_reactions()
            for x in self.beam.discretize():
                M = x * r_left
                for load in self.beam.loads:
                    M -= load.moment_contribution(x)
                output.append(M)
            self._moment = output
        return self._moment

    def compute_stress(self):
        output = []
        c = self.section.height / 2
        I = self.section.width * self.section.height**3 / 12

        for M in self.compute_moment():
            output.append(M * c / I)
        return output
    
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


class Beam:
    def __init__(self, length,intervals):
        self.length = length
        self.intervals = intervals
        self.loads = []
        self.supports = []

    def add_load(self, load):
        self.loads.append(load)
    
    def add_support(self, support):
        self.supports.append(support)
    
    def discretize(self):
        delta = self.length / self.intervals
        return [i * delta for i in range(self.intervals + 1)]
        
class Section:
    def __init__(self, height, width):
        self.height = height
        self.width = width

class Support:
    def __init__(self, position):
        self.position = position

class PinnedSupport(Support):
    def __init__(self, position):
        super().__init__(position)

class RollerSupport(Support):
    def __init__(self, position):
        super().__init__(position)

class Load:
    def __init__(self, magnitude, position):
        self.magnitude = magnitude
        self.position = position

    def equivalent_force(self):
        raise NotImplementedError
        
    def equivalent_position(self):
        raise NotImplementedError
        
    def shear_contribution(self, x):
        raise NotImplementedError
        
    def moment_contribution(self, x):
        raise NotImplementedError

class PointLoad(Load):
    def __init__(self, magnitude, position):
        super().__init__(magnitude, position)
    
    def equivalent_position(self):
        return self.position
    
    def equivalent_magnitude(self):
        return self.magnitude

    def shear_contribution(self, x):
        if self.position <= x: return self.magnitude 
        return 0

    def moment_contribution(self,x):
        if self.position <= x: return self.magnitude * (x - self.position)
        return 0

class DistributedLoad(Load):
    def __init__(self, magnitude, position, end):
        super().__init__(magnitude, position)
        self.end = end

    def equivalent_position(self):
        return (self.end + self.position) / 2

    def equivalent_magnitude(self):
        return self.magnitude * (self.end - self.position)

    def shear_contribution(self, x):
        if self.position <= x <= self.end: return self.magnitude * (x - self.position) 
        elif self.end < x: return self.magnitude * (self.end - self.position)
        return 0

    def moment_contribution(self, x):
        if self.position <= x <= self.end: return self.magnitude * (x - self.position)**2 / 2
        elif self.end < x: return self.magnitude * (self.end - self.position) * (x - (self.position + self.end) / 2)
        return 0

# Utility functions

def get_number(prompt, number_type = float):
    while True:
        value = input(prompt)
        
        try:
            return number_type(value)
        except ValueError:
            print("Please enter a number")
    
def extract_min_and_max(values, coordinates = None):
    min_value = min(values)
    max_value = max(values)
    
    if coordinates is not None:
        min_index = values.index(min_value)
        max_index = values.index(max_value)
        return ((min_value, coordinates[min_index]),(max_value, coordinates[max_index])) 
    else:
        return (min_value, max_value)
    
def extract_absolute_value(values, coordinates = None):
    abs_values = [abs(v) for v in values]
    abs_value = max(abs_values)
    if coordinates is not None:
        index = abs_values.index(abs_value) 
        return (abs_value, coordinates[index])
    else:
        return abs_value


# Initiate        

if __name__ == "__main__":
    main()