def Descritize(length, resolution):
    delta = length / resolution
    coordinates = []
    for i in range(0, resolution):
        coordinates.append(i * delta)
    print(coordinates)
    



def main():
    length = input("enter length: ")
    points = input("enter number on chunks: ")

    Descritize(int(length),int(points))

main()