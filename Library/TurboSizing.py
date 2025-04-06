import os
import ctREFPROP.ctREFPROP as ct

os.environ['RPPREFIX'] = r'C:\Program Files (x86)\REFPROP'

root = os.environ['RPPREFIX']
RP = ct.REFPROPFunctionLibrary(os.path.join(root, 'REFPRP64.dll'))
RP.SETPATHdll(root)

REF = {
    'iUnits': RP.GETENUMdll(0,'MASS BASE SI')[0],
}

def TURBOMACH_TURB(FLUID_type,FLUID_z,mdot,FLUID_Plow,FLUID_Phigh,eta_turb,T_in,RPM):
    #eta is completely independent of turbomachine sizing
    #isentropic efficiency of the compressor turbomachine (turns out this is completely unneeded for the turbine sizing)
    
    FLUID = { # Creates FLUID dictionary
        'type': FLUID_type,
        'MIX': FLUID_z, # mixture ratios
        'nstates': 2, #number of states needed to be identified for the supercritical working fluid
        'Phigh': FLUID_Phigh, #[Pa], Desired high side pressure exiting from the compressor
        'Plow': FLUID_Plow, #[Pa], Desired low side pressure exiting from the turbine
        'T': [T_in, T_in-300.0] #Initial guessed temperatures at inlet and outlet of turbomachine
    }
    
    FLUID['P'] = [FLUID['Phigh'],FLUID['Plow']] #[Pa], fluid pressure setpoints
    FLUID['h']=[]; FLUID['s']=[] # initializes 'h' and 's' for FLUID
    for ii in range(FLUID['nstates']): # Fills 'h' and 's' for FLUID
        FLUID['h'].append(RP.REFPROPdll(FLUID['type'],'TP','H',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg]
        #FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'TP','S',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][ii],FLUID['h'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        #FLUID['M'] = RP.REFPROPdll(FLUID['type'],'TP','M',REF['iUnits'],1,0,FLUID['T'][0],FLUID['P'][0],FLUID['MIX'])[1][0]

    FLUID['mdot'] = mdot #[kg/s]
    
    # turbine subfunction
    if eta_turb > 1.0:
        print('ERROR: isentropic efficiency of compressor/pump cannot exceed 1')
    else:
        # Ideal
        h2s = RP.REFPROPdll(FLUID['type'],'PS','H',REF['iUnits'],1,0,FLUID['P'][1],FLUID['s'][0],FLUID['MIX'])[1][0] #[J/kg]
        WORK_IDEAL = FLUID['mdot']*(FLUID['h'][0]-h2s) # [W]
        Had = abs(FLUID['h'][0]-h2s) #[J/kg], adiabatic enthlapy difference
        # REAL
        WORK = eta_turb*WORK_IDEAL # [W]
        h2 = FLUID['h'][0] - eta_turb*(FLUID['h'][0]-h2s) # [J/kg]

        # update outlet state
        FLUID['h'][1] = h2
        FLUID['T'][1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][1],FLUID['MIX'])[1][0] #[J/mol-K]

    rho = RP.REFPROPdll(FLUID['type'],'PH','D',REF['iUnits'],1,0,FLUID['P'][0],FLUID['h'][0],FLUID['MIX'])[1][0]
    V_dot = FLUID['mdot']/(rho) #[kg/m^3]
    Ns = RPM*0.10472*(V_dot**(0.5))/(Had**(0.75)) #specific speed
    Ds = 2.056*(Ns**(-0.812)) #spefic diameter
    D = Ds*(V_dot**(0.5))/(Had**(0.25)) #[m], turbine diameter
    mass = 180.0*(D**(2.0)) #[kg], weight of the turbine
    
    output_full = [V_dot,Ns,Ds,D,mass,WORK]
    return[output_full]

def TURBOMACH_COMP(FLUID_type,FLUID_z,mdot,FLUID_Plow,FLUID_Phigh,eta_comp,T_in,RPM):
    #eta is completely indepednet of thne pump sizing
    #isentropic efficiency of the compressor turbomachine (turns out this is completely unneeded for the compressor sizing)
    
    FLUID = { # Creates FLUID dictionary
        'type': FLUID_type,
        'MIX': FLUID_z, # mixture ratios
        'nstates': 2, #number of states needed to be identified for the supercritical working fluid
        'Phigh': FLUID_Phigh, #[Pa], Desired high side pressure exiting from the compressor
        'Plow': FLUID_Plow, #[Pa], Desired low side pressure exiting from the turbine
        'T': [T_in, T_in+300.0] #Initial guessed temperatures at inlet and outlet of turbomachine 
    }

    FLUID['P'] = [FLUID['Plow'],FLUID['Phigh']] #[Pa], fluid pressure setpoints
    FLUID['h']=[]; FLUID['s']=[] # initializes 'h' and 's' for FLUID
    for ii in range(FLUID['nstates']): # Fills 'h' and 's' for FLUID
        FLUID['h'].append(RP.REFPROPdll(FLUID['type'],'TP','H',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg]
        FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'TP','S',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        FLUID['M'] = RP.REFPROPdll(FLUID['type'],'TP','M',REF['iUnits'],1,0,FLUID['T'][0],FLUID['P'][0],FLUID['MIX'])[1][0]

    FLUID['mdot'] = mdot #[kg/s]
    
    # Compressor / Pump Subfunction 
    if eta_comp > 1.0:
        print('ERROR: isentropic efficiency of compressor/pump cannot exceed 1')
    else:
        # Ideal
        h2s = RP.REFPROPdll(FLUID['type'],'PS','H',REF['iUnits'],1,0,FLUID['P'][1],FLUID['s'][0],FLUID['MIX'])[1][0] #[J/kg]
        WORK_IDEAL = FLUID['mdot']*(h2s - FLUID['h'][0]) # [W]
        Had = abs(h2s-FLUID['h'][0]) #[J/kg], adiabatic enthlapy difference
        
        # REAL
        WORK = WORK_IDEAL/eta_comp  # [W]
        h2 = (h2s-FLUID['h'][0])/eta_comp + FLUID['h'][0] # [J/kg]

        # update outlet state
        FLUID['h'][1] = h2
        FLUID['T'][1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][1],FLUID['MIX'])[1][0] #[J/mol-K]

    rho = RP.REFPROPdll(FLUID['type'],'PH','D',REF['iUnits'],1,0,FLUID['P'][0],FLUID['h'][0],FLUID['MIX'])[1][0]
    V_dot = FLUID['mdot']/(rho) #[kg/m^3]
    Ns = RPM*0.10472*(V_dot**(0.5))/(Had**(0.75)) #specific speed
    Ds = 2.719*(Ns**(-1.092)) #spefic diameter
    D = Ds*(V_dot**(0.5))/(Had**(0.25)) #[m], pump diameter
    mass = 180.0*(D**(2.0)) #[kg], weight of the compressor
    
    output_full = [V_dot,Ns,Ds,D,mass,WORK]
    return[output_full]