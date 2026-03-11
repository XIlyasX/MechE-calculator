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
    shear = compute_shear(
        beam,
        r_left,
        data["loads"],
    )
    moment = compute_moment(
        beam,
        r_left,
        data["loads"],
    )
    stress = compute_stress(
        moment,
        data["height"],
        data["width"]
    )
    ( abs_stress, abs_stress_pos) = extract_absolute_value(stress, beam)
    (min_shear,max_shear) = extract_min_and_max(shear)
    ((min_moment, min_moment_pos),( max_moment, max_moment_pos)) = extract_min_and_max(moment, beam)
    print(f"""Reaction forces:
          left reaction: {r_left}N
          right reaction: {r_right}N
          Shear: {shear}
          Moment: {moment}
          Stress: {stress}
          Shear at x: {shear_at_x}N
          Moment at x: {moment_at_x}Nm
          min shear: {min_shear}N
          max shear: {max_shear}N
          min moment: {min_moment}Nm
          at: {min_moment_pos}m
          max moment: {max_moment}Nm
          at: {max_moment_pos}m
          absolute stress: {abs_stress}Pa
          at: {abs_stress_pos}m
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
        width = get_number("Enter the width of the beam: ")
        if width <= 0:
            print("Beam's width must be positive.\n")
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
        for i in range(loads_number):
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
          Height: {height}m
          Width: {width}m
          Intervals: {number_of_intervals}
          Loads: {loads}
          Shear position: {shear_position}m
          Moment position: {moment_position}m""")
    
    data = {
        "length": length,
        "height": height,
        "width": width,
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

def compute_stress(moment, height, width):
    output = []
    c = height/2
    I = width * height**3 / 12

    for M in moment:
        output.append(M * c / I)

    return output

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
    for i in range(number_of_intervals + 1):
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
    
def extract_absolute_value(values, coordinates = None):
    abs_values = [abs(v) for v in values]
    abs_value = max(abs_values)
    if coordinates is not None:
        index = abs_values.index(abs_value) 
        return (abs_value, coordinates[index])
    else:
        return abs_value

    






    


        



main()