class Solver:
    def __init__(self):
        pass

class Beam:
    def __init__(self, length,intervals):
        self.length = length
        self.intervals = intervals
        self.loads = []
        self.supports = []
        
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

class PointLoad(Load):
    def __init__(self, magnitude, position):
        super().__init__(magnitude, position)
        