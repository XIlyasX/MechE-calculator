def main():
    data = Take_Input()
    R_left, R_right = Compute_Reactions(
        data["length"],
        data["distance"],
        data["force"]
    )
    print(f"""Reaction forces:
          left reaction: {R_left}N
          right reaction: {R_right}N
          """)



def Take_Input():
    while True:
        length = get_number("Enter the length of the beam: ")
        distance_from_left = get_number("Enter the distance from left: ")
        force_in_newtons = get_number("Enter the force in newtons: ")

        if length <= 0:
            print("Beam length must be positive.\n")
            continue

        if distance_from_left < 0 or distance_from_left > length:
            print("Distance must be between 0 and beam length.\n")
            continue
    
        break

    print(f"""you entered the following values: 
          Length: {length}m
          Distance: {distance_from_left}m 
          Force: {force_in_newtons}N""")
    
    data = {
        "length": length,
        "distance": distance_from_left,
        "force": force_in_newtons
    }
    
    return data

def Compute_Reactions(length, distance_from_left, force_in_newtons):
    R_right = force_in_newtons * distance_from_left / length
    R_left = force_in_newtons - R_right

    return R_left, R_right

def get_number(prompt):
    while True:
        value = input(prompt)
        
        try:
            return float(value)
        except ValueError:
            print("Please enter a number")

    


        



main()