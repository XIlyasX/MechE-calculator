import numpy as np

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
        return np.linspace(0, self.length, self.intervals + 1)
        
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
        return np.where(self.position <= x, self.magnitude, 0)

    def moment_contribution(self,x):
        return np.where(self.position <= x, self.magnitude * (x - self.position), 0)

class DistributedLoad(Load):
    def __init__(self, magnitude, position, end):
        super().__init__(magnitude, position)
        self.end = end

    def equivalent_position(self):
        return (self.end + self.position) / 2

    def equivalent_magnitude(self):
        return self.magnitude * (self.end - self.position)

    def shear_contribution(self, x):
        return np.where((self.position <= x) & (x <= self.end),
                         self.magnitude * (x - self.position),
                           np.where(self.end < x, self.magnitude * ( self.end - self.position), 0))

    def moment_contribution(self, x):
        return np.where((self.position <= x) & (x <= self.end),
                         self.magnitude * (x - self.position)**2 / 2,
                           np.where(self.end < x, self.magnitude * (self.end - self.position) * (x - (self.position + self.end) / 2), 0))