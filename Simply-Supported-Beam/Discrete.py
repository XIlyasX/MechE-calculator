def Descritize(length, number_of_intervals):
    delta = length / number_of_intervals
    coordinates = []
    for i in range(0, number_of_intervals + 1):
        coordinates.append(i * delta)
    return coordinates
    
def Compute_Shear(beam, R_left, force, distance):
    for x in beam:
        x = R_left
        if x >= distance:
            x = R_left - force


def main():
    length = input("enter length: ")
    number_of_intervals = input("enter nuumber of intervals: ")

    beam = Descritize(int(length),int(number_of_intervals))
    R_left = 5
    distance = 5
    force = 1
    output = []

    for x in beam:
        if x >= distance:
            x = R_left - force
        else:
            x = R_left
        output.append(x)
    print(output)


main()