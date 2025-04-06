# Global registry
TURBOMACHINE_REGISTRY = {}

class Turbomachine:

    # Shared by all instances
    DB_FEATURES = (
        '`FLUID.type` VARCHAR(255), `FLUID.z` FLOAT, `FLUID.mdot` FLOAT, `FLUID.PRatio` FLOAT, '
        '`FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `eta.turb` FLOAT, `eta.comp` FLOAT, '
        '`FLUID.Tin` FLOAT, `RPM` FLOAT, `FLUID.Vdot` FLOAT, `Ns` FLOAT, `Ds` FLOAT, `D` FLOAT, '
        '`mass.turb` FLOAT, `mass.comp` FLOAT, `W.turb` FLOAT, `W.comp` FLOAT'
    )
    
    SIM_IN = 'id, `is.imputed`, `FLUID.type`, `FLUID.z`, `FLUID.mdot`, `FLUID.Plow`, `FLUID.Phigh`, `eta.turb`, `eta.comp`, `FLUID.Tin`, `RPM`'
   
    SIM_OUT = (
        '`FLUID.Vdot` = %s, `Ns` = %s, `Ds` = %s, `D` = %s, '
        '`mass.turb` = %s, `mass.comp` = %s, `W.turb` = %s, `W.comp` = %s'
    )

    def __init__(self, name, code, type, var_bounds):
        self.specs = {
            'Name': name,
            'code': code,
        }
        self.var_bounds = var_bounds

    def get_specs(self):
        return self.specs

    def get_bounds(self):
        return self.var_bounds

    def get_sim_input_fields(self):
        return Turbomachine.SIM_IN

    def get_sim_output_fields(self):
        return Turbomachine.SIM_OUT

    def get_db_schema(self):
        return Turbomachine.DB_FEATURES
    
    def get_turbomachine(code):
        """
        Retrieve a Turbomachine instance by its code and return its structured data.
        """
        machine = TURBOMACHINE_REGISTRY.get(code.lower())
        if not machine:
            raise ValueError(f"No Turbomachine registered with code '{code}'")
        
        return {
            'specs': machine.get_specs(),
            'Var_bounds': machine.get_bounds(),
            'DB_features': machine.get_db_schema(),
            'sim_in': machine.get_sim_input_fields(),
            'sim_out': machine.get_sim_output_fields()
    }


#EXAMPLE USAGE
#     comp = Turbomachine(
#     name='Basic Compressor',
#     code='Comp',
#     var_bounds=[
#         (0.85, 1),
#         (2, 18),
#         (1.8, 4.0),
#         (7.4, 8.5),
#         (0.7, 0.9),
#         (290, 750),
#         (10000, 100000)
#     ]
# )
