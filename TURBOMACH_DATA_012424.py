TURBOMACH_DATA = {
    'Turb':{
        'specs': {
            'Name': 'Basic Turbine',
            'code': 'Turb'
        },
    'Var_bounds': [
        (0.85, 1), # FLUID mix ratio
        (2, 18), # FLUID mdot [kg/s]
        (1.8, 4.0), # FLUID Pressure ratio
        (7.4, 8.5), # FLUID P_low [MPa]
        (0.7,0.9), # eta.turb
        (600, 900), # FLUID inlet temp [K]
        (10000,100000) # RPM
    ],
    'DB_features': '`FLUID.type` VARCHAR(255), `FLUID.z` FLOAT, `FLUID.mdot` FLOAT, `FLUID.PRatio` FLOAT, `FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `eta.turb` FLOAT, `FLUID.Tin` FLOAT, `RPM` FLOAT, `FLUID.Vdot` FLOAT, `Ns` FLOAT, `Ds` FLOAT, `D` FLOAT, `mass.turb` FLOAT, `W.turb` FLOAT',
    'sim_in': 'id, `is.imputed`, `FLUID.type`, `FLUID.z`, `FLUID.mdot`, `FLUID.Plow`, `FLUID.Phigh`, `eta.turb`, `FLUID.Tin`,`RPM`',
    'sim_out': '`FLUID.Vdot` = %s, `Ns` = %s, `Ds` = %s, `D` = %s, `mass.turb` = %s, `W.turb` = %s'
    },
    
    'Comp':{
        'specs': {
            'Name': 'Basic Compressor',
            'code': 'Comp'
        },
    'Var_bounds': [
        (0.85, 1), # FLUID mix ratio
        (2, 18), # FLUID mdot [kg/s]
        (1.8, 4.0), # FLUID Pressure ratio
        (7.4, 8.5), # FLUID P_low [MPa]
        (0.7,0.9), # eta.comp
        (290, 750), # FLUID inlet temp [K]
        (10000,100000) # RPM
    ],
    'DB_features': '`FLUID.type` VARCHAR(255), `FLUID.z` FLOAT, `FLUID.mdot` FLOAT, `FLUID.PRatio` FLOAT, `FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `eta.comp` FLOAT, `FLUID.Tin` FLOAT, `RPM` FLOAT, `FLUID.Vdot` FLOAT, `Ns` FLOAT, `Ds` FLOAT, `D` FLOAT, `mass.comp` FLOAT, `W.comp` FLOAT',
    'sim_in': 'id, `is.imputed`, `FLUID.type`, `FLUID.z`, `FLUID.mdot`, `FLUID.Plow`, `FLUID.Phigh`, `eta.comp`, `FLUID.Tin`,`RPM`',
    'sim_out': '`FLUID.Vdot` = %s, `Ns` = %s, `Ds` = %s, `D` = %s, `mass.comp` = %s, `W.comp` = %s'
    }
}