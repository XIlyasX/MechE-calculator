def main():
    get_input()

def get_input():
    
    loads_number = get_number("Enter number of loads: ")
    loads = []
    for i in range(0, int(loads_number)):
        force = get_number("Enter the value of force: ") 
        position = get_number("Enter the position where this force is applied: ")
        loads.append((force, position))
    print(loads)
    
        




def get_number(prompt):
    while True:
        value = input(prompt)

        try:
            return float(value)
        except ValueError:
            print("please enter a number")




main()