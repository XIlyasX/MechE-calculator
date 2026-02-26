def main():
    data = Take_Input()
    R_left, R_right = Compute_Reactions(
        data["length"],
        data["distance"],
        data["force"]
    )
    Shear = Compute_Shear(
        data["shear_position"],
        R_left,
        data["force"],
        data["distance"]
    )

    Moment = Compute_Moment(
        data["moment_position"],
        R_left,
        data["force"],
        data["distance"]
    )

    print(f"""Reaction forces:
          left reaction: {R_left}N
          right reaction: {R_right}N
          Shear: {Shear}N
          Moment: {Moment}Nm
          """)



def Take_Input():
    while True:
        length = get_number("Enter the length of the beam: ")
        distance_from_left = get_number("Enter the distance from left: ")
        force_in_newtons = get_number("Enter the force in newtons: ")
        shear_position = get_number("At which point you want to calculate shear?")
        moment_position = get_number("At which position you want to calculate moment?")

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
          Distance: {distance_from_left}m 
          Force: {force_in_newtons}N
          Shear position: {shear_position}m
          Moment position: {moment_position}m""")
    
    data = {
        "length": length,
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

def Compute_Shear(x, R_left, force, distance):
    V = R_left
    if x >= distance:
        V = R_left - force
    
    return V


def Compute_Moment(x, R_left, force, distance ):
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

    


        



main()