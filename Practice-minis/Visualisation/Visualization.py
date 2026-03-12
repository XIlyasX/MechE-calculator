import numpy as np

# Create an array of 100 points between 0 and 10
x = np.linspace(0, 10, 11)

# Try these and see what you get
print(x)
print(x[x > 5])  # filtering
print(np.sum(x))
print(np.min(x), np.max(x))