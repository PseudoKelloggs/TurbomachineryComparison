import numpy as np

class VelocityTriangle:
    def __init__(self):
        self.bladeSpeed = np.arange(1000, 100000, 10)  # Rotational Speed from 1,000 to 100,000
        self.bladeAngle = np.arange(0, 60, 1)  # Blade Angle from 0 to 60 degrees
        
        # Placeholder arrays for other velocity components (to be computed later)
        self.relativeVelocity = None
        self.absoluteVelocity = None
        self.relativeFlowAngle = None
        self.absoluteFlowAngle = None
        self.normalVelocity = None
        self.tangentialVelocity = None

    def display_initial_values(self):
        print("Blade Speed:", self.bladeSpeed[:10])
        print("Blade Angle:", self.bladeAngle[:10])

# Create an instance of the VelocityTriangle class
velocity_triangle = VelocityTriangle()
velocity_triangle.display_initial_values()

