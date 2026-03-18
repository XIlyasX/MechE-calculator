from utils import get_number
from models import PointLoad, DistributedLoad

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
        E = get_number("Enter Young’s Modulus: ")
        if E <= 0:
            print("Must be positive.\n")
            continue
        intervals = get_number("Enter number of intervals: ", int)
        if intervals <= 0:
            print("Number of intervals must be bigger than 0: ")
            continue
        break
    return length, height, width,E, intervals

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