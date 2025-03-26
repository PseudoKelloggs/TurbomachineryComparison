import csv
import numpy as np

def lhs(bounds, n_samples):
    num_vars = len(bounds)
    # Generate the intervals
    intervals = np.linspace(0, 1, n_samples + 1)
    
    # Initialize the sample containers
    samples = np.empty((n_samples, num_vars))
    
    # Iterate over each variable
    for ii in range(num_vars):
        # Get the bounds for the current variable
        min_val, max_val = bounds[ii]
        
        # Randomly sample one point in each interval
        points = np.random.uniform(intervals[:-1], intervals[1:], n_samples)
        
        # Map the sampled points to the range of the variable
        samples[:, ii] = min_val + (max_val - min_val) * points
        
        # Shuffle the points to ensure randomness along this dimension
        np.random.shuffle(samples[:, ii])
    
    return samples

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False