def main():
    data = take_input()
    beam = discretize(
        (data["length"]),
        (data["intervals"])
    )
    r_left, r_right = compute_reactions(
        data["length"],
        data["loads"],
    )
    shear_at_x = compute_shear_at_x(
        data["shear_position"],
        r_left,
        data["loads"],
    )

    moment_at_x = compute_moment_at_x(
        data["moment_position"],
        r_left,
        data["loads"]
    )
    Shear = compute_shear(
        beam,
        r_left,
        data["loads"],
    )
    Moment = compute_moment(
        beam,
        r_left,
        data["loads"],
    )
    (min_shear,max_shear) = extract_min_and_max(Shear)
    ((min_moment, min_moment_pos),( max_moment, max_moment_pos)) = extract_min_and_max(Moment, beam)
    print(f"""Reaction forces:
          left reaction: {r_left}N
          right reaction: {r_right}N
          Shear: {Shear}
          Moment: {Moment}
          Shear at x: {shear_at_x}N
          Moment at x: {moment_at_x}Nm
          min shear: {min_shear}N
          max sheaer: {max_shear}N
          min moment: {min_moment}Nm
          at: {min_moment_pos}m
          max moment: {max_moment}Nm
          at: {max_moment_pos}m
          """)



def take_input():
    while True:
        length = get_number("Enter the length of the beam: ")
        if length <= 0:
            print("Beam's length must be positive.\n")
            continue
        height = get_number("Enter the height of the beam: ")
        if height <= 0:
            print("Beam's height must be positive.\n")
            continue
        height = get_number("Enter the height of the beam: ")
        if height <= 0:
            print("Beam's height must be positive.\n")
            continue
        number_of_intervals = get_number("Enter number of intervals: ", int)
        if number_of_intervals <= 0:
            print("Number of internvals must be bigger than 0: ")
            continue
        loads_number = get_number("Enter number of loads: ", int)
        if loads_number <= 0:
            print("number of loads must be at least 1")
            continue
        loads = []
        for i in range(0, loads_number):
            while True:
                force = get_number(f"Enter force #{i+1}: ") 
                position = get_number(f"Enter position of force #{i+1}: ")
                if 0 <= position <= length:
                    loads.append((force, position))
                    break
                else:
                    print("Position must be between 0 and beam length.")
        shear_position = get_number("At which point you want to calculate shear?")
        if shear_position < 0 or shear_position > length:
            print("Point must be between 0 and beam length.\n")
            continue
        moment_position = get_number("At which position you want to calculate moment?")
        if moment_position < 0 or moment_position > length:
            print("Point must be between 0 and beam length.\n")
            continue
    
        break

    print(f"""you entered the following values: 
          Length: {length}m
          Intervals: {number_of_intervals}
          Loads: {loads}
          Shear position: {shear_position}m
          Moment position: {moment_position}m""")
    
    data = {
        "length": length,
        "intervals": number_of_intervals,
        "loads": loads,
        "shear_position": shear_position,
        "moment_position": moment_position
    }
    
    return data


def compute_reactions(length, loads):
    r_right = sum(force * position for force,position in loads) / length
    r_left = sum(force for force,position in loads) - r_right

    return r_left, r_right


def compute_shear(beam, r_left, loads):
    output = []

    for x in beam:
        output.append(compute_shear_at_x(x, r_left, loads))

    return output

def compute_shear_at_x(x, r_left, loads):
    V = r_left - sum(force for force,position in loads if position <= x)
    
    return V

def compute_moment(beam, r_left, loads):
    output = []

    for x in beam:
        output.append(compute_moment_at_x(x, r_left, loads))
    
    return output

def compute_moment_at_x(x, r_left, loads ):
    M = x * r_left
    for force, position in loads:
        if position <= x:
            M -= force * (x - position)

    return M

def get_number(prompt, number_type = float):
    while True:
        value = input(prompt)
        
        try:
            return number_type(value)
        except ValueError:
            print("Please enter a number")


def discretize(length, number_of_intervals):
    delta = length / number_of_intervals
    coordinates = []
    for i in range(0, number_of_intervals + 1):
        coordinates.append(i * delta)
    return coordinates
    
def extract_min_and_max(values, coordinates = None):
    min_value = min(values)
    max_value = max(values)
    
    if coordinates is not None:
        min_index = values.index(min_value)
        max_index = values.index(max_value)
        return ((min_value, coordinates[min_index]),(max_value, coordinates[max_index])) 
    else:
        return (min_value, max_value)
    






    


        



main()