def main():
    data = Take_Input()
    Beam = Descritize(
        float(data["length"]),
        float(data["intervals"])
    )
    R_left, R_right = Compute_Reactions(
        data["length"],
        data["distance"],
        data["force"]
    )
    Shear_at_x = Compute_Shear_at_x(
        data["shear_position"],
        R_left,
        data["force"],
        data["distance"]
    )

    Moment_at_x = Compute_Moment_at_x(
        data["moment_position"],
        R_left,
        data["force"],
        data["distance"]
    )
    Shear = Compute_Shear(
        Beam,
        R_left,
        data["force"],
        data["distance"]
    )
    Moment = Compute_Moment(
        Beam,
        R_left,
        data["force"],
        data["distance"]
    )
    print(f"""Reaction forces:
          left reaction: {R_left}N
          right reaction: {R_right}N
          Shear: {Shear}
          Moment: {Moment}
          Shear at x: {Shear_at_x}N
          Moment at x: {Moment_at_x}Nm
          """)



def Take_Input():
    while True:
        length = get_number("Enter the length of the beam: ")
        number_of_intervals = get_number("Enter number of intervals: ")
        distance_from_left = get_number("Enter the distance from left: ")
        force_in_newtons = get_number("Enter the force in newtons: ")
        shear_position = get_number("At which point you want to calculate shear?")
        moment_position = get_number("At which position you want to calculate moment?")

        if number_of_intervals <= 0:
            print("Number of internvals must be bigger than 0: ")
            continue

        if length <= 0:
            print("Beam length must be positive.\n")
            continue

        if shear_position < 0 or shear_position > length:
            print("Point must be between 0 and beam length.\n")
            continue

        if moment_position < 0 or moment_position > length:
            print("Point must be between 0 and beam length.\n")
            continue

        if distance_from_left < 0 or distance_from_left > length:
            print("Distance must be between 0 and beam length.\n")
            continue
    
        break

    print(f"""you entered the following values: 
          Length: {length}m
          Intervals: {number_of_intervals}
          Distance: {distance_from_left}m 
          Force: {force_in_newtons}N
          Shear position: {shear_position}m
          Moment position: {moment_position}m""")
    
    data = {
        "length": length,
        "intervals": number_of_intervals,
        "distance": distance_from_left,
        "force": force_in_newtons,
        "shear_position": shear_position,
        "moment_position": moment_position
    }
    
    return data


def Compute_Reactions(length, distance_from_left, force_in_newtons):
    R_right = force_in_newtons * distance_from_left / length
    R_left = force_in_newtons - R_right

    return R_left, R_right


def Compute_Shear(beam, R_left, force, distance):
    output = []

    for x in beam:
        output.append(Compute_Shear_at_x(x, R_left, force, distance))

    return output

def Compute_Shear_at_x(x, R_left, force, distance):
    V = R_left
    if x >= distance:
        V = R_left - force
    
    return V

def Compute_Moment(beam, R_left, force, distance):
    output = []

    for x in beam:
        output.append(Compute_Moment_at_x(x, R_left, force, distance))
    
    return output

def Compute_Moment_at_x(x, R_left, force, distance ):
    M = x * R_left
    if x >= distance:
        M = x * R_left - force * (x - distance)
    return M

def get_number(prompt):
    while True:
        value = input(prompt)
        
        try:
            return float(value)
        except ValueError:
            print("Please enter a number")


def Descritize(length, number_of_intervals):
    delta = length / number_of_intervals
    coordinates = []
    for i in range(0, number_of_intervals + 1):
        coordinates.append(i * delta)
    return coordinates
    





    


        



main()