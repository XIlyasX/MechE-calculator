def get_number(prompt, number_type = float):
    while True:
        value = input(prompt)
        
        try:
            return number_type(value)
        except ValueError:
            print("Please enter a number")
    
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