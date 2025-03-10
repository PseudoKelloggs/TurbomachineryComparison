class Turbomachinery:

    def __init__(self, machine_type, subtype): 
        # machine_type: Compressor, Turbine, etc.
        # subtype: Axial, Radial, etc.
        self.machine_type = machine_type
        self.subtype = subtype
        print("Machine Type:", self.machine_type)
        print("Subtype:", self.subtype)

