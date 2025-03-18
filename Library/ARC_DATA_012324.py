ARC_DATA = {
    'DH_RC': {
        'Cycle_specs': {
            'Name': 'Direct Heating, Recuperated Cycle',
            'Code': 'DH_RC',
            'turb': 1,
            'comp': 1,
            'hxer': 2,
            'heating': 'direct'
            },
        'Var_bounds': [
            (0.85, 1), # FLUID mix ratio
            (600, 900), # FLUID Max Temp [K]
            (275, 315), # COOLANT In Temp [K]
            (7.4, 8.5), # FLUID P_low [MPa]
            (1.8, 4.0), # FLUID Pressure Ratio
            (0.7, 0.9), # eta_comp
            (0.7, 0.9), # eta_turb
            (0.4,0.9), # eps_hx_1
            (0.4,0.9), # eps_hx_2
            (2,18), # FLUID_mdot
            (3, 10) # COOLANT_mdot [kg/s]
            ],
        'DB_features': '`FLUID.type` VARCHAR(255), `COOLANT.type` VARCHAR(255), `FLUID.z` FLOAT, `Q.source` FLOAT, `FLUID.TMax` FLOAT,`COOLANT.Tin` FLOAT, `FLUID.PRatio` FLOAT, `FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `COOLANT.Pop` FLOAT, `eta.comp` FLOAT, `eta.turb` FLOAT, `eta.pump` FLOAT, `eps.1` FLOAT, `eps.2` FLOAT, `FLUID.mdot` FLOAT, `COOLANT.mdot` FLOAT, `FLUID.T1` FLOAT, `FLUID.T2` FLOAT, `FLUID.T3` FLOAT, `FLUID.T4` FLOAT, `FLUID.T5` FLOAT, `FLUID.T6` FLOAT, `FLUID.P1` FLOAT, `FLUID.P2` FLOAT, `FLUID.P3` FLOAT, `FLUID.P4` FLOAT, `FLUID.P5` FLOAT, `FLUID.P6` FLOAT, `FLUID.h1` FLOAT, `FLUID.h2` FLOAT, `FLUID.h3` FLOAT, `FLUID.h4` FLOAT, `FLUID.h5` FLOAT, `FLUID.h6` FLOAT,`FLUID.s1` FLOAT, `FLUID.s2` FLOAT, `FLUID.s3` FLOAT, `FLUID.s4` FLOAT, `FLUID.s5` FLOAT, `FLUID.s6` FLOAT, `COOLANT.T1` FLOAT, `COOLANT.T2` FLOAT, `COOLANT.T3` FLOAT, `COOLANT.P1` FLOAT, `COOLANT.P2` FLOAT, `COOLANT.P3` FLOAT, `COOLANT.h1` FLOAT, `COOLANT.h2` FLOAT, `COOLANT.h3` FLOAT, `COOLANT.s1` FLOAT, `COOLANT.s2` FLOAT, `COOLANT.s3` FLOAT, `eta.cyc` FLOAT, `W.comp` FLOAT, `W.turb` FLOAT, `W.pump` FLOAT, `W.net` FLOAT',
        'sim_in': "id, `is.imputed`, `FLUID.type`, `FLUID.z`, `COOLANT.type`, `FLUID.mdot`, `COOLANT.mdot`, `FLUID.TMax`, `COOLANT.Tin`, `FLUID.Plow`, `FLUID.Phigh`, `COOLANT.Pop`, `eta.comp`, `eta.turb`, `eta.pump`, `eps.1`, `eps.2`",
        'sim_out': "`is.con` = %s, `Q.source` = %s, `FLUID.T1` = %s, `FLUID.T2` = %s, `FLUID.T3` = %s, `FLUID.T4` = %s, `FLUID.T5` = %s, `FLUID.T6` = %s, `FLUID.P1` = %s, `FLUID.P2` = %s, `FLUID.P3` = %s, `FLUID.P4` = %s, `FLUID.P5` = %s, `FLUID.P6` = %s, `FLUID.h1` = %s, `FLUID.h2` = %s, `FLUID.h3` = %s, `FLUID.h4` = %s, `FLUID.h5` = %s, `FLUID.h6` = %s,`FLUID.s1` = %s, `FLUID.s2` = %s, `FLUID.s3` = %s, `FLUID.s4` = %s, `FLUID.s5` = %s, `FLUID.s6` = %s, `COOLANT.T1` = %s, `COOLANT.T2` = %s, `COOLANT.T3` = %s, `COOLANT.P1` = %s, `COOLANT.P2` = %s, `COOLANT.P3` = %s, `COOLANT.h1` = %s, `COOLANT.h2` = %s, `COOLANT.h3` = %s, `COOLANT.s1` = %s, `COOLANT.s2` = %s, `COOLANT.s3` = %s, `eta.cyc` = %s, `W.comp` = %s, `W.turb` = %s, `W.pump` = %s, `W.net` = %s",
        'validation_metrics': "id, `is.con`, `eta.cyc`, `W.net`, `FLUID.Tmax`, `FLUID.T1`, `FLUID.T2`, `FLUID.T3`, `FLUID.T4`, `FLUID.T5`, `FLUID.T6`"
    },
    'DH_NRC': {
        'Cycle_specs': {
            'Name': 'Direct Heating, Non-Recuperated Cycle',
            'Code': 'DH_NRC',
            'turb': 1,
            'comp': 1,
            'hxer': 1,
            'heating': 'direct'
            },
        'Var_bounds': [
            (0.85, 1), # FLUID mix ratio
            (600, 900), # FLUID Max Temp [K]
            (275, 315), # COOLANT In Temp [K]
            (7.4, 8.5), # FLUID P_low [MPa]
            (1.8, 4.0), # FLUID Pressure Ratio
            (0.7, 0.9), # eta_comp
            (0.7, 0.9), # eta_turb
            (0.4,0.9), # eps_hx_1
            (2,18), # FLUID_mdot
            (3, 10) # COOLANT_mdot [kg/s]
            ],
        'DB_features': '`FLUID.type` VARCHAR(255), `COOLANT.type` VARCHAR(255), `FLUID.z` FLOAT, `Q.source` FLOAT, `FLUID.TMax` FLOAT,`COOLANT.Tin` FLOAT, `FLUID.PRatio` FLOAT, `FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `COOLANT.Pop` FLOAT, `eta.comp` FLOAT, `eta.turb` FLOAT, `eta.pump` FLOAT, `eps.1` FLOAT, `FLUID.mdot` FLOAT, `COOLANT.mdot` FLOAT, `FLUID.T1` FLOAT, `FLUID.T2` FLOAT, `FLUID.T3` FLOAT, `FLUID.T4` FLOAT, `FLUID.P1` FLOAT, `FLUID.P2` FLOAT, `FLUID.P3` FLOAT, `FLUID.P4` FLOAT, `FLUID.h1` FLOAT, `FLUID.h2` FLOAT, `FLUID.h3` FLOAT, `FLUID.h4` FLOAT, `FLUID.s1` FLOAT, `FLUID.s2` FLOAT, `FLUID.s3` FLOAT, `FLUID.s4` FLOAT, `COOLANT.T1` FLOAT, `COOLANT.T2` FLOAT, `COOLANT.T3` FLOAT, `COOLANT.P1` FLOAT, `COOLANT.P2` FLOAT, `COOLANT.P3` FLOAT, `COOLANT.h1` FLOAT, `COOLANT.h2` FLOAT, `COOLANT.h3` FLOAT, `COOLANT.s1` FLOAT, `COOLANT.s2` FLOAT, `COOLANT.s3` FLOAT, `eta.cyc` FLOAT, `W.comp` FLOAT, `W.turb` FLOAT, `W.pump` FLOAT, `W.net` FLOAT',
        'sim_in': "id, `is.imputed`, `FLUID.type`, `FLUID.z`, `COOLANT.type`, `FLUID.mdot`, `COOLANT.mdot`, `FLUID.TMax`, `COOLANT.Tin`, `FLUID.Plow`, `FLUID.Phigh`, `COOLANT.Pop`, `eta.comp`, `eta.turb`, `eta.pump`, `eps.1`",
        'sim_out': "`is.con` = %s, `Q.source` = %s, `FLUID.T1` = %s, `FLUID.T2` = %s, `FLUID.T3` = %s, `FLUID.T4` = %s, `FLUID.P1` = %s, `FLUID.P2` = %s, `FLUID.P3` = %s, `FLUID.P4` = %s, `FLUID.h1` = %s, `FLUID.h2` = %s, `FLUID.h3` = %s, `FLUID.h4` = %s, `FLUID.s1` = %s, `FLUID.s2` = %s, `FLUID.s3` = %s, `FLUID.s4` = %s, `COOLANT.T1` = %s, `COOLANT.T2` = %s, `COOLANT.T3` = %s, `COOLANT.P1` = %s, `COOLANT.P2` = %s, `COOLANT.P3` = %s, `COOLANT.h1` = %s, `COOLANT.h2` = %s, `COOLANT.h3` = %s, `COOLANT.s1` = %s, `COOLANT.s2` = %s, `COOLANT.s3` = %s, `eta.cyc` = %s, `W.comp` = %s, `W.turb` = %s, `W.pump` = %s, `W.net` = %s",
        'validation_metrics': "id, `is.con`, `eta.cyc`, `W.net`, `FLUID.Tmax`, `FLUID.T1`, `FLUID.T2`, `FLUID.T3`, `FLUID.T4`"
    },    
    'IH_RC': {
        'Cycle_specs': {
            'Name': 'Indirect Heating, Recuperated Cycle',
            'Code': 'IH_RC',
            'turb': 1,
            'comp': 1,
            'hxer': 3,
            'heating': 'indirect'
            },
        'Var_bounds': [
            (0.85, 1), # FLUID mix ratio
            (600, 900), # COOLANT Max Temp [K]
            (275, 315), # COOLANT In Temp [K]
            (7.4, 8.5), # FLUID P_low [MPa]
            (1.8, 4.0), # FLUID Pressure Ratio
            (0.7, 0.9), # eta_comp
            (0.7, 0.9), # eta_turb
            (0.4,0.9), # eps_hx_1
            (0.4,0.9), # eps_hx_2
            (0.4,0.9), # eps_hx_3
            (2,18), # FLUID_mdot
            (3, 10) # COOLANT_mdot [kg/s]
            ],
        'DB_features': '`FLUID.type` VARCHAR(255), `COOLANT.type` VARCHAR(255), `FLUID.z` FLOAT, `Q.source` FLOAT, `COOLANT.TMax` FLOAT,`COOLANT.Tin` FLOAT, `FLUID.PRatio` FLOAT, `FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `COOLANT.Pop` FLOAT, `eta.comp` FLOAT, `eta.turb` FLOAT, `eta.pump` FLOAT, `eps.1` FLOAT, `eps.2` FLOAT, `eps.3` FLOAT, `FLUID.mdot` FLOAT, `COOLANT.mdot` FLOAT, `FLUID.T1` FLOAT, `FLUID.T2` FLOAT, `FLUID.T3` FLOAT, `FLUID.T4` FLOAT, `FLUID.T5` FLOAT, `FLUID.T6` FLOAT, `FLUID.P1` FLOAT, `FLUID.P2` FLOAT, `FLUID.P3` FLOAT, `FLUID.P4` FLOAT, `FLUID.P5` FLOAT, `FLUID.P6` FLOAT, `FLUID.h1` FLOAT, `FLUID.h2` FLOAT, `FLUID.h3` FLOAT, `FLUID.h4` FLOAT, `FLUID.h5` FLOAT, `FLUID.h6` FLOAT,`FLUID.s1` FLOAT, `FLUID.s2` FLOAT, `FLUID.s3` FLOAT, `FLUID.s4` FLOAT, `FLUID.s5` FLOAT, `FLUID.s6` FLOAT, `COOLANT.T1` FLOAT, `COOLANT.T2` FLOAT, `COOLANT.T3` FLOAT, `COOLANT.T4` FLOAT, `COOLANT.T5` FLOAT, `COOLANT.P1` FLOAT, `COOLANT.P2` FLOAT, `COOLANT.P3` FLOAT, `COOLANT.P4` FLOAT, `COOLANT.P5` FLOAT, `COOLANT.h1` FLOAT, `COOLANT.h2` FLOAT, `COOLANT.h3` FLOAT, `COOLANT.h4` FLOAT, `COOLANT.h5` FLOAT, `COOLANT.s1` FLOAT, `COOLANT.s2` FLOAT, `COOLANT.s3` FLOAT, `COOLANT.s4` FLOAT, `COOLANT.s5` FLOAT, `eta.cyc` FLOAT, `W.comp` FLOAT, `W.turb` FLOAT, `W.pump` FLOAT, `W.net` FLOAT',
        'sim_in': "id, `is.imputed`, `FLUID.type`, `FLUID.z`, `COOLANT.type`, `FLUID.mdot`, `COOLANT.mdot`, `COOLANT.TMax`, `COOLANT.Tin`, `FLUID.Plow`, `FLUID.Phigh`, `COOLANT.Pop`, `eta.comp`, `eta.turb`, `eta.pump`, `eps.1`, `eps.2`, `eps.3`",
        'sim_out': "`is.con` = %s, `Q.source` = %s, `FLUID.T1` = %s, `FLUID.T2` = %s, `FLUID.T3` = %s, `FLUID.T4` = %s, `FLUID.T5` = %s, `FLUID.T6` = %s, `FLUID.P1` = %s, `FLUID.P2` = %s, `FLUID.P3` = %s, `FLUID.P4` = %s, `FLUID.P5` = %s, `FLUID.P6` = %s, `FLUID.h1` = %s, `FLUID.h2` = %s, `FLUID.h3` = %s, `FLUID.h4` = %s, `FLUID.h5` = %s, `FLUID.h6` = %s, `FLUID.s1` = %s, `FLUID.s2` = %s, `FLUID.s3` = %s, `FLUID.s4` = %s, `FLUID.s5` = %s, `FLUID.s6` = %s, `COOLANT.T1` = %s, `COOLANT.T2` = %s, `COOLANT.T3` = %s, `COOLANT.T4` = %s, `COOLANT.T5` = %s, `COOLANT.P1` = %s, `COOLANT.P2` = %s, `COOLANT.P3` = %s, `COOLANT.P4` = %s, `COOLANT.P5` = %s, `COOLANT.h1` = %s, `COOLANT.h2` = %s, `COOLANT.h3` = %s, `COOLANT.h4` = %s, `COOLANT.h5` = %s, `COOLANT.s1` = %s, `COOLANT.s2` = %s, `COOLANT.s3` = %s, `COOLANT.s4` = %s, `COOLANT.s5` = %s, `eta.cyc` = %s, `W.comp` = %s, `W.turb` = %s, `W.pump` = %s, `W.net` = %s",
        'validation_metrics': "id, `is.con`, `eta.cyc`, `W.net`, `COOLANT.Tmax`, `COOLANT.T1`, `COOLANT.T2`, `COOLANT.T3`, `COOLANT.T4`, `COOLANT.T5`"
    },
    'IH_NRC': {
        'Cycle_specs': {
            'Name': 'Indirect Heating, Non-Recuperated Cycle',
            'Code': 'IH_NRC',
            'turb': 1,
            'comp': 1,
            'hxer': 2,
            'heating': 'indirect'
            },
        'Var_bounds': [
            (0.85, 1), # FLUID mix ratio
            (600, 900), # COOLANT Max Temp [K]
            (275, 315), # COOLANT In Temp [K]
            (7.4, 8.5), # FLUID P_low [MPa]
            (1.8, 4.0), # FLUID Pressure Ratio
            (0.7, 0.9), # eta_comp
            (0.7, 0.9), # eta_turb
            (0.4,0.9), # eps_hx_1
            (0.4,0.9), # eps_hx_2
            (2,18), # FLUID_mdot
            (3, 10) # COOLANT_mdot [kg/s]
            ],
        'DB_features': '`FLUID.type` VARCHAR(255), `COOLANT.type` VARCHAR(255), `FLUID.z` FLOAT, `Q.source` FLOAT, `COOLANT.TMax` FLOAT,`COOLANT.Tin` FLOAT, `FLUID.PRatio` FLOAT, `FLUID.Plow` FLOAT, `FLUID.Phigh` FLOAT, `COOLANT.Pop` FLOAT, `eta.comp` FLOAT, `eta.turb` FLOAT, `eta.pump` FLOAT, `eps.1` FLOAT, `eps.2` FLOAT, `FLUID.mdot` FLOAT, `COOLANT.mdot` FLOAT, `FLUID.T1` FLOAT, `FLUID.T2` FLOAT, `FLUID.T3` FLOAT, `FLUID.T4` FLOAT, `FLUID.P1` FLOAT, `FLUID.P2` FLOAT, `FLUID.P3` FLOAT, `FLUID.P4` FLOAT, `FLUID.h1` FLOAT, `FLUID.h2` FLOAT, `FLUID.h3` FLOAT, `FLUID.h4` FLOAT, `FLUID.s1` FLOAT, `FLUID.s2` FLOAT, `FLUID.s3` FLOAT, `FLUID.s4` FLOAT, `COOLANT.T1` FLOAT, `COOLANT.T2` FLOAT, `COOLANT.T3` FLOAT, `COOLANT.T4` FLOAT, `COOLANT.T5` FLOAT, `COOLANT.P1` FLOAT, `COOLANT.P2` FLOAT, `COOLANT.P3` FLOAT, `COOLANT.P4` FLOAT, `COOLANT.P5` FLOAT, `COOLANT.h1` FLOAT, `COOLANT.h2` FLOAT, `COOLANT.h3` FLOAT, `COOLANT.h4` FLOAT, `COOLANT.h5` FLOAT, `COOLANT.s1` FLOAT, `COOLANT.s2` FLOAT, `COOLANT.s3` FLOAT, `COOLANT.s4` FLOAT, `COOLANT.s5` FLOAT, `eta.cyc` FLOAT, `W.comp` FLOAT, `W.turb` FLOAT, `W.pump` FLOAT, `W.net` FLOAT',
        'sim_in': "id, `is.imputed`, `FLUID.type`, `FLUID.z`, `COOLANT.type`, `FLUID.mdot`, `COOLANT.mdot`, `COOLANT.TMax`, `COOLANT.Tin`, `FLUID.Plow`, `FLUID.Phigh`, `COOLANT.Pop`, `eta.comp`, `eta.turb`, `eta.pump`, `eps.1`, `eps.2`",
        'sim_out': "`is.con` = %s, `Q.source` = %s, `FLUID.T1` = %s, `FLUID.T2` = %s, `FLUID.T3` = %s, `FLUID.T4` = %s, `FLUID.P1` = %s, `FLUID.P2` = %s, `FLUID.P3` = %s, `FLUID.P4` = %s, `FLUID.h1` = %s, `FLUID.h2` = %s, `FLUID.h3` = %s, `FLUID.h4` = %s, `FLUID.s1` = %s, `FLUID.s2` = %s, `FLUID.s3` = %s, `FLUID.s4` = %s, `COOLANT.T1` = %s, `COOLANT.T2` = %s, `COOLANT.T3` = %s, `COOLANT.T4` = %s, `COOLANT.T5` = %s, `COOLANT.P1` = %s, `COOLANT.P2` = %s, `COOLANT.P3` = %s, `COOLANT.P4` = %s, `COOLANT.P5` = %s, `COOLANT.h1` = %s, `COOLANT.h2` = %s, `COOLANT.h3` = %s, `COOLANT.h4` = %s, `COOLANT.h5` = %s, `COOLANT.s1` = %s, `COOLANT.s2` = %s, `COOLANT.s3` = %s, `COOLANT.s4` = %s, `COOLANT.s5` = %s, `eta.cyc` = %s, `W.comp` = %s, `W.turb` = %s, `W.pump` = %s, `W.net` = %s",
        'validation_metrics': "id, `is.con`, `eta.cyc`, `W.net`, `COOLANT.Tmax`, `COOLANT.T1`, `COOLANT.T2`, `COOLANT.T3`, `COOLANT.T4`, `COOLANT.T5`"
    },  
}