import numpy as np

def get_number(prompt, number_type = float):
    while True:
        value = input(prompt)
        
        try:
            return number_type(value)
        except ValueError:
            print("Please enter a number")
    
def extract_min_and_max(values, coordinates = None):
    min_value = np.min(values)
    max_value = np.max(values)
    
    if coordinates is not None:
        min_index = np.argmin(values)
        max_index = np.argmax(values)
        return ((min_value, coordinates[min_index]),(max_value, coordinates[max_index])) 
    else:
        return (min_value, max_value)
    
def extract_absolute_value(values, coordinates = None):
    abs_values = np.abs(values)
    abs_value = np.max(abs_values)
    if coordinates is not None:
        index = np.argmax(abs_values) 
        return (abs_value, coordinates[index])
    else:
        return abs_value