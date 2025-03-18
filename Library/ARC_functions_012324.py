import os
import ctREFPROP.ctREFPROP as ct
import sCO2_Cycle_Subsystems_082323 as subsys

os.environ['RPPREFIX'] = r'C:\Program Files (x86)\REFPROP'

root = os.environ['RPPREFIX']
RP = ct.REFPROPFunctionLibrary(os.path.join(root, 'REFPRP64.dll'))
RP.SETPATHdll(root)

REF = {
    'iUnits': RP.GETENUMdll(0,'MASS BASE SI')[0],
}

def DH_RC(FLUID_type,FLUID_z,COOLANT_type,FLUID_mdot,COOLANT_mdot,FLUID_TMax,COOLANT_Tin,FLUID_Plow,FLUID_Phigh,COOLANT_Pop,eta_comp,eta_turb,eta_pump,eps_1,eps_2):
    
    COOLANT = { # Creates COOLANT dictionary
    'type': COOLANT_type,
    'MIX': [1], # mixture ratios
    'nstates': 3, #number of states needed to be identified for the Coolant
    'Pset': COOLANT_Pop*1e6, #[Pa], Coolant pressure (assume constant)
    'T': [COOLANT_Tin,COOLANT_Tin+10,320.0]  #[K], initial guesses for temperature for states of cooolant
    }

    COOLANT['P'] = [101320,COOLANT['Pset'],COOLANT['Pset']] #[Pa], fuel pressure setpoints
    COOLANT['h']=[]; COOLANT['s']=[] # initializes 'h' and 's' for COOLANT
    for ii in range(COOLANT['nstates']): # Fills 'h' and 's' for COOLANT
        COOLANT['h'].append(RP.REFPROPdll(COOLANT['type'],'TP','H',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol]
        COOLANT['s'].append(RP.REFPROPdll(COOLANT['type'],'TP','S',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol-K]
        COOLANT['M'] = RP.REFPROPdll(COOLANT['type'],'TP','M',REF['iUnits'],1,0,COOLANT['T'][0],COOLANT['P'][0],COOLANT['MIX'])[1][0]

    FLUID = { # Creates FLUID dictionary
        'type': FLUID_type,
        'MIX': FLUID_z, # mixture ratios
        'nstates': 6, #number of states needed to be identified for the supercritical working fluid
        'Phigh': FLUID_Phigh*1e6, #[Pa], Desired high side pressure exiting from the compressor
        'Plow': FLUID_Plow*1e6, #[Pa], Desired low side pressure exiting from the turbine
        'T': [315.0,400.0,500.0,FLUID_TMax,FLUID_TMax-50.0,400.0] #Initial guessed temperature distribution for the cycle 
    }

    #heat exchanger performance
    dP_max = 100.0*1e3 #[Pa], tolerable pressure drop through each heat exchanger for working fluid.

    FLUID['P'] = [FLUID['Plow'],FLUID['Phigh'],FLUID['Phigh']-1*dP_max,FLUID['Phigh']-2*dP_max,FLUID['Plow']+2*dP_max,FLUID['Plow']+1*dP_max] #[kPa], fluid pressure setpoints
    FLUID['h']=[]; FLUID['s']=[] # initializes 'h' and 's' for FLUID
    for ii in range(FLUID['nstates']): # Fills 'h' and 's' for FLUID
        FLUID['h'].append(RP.REFPROPdll(FLUID['type'],'TP','H',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg]
        FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'TP','S',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        FLUID['M'] = RP.REFPROPdll(FLUID['type'],'TP','M',REF['iUnits'],1,0,FLUID['T'][0],FLUID['P'][0],FLUID['MIX'])[1][0]

    #Solution Settings
    alpha = 0.8 #under-relaxation factor used in updating properties of interest
    tol = 0.1 #[K], maximum allowable temperature tolerancing for cycle solution

    FLUID['mdot'] = FLUID_mdot
    COOLANT['mdot'] = COOLANT_mdot

    [COOLANT,Wpump] = subsys.Fuel_Pump(REF,COOLANT,eta_pump,1,2,RP)
    
    c = []
    con = 0
    flagcon1 = 0
    count1 = 0
    EB = []
    while flagcon1 < 1:
        count1 += 1

        Tcurrent = FLUID['T']
        
        # state 1->2 Compressor w/ isentropic efficiency
        [FLUID,Wcomp] = subsys.Comp_Pump(REF,FLUID,eta_comp,1,2,RP)
        Wcompcheck = FLUID['mdot']*(FLUID['h'][2-1] - FLUID['h'][1-1])
            
        # state 2->3, high pressure side of recuperator
        # HOT , COLD
        [FLUID['h'][6-1],FLUID['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,FLUID,eps_2,alpha,5,6,2,3,'Both')
            
        FLUID['T'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        FLUID['T'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        # state 3->4, Heating in combustion chamber walls
        Q_source = FLUID['mdot']*(FLUID['h'][4-1] - FLUID['h'][3-1])
        
        # state 4->5 Turbine w/ isentropic efficiency
        [FLUID,Wturb] = subsys.Turbine(REF,FLUID,eta_turb,4,5)
        Wturbcheck = FLUID['mdot']*(FLUID['h'][4-1] - FLUID['h'][5-1])
            
        # state 5->6, low pressure side of recuperator
        # HOT , COLD
        [FLUID['h'][6-1],FLUID['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,FLUID,eps_2,alpha,5,6,2,3,'Both')
        
        FLUID['T'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        FLUID['T'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        # state 6->1, CO2 side of heat rejection heat exchanger
        # HOT , COLD
        [FLUID['h'][1-1],COOLANT['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,COOLANT,eps_1,alpha,6,1,2,3,'Both')
        
        FLUID['T'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        COOLANT['T'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','T',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[K]
        COOLANT['s'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','S',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[J/mol-K]
        
        Q_out = COOLANT['mdot']*(COOLANT['h'][3-1]-COOLANT['h'][2-1])
            
        # Cycle Efficiency
        eta_Cyc = (Wturb-Wcomp)/Q_source
        eta_Carnot = 1 - (min(FLUID['T'])/(max(FLUID['T'])))
        
        # Find the maximum difference between the changes in temperature
        diffT = []       
        for ii in range(len(FLUID['T'])):
            diffT.append(abs(FLUID['T'][ii]-Tcurrent[ii]))
        maxdiffT = max(diffT)
        
        # Energy Balance (cycle)
        EB.append(abs(Q_source+Wcomp-Wturb-Q_out))
        
        #print(EB[count1-1])
        #print(count1-1)
        
        if (maxdiffT < tol and EB[count1-1] < 1e-4):
                flagcon1 = 1
                c.append(count1)
                con = 1 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
        if (count1 > 200):
                flagcon1 = 1
                c.append(count1)
                con = 0 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        Work_net = Wturb - Wcomp
    
    output_full = [
    con, Q_source,
    FLUID['T'][0], FLUID['T'][1], FLUID['T'][2], FLUID['T'][3], FLUID['T'][4], FLUID['T'][5],
    FLUID['P'][0], FLUID['P'][1], FLUID['P'][2], FLUID['P'][3], FLUID['P'][4], FLUID['P'][5],
    FLUID['h'][0], FLUID['h'][1], FLUID['h'][2], FLUID['h'][3], FLUID['h'][4], FLUID['h'][5],
    FLUID['s'][0], FLUID['s'][1], FLUID['s'][2], FLUID['s'][3], FLUID['s'][4], FLUID['s'][5],
    COOLANT['T'][0], COOLANT['T'][1], COOLANT['T'][2],
    COOLANT['P'][0], COOLANT['P'][1], COOLANT['P'][2],
    COOLANT['h'][0], COOLANT['h'][1], COOLANT['h'][2],
    COOLANT['s'][0], COOLANT['s'][1], COOLANT['s'][2],
    eta_Cyc, Wcomp, Wturb, Wpump, Work_net
    ]
    
    #return[FLUID,COOLANT,Q_source,eta_Cyc,Wcomp,Wturb,Wpump,Work_net,con]
    return[output_full]



def DH_NRC(FLUID_type,FLUID_z,COOLANT_type,FLUID_mdot,COOLANT_mdot,FLUID_TMax,COOLANT_Tin,FLUID_Plow,FLUID_Phigh,COOLANT_Pop,eta_comp,eta_turb,eta_pump,eps_1):
    
    COOLANT = { # Creates COOLANT dictionary
    'type': COOLANT_type,
    'MIX': [1], # mixture ratios
    'nstates': 3, #number of states needed to be identified for the Coolant
    'Pset': COOLANT_Pop*1e6, #[Pa], Coolant pressure (assume constant)
    'T': [COOLANT_Tin,COOLANT_Tin+10,320.0]  #[K], initial guesses for temperature for states of cooolant
    }

    COOLANT['P'] = [101320,COOLANT['Pset'],COOLANT['Pset']] #[Pa], fuel pressure setpoints
    COOLANT['h']=[]; COOLANT['s']=[] # initializes 'h' and 's' for COOLANT
    for ii in range(COOLANT['nstates']): # Fills 'h' and 's' for COOLANT
        COOLANT['h'].append(RP.REFPROPdll(COOLANT['type'],'TP','H',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol]
        COOLANT['s'].append(RP.REFPROPdll(COOLANT['type'],'TP','S',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol-K]
        COOLANT['M'] = RP.REFPROPdll(COOLANT['type'],'TP','M',REF['iUnits'],1,0,COOLANT['T'][0],COOLANT['P'][0],COOLANT['MIX'])[1][0]

    FLUID = { # Creates FLUID dictionary
        'type': FLUID_type,
        'MIX': FLUID_z, # mixture ratios
        'nstates': 4, #number of states needed to be identified for the supercritical working fluid
        'Phigh': FLUID_Phigh*1e6, #[Pa], Desired high side pressure exiting from the compressor
        'Plow': FLUID_Plow*1e6, #[Pa], Desired low side pressure exiting from the turbine
        'T': [315.0,400.0,FLUID_TMax,FLUID_TMax-100.0] #Initial guessed temperature distribution for the cycle 
    }

    #heat exchanger performance
    dP_max = 100.0*1e3 #[Pa], tolerable pressure drop through each heat exchanger for working fluid.

    FLUID['P'] = [FLUID['Plow'],FLUID['Phigh'],FLUID['Phigh']-2*dP_max,FLUID['Plow']+1*dP_max] #[kPa], fluid pressure setpoints
    FLUID['h']=[]; FLUID['s']=[] # initializes 'h' and 's' for FLUID
    for ii in range(FLUID['nstates']): # Fills 'h' and 's' for FLUID
        FLUID['h'].append(RP.REFPROPdll(FLUID['type'],'TP','H',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg]
        FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'TP','S',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        FLUID['M'] = RP.REFPROPdll(FLUID['type'],'TP','M',REF['iUnits'],1,0,FLUID['T'][0],FLUID['P'][0],FLUID['MIX'])[1][0]

    #Solution Settings
    alpha = 0.8 #under-relaxation factor used in updating properties of interest
    tol = 0.1 #[K], maximum allowable temperature tolerancing for cycle solution

    FLUID['mdot'] = FLUID_mdot
    COOLANT['mdot'] = COOLANT_mdot

    [COOLANT,Wpump] = subsys.Fuel_Pump(REF,COOLANT,eta_pump,1,2,RP)
    
    c = []
    con = 0
    flagcon1 = 0
    count1 = 0
    EB = []
    while flagcon1 < 1:
        count1 += 1

        Tcurrent = FLUID['T']
        
        # state 1->2 Compressor w/ isentropic efficiency
        [FLUID,Wcomp] = subsys.Comp_Pump(REF,FLUID,eta_comp,1,2,RP)
        Wcompcheck = FLUID['mdot']*(FLUID['h'][2-1] - FLUID['h'][1-1])
            
        # state 2->3, Heating in combustion chamber walls
        Q_source = FLUID['mdot']*(FLUID['h'][3-1] - FLUID['h'][2-1])
        
        # state 3->4 Turbine w/ isentropic efficiency
        [FLUID,Wturb] = subsys.Turbine(REF,FLUID,eta_turb,3,4)
        Wturbcheck = FLUID['mdot']*(FLUID['h'][3-1] - FLUID['h'][4-1])
        
        # state 4->1, CO2 side of heat rejection heat exchanger
        # HOT , COLD
        [FLUID['h'][1-1],COOLANT['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,COOLANT,eps_1,alpha,4,1,2,3,'Both')
        
        FLUID['T'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        COOLANT['T'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','T',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[K]
        COOLANT['s'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','S',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[J/mol-K]
        
        Q_out = COOLANT['mdot']*(COOLANT['h'][3-1]-COOLANT['h'][2-1])
            
        # Cycle Efficiency
        eta_Cyc = (Wturb-Wcomp)/Q_source
        eta_Carnot = 1 - (min(FLUID['T'])/(max(FLUID['T'])))
        
        # Find the maximum difference between the changes in temperature
        diffT = []       
        for ii in range(len(FLUID['T'])):
            diffT.append(abs(FLUID['T'][ii]-Tcurrent[ii]))
        maxdiffT = max(diffT)
        
        # Energy Balance (cycle)
        EB.append(abs(Q_source+Wcomp-Wturb-Q_out))
        
        #print(EB[count1-1])
        #print(count1-1)
        
        if (maxdiffT < tol and EB[count1-1] < 1e-4):
                flagcon1 = 1
                c.append(count1)
                con = 1 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
        if (count1 > 200):
                flagcon1 = 1
                c.append(count1)
                con = 0 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        Work_net = Wturb - Wcomp
    
    output_full = [
    con, Q_source,
    FLUID['T'][0], FLUID['T'][1], FLUID['T'][2], FLUID['T'][3],
    FLUID['P'][0], FLUID['P'][1], FLUID['P'][2], FLUID['P'][3],
    FLUID['h'][0], FLUID['h'][1], FLUID['h'][2], FLUID['h'][3],
    FLUID['s'][0], FLUID['s'][1], FLUID['s'][2], FLUID['s'][3],
    COOLANT['T'][0], COOLANT['T'][1], COOLANT['T'][2],
    COOLANT['P'][0], COOLANT['P'][1], COOLANT['P'][2],
    COOLANT['h'][0], COOLANT['h'][1], COOLANT['h'][2],
    COOLANT['s'][0], COOLANT['s'][1], COOLANT['s'][2],
    eta_Cyc, Wcomp, Wturb, Wpump, Work_net]
    #return[FLUID,COOLANT,Q_source,eta_Cyc,Wcomp,Wturb,Wpump,Work_net,con]
    return[output_full]

def IH_RC(FLUID_type,FLUID_z,COOLANT_type,FLUID_mdot,COOLANT_mdot,COOLANT_TMax,COOLANT_Tin,FLUID_Plow,FLUID_Phigh,COOLANT_Pop,eta_comp,eta_turb,eta_pump,eps_1,eps_2,eps_3):
    
    #heat exchanger performance
    dP_max = 100.0*1e3 #[Pa], tolerable pressure drop through each heat exchanger for working fluid.
    
    COOLANT = { # Creates COOLANT dictionary
    'type': COOLANT_type,
    'MIX': [1], # mixture ratios
    'nstates': 5, #number of states needed to be identified for the Coolant
    'Pset': COOLANT_Pop*1e6, #[Pa], Coolant pressure (assume constant)
    'T': [COOLANT_Tin,COOLANT_Tin+10,340.0,COOLANT_TMax,COOLANT_TMax-100.0]  #[K], initial guesses for temperature for states of cooolant
    }

    COOLANT['P'] = [101320,COOLANT['Pset'],COOLANT['Pset'],COOLANT['Pset']-1*dP_max,COOLANT['Pset']-2*dP_max] #[Pa], fuel pressure setpoints
    COOLANT['h']=[]; COOLANT['s']=[] # initializes 'h' and 's' for COOLANT
    for ii in range(COOLANT['nstates']): # Fills 'h' and 's' for COOLANT
        COOLANT['h'].append(RP.REFPROPdll(COOLANT['type'],'TP','H',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol]
        COOLANT['s'].append(RP.REFPROPdll(COOLANT['type'],'TP','S',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol-K]
        COOLANT['M'] = RP.REFPROPdll(COOLANT['type'],'TP','M',REF['iUnits'],1,0,COOLANT['T'][0],COOLANT['P'][0],COOLANT['MIX'])[1][0]

    FLUID = { # Creates FLUID dictionary
        'type': FLUID_type,
        'MIX': FLUID_z, # mixture ratios
        'nstates': 6, #number of states needed to be identified for the supercritical working fluid
        'Phigh': FLUID_Phigh*1e6, #[Pa], Desired high side pressure exiting from the compressor
        'Plow': FLUID_Plow*1e6, #[Pa], Desired low side pressure exiting from the turbine
        'T': [315.0,400.0,500.0,600.0,550.0,400.0] #Initial guessed temperature distribution for the cycle 
    }

    FLUID['P'] = [FLUID['Plow'],FLUID['Phigh'],FLUID['Phigh']-1*dP_max,FLUID['Phigh']-2*dP_max,FLUID['Plow']+2*dP_max,FLUID['Plow']+1*dP_max] #[kPa], fluid pressure setpoints
    FLUID['h']=[]; FLUID['s']=[] # initializes 'h' and 's' for FLUID
    for ii in range(FLUID['nstates']): # Fills 'h' and 's' for FLUID
        FLUID['h'].append(RP.REFPROPdll(FLUID['type'],'TP','H',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg]
        FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'TP','S',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        FLUID['M'] = RP.REFPROPdll(FLUID['type'],'TP','M',REF['iUnits'],1,0,FLUID['T'][0],FLUID['P'][0],FLUID['MIX'])[1][0]

    #Solution Settings
    alpha = 0.8 #under-relaxation factor used in updating properties of interest
    tol = 0.1 #[K], maximum allowable temperature tolerancing for cycle solution

    FLUID['mdot'] = FLUID_mdot
    COOLANT['mdot'] = COOLANT_mdot

    [COOLANT,Wpump] = subsys.Fuel_Pump(REF,COOLANT,eta_pump,1,2,RP)
    
    c = []
    con = 0
    flagcon1 = 0
    count1 = 0
    EB = []
    while flagcon1 < 1:
        count1 += 1

        Tcurrent = FLUID['T']
        
        # state 1->2 Compressor w/ isentropic efficiency
        [FLUID,Wcomp] = subsys.Comp_Pump(REF,FLUID,eta_comp,1,2,RP)
        Wcompcheck = FLUID['mdot']*(FLUID['h'][2-1] - FLUID['h'][1-1])
        
        # state 2->3, high pressure side of recuperator
        # HOT , COLD
        [FLUID['h'][6-1],FLUID['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,FLUID,eps_3,alpha,5,6,2,3,'Both')
            
        FLUID['T'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        FLUID['T'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        # state 3->4  , FLUID heating in eps_2 from COOLANT
        Q_source = COOLANT['mdot']*(COOLANT['h'][4-1] - COOLANT['h'][3-1])
        
        [COOLANT['h'][5-1],FLUID['h'][4-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,COOLANT,FLUID,eps_2,alpha,4,5,3,4,'Both')
        
        COOLANT['T'][5-1] = RP.REFPROPdll(COOLANT['type'],'PH','T',REF['iUnits'],1,0,COOLANT['P'][5-1],COOLANT['h'][5-1],COOLANT['MIX'])[1][0] #[K]
        COOLANT['s'][5-1] = RP.REFPROPdll(COOLANT['type'],'PH','S',REF['iUnits'],1,0,COOLANT['P'][5-1],COOLANT['h'][5-1],COOLANT['MIX'])[1][0] #[J/mol-K]
        
        FLUID['T'][4-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][4-1],FLUID['h'][4-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][4-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][4-1],FLUID['h'][4-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        Q_in = COOLANT['mdot']*(COOLANT['h'][4-1]-COOLANT['h'][5-1])
        
        # state 4->5 Turbine w/ isentropic efficiency
        [FLUID,Wturb] = subsys.Turbine(REF,FLUID,eta_turb,4,5)
        Wturbcheck = FLUID['mdot']*(FLUID['h'][4-1] - FLUID['h'][5-1])
            
        # state 5->6, low pressure side of recuperator
        # HOT , COLD
        [FLUID['h'][6-1],FLUID['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,FLUID,eps_3,alpha,5,6,2,3,'Both')
        
        FLUID['T'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][6-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][6-1],FLUID['h'][6-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        FLUID['T'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        Q_check_hx3 = FLUID['mdot']*(FLUID['h'][5-1]-FLUID['h'][3-1])
        
        # state 6->1, CO2 side of heat rejection heat exchanger
        # HOT , COLD
        [FLUID['h'][1-1],COOLANT['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,COOLANT,eps_1,alpha,6,1,2,3,'Both')
        
        FLUID['T'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        COOLANT['T'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','T',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[K]
        COOLANT['s'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','S',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[J/mol-K]
        
        Q_out = COOLANT['mdot']*(COOLANT['h'][3-1]-COOLANT['h'][2-1])
            
        # Cycle Efficiency
        eta_Cyc = (Wturb-Wcomp)/Q_source
        eta_Carnot = 1 - (min(FLUID['T'])/(max(FLUID['T'])))
        
        # Find the maximum difference between the changes in temperature
        diffT = []       
        for ii in range(len(FLUID['T'])):
            diffT.append(abs(FLUID['T'][ii]-Tcurrent[ii]))
        maxdiffT = max(diffT)
        
        # Energy Balance (cycle)
        EB.append(abs(Q_in+Wcomp-Wturb-Q_out))
        
        #print(EB[count1-1])
        #print(count1-1)
        
        if (maxdiffT < tol and EB[count1-1] < 1e-4):
                flagcon1 = 1
                c.append(count1)
                con = 1 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
        if (count1 > 200):
                flagcon1 = 1
                c.append(count1)
                con = 0
        
        Work_net = Wturb - Wcomp
    
    output_full = [
    con, Q_source,
    FLUID['T'][0], FLUID['T'][1], FLUID['T'][2], FLUID['T'][3],
    FLUID['P'][0], FLUID['P'][1], FLUID['P'][2], FLUID['P'][3],
    FLUID['h'][0], FLUID['h'][1], FLUID['h'][2], FLUID['h'][3],
    FLUID['s'][0], FLUID['s'][1], FLUID['s'][2], FLUID['s'][3],
    COOLANT['T'][0], COOLANT['T'][1], COOLANT['T'][2], COOLANT['T'][3], COOLANT['T'][4],
    COOLANT['P'][0], COOLANT['P'][1], COOLANT['P'][2], COOLANT['P'][3], COOLANT['P'][4],
    COOLANT['h'][0], COOLANT['h'][1], COOLANT['h'][2], COOLANT['h'][3], COOLANT['h'][4],
    COOLANT['s'][0], COOLANT['s'][1], COOLANT['s'][2], COOLANT['s'][3], COOLANT['s'][4],
    eta_Cyc, Wcomp, Wturb, Wpump, Work_net
    ]
    #return[FLUID,COOLANT,Q_source,eta_Cyc,Wcomp,Wturb,Wpump,Work_net,con]
    return[output_full]

def IH_NRC(FLUID_type,FLUID_z,COOLANT_type,FLUID_mdot,COOLANT_mdot,COOLANT_TMax,COOLANT_Tin,FLUID_Plow,FLUID_Phigh,COOLANT_Pop,eta_comp,eta_turb,eta_pump,eps_1,eps_2):
    
    #heat exchanger performance
    dP_max = 100.0*1e3 #[Pa], tolerable pressure drop through each heat exchanger for working fluid.
    
    COOLANT = { # Creates COOLANT dictionary
    'type': COOLANT_type,
    'MIX': [1], # mixture ratios
    'nstates': 5, #number of states needed to be identified for the Coolant
    'Pset': COOLANT_Pop*1e6, #[Pa], Coolant pressure (assume constant)
    'T': [COOLANT_Tin,COOLANT_Tin+10,340.0,COOLANT_TMax,COOLANT_TMax-100.0]  #[K], initial guesses for temperature for states of cooolant
    }

    COOLANT['P'] = [101320,COOLANT['Pset'],COOLANT['Pset'],COOLANT['Pset']-1*dP_max,COOLANT['Pset']-2*dP_max] #[Pa], fuel pressure setpoints
    COOLANT['h']=[]; COOLANT['s']=[] # initializes 'h' and 's' for COOLANT
    for ii in range(COOLANT['nstates']): # Fills 'h' and 's' for COOLANT
        COOLANT['h'].append(RP.REFPROPdll(COOLANT['type'],'TP','H',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol]
        COOLANT['s'].append(RP.REFPROPdll(COOLANT['type'],'TP','S',REF['iUnits'],1,0,COOLANT['T'][ii],COOLANT['P'][ii],COOLANT['MIX'])[1][0]) #[J/mol-K]
        COOLANT['M'] = RP.REFPROPdll(COOLANT['type'],'TP','M',REF['iUnits'],1,0,COOLANT['T'][0],COOLANT['P'][0],COOLANT['MIX'])[1][0]

    FLUID = { # Creates FLUID dictionary
        'type': FLUID_type,
        'MIX': FLUID_z, # mixture ratios
        'nstates': 4, #number of states needed to be identified for the supercritical working fluid
        'Phigh': FLUID_Phigh*1e6, #[Pa], Desired high side pressure exiting from the compressor
        'Plow': FLUID_Plow*1e6, #[Pa], Desired low side pressure exiting from the turbine
        'T': [315.0,400.0,500.0,400.0] #Initial guessed temperature distribution for the cycle 
    }

    FLUID['P'] = [FLUID['Plow']+1*dP_max,FLUID['Phigh'],FLUID['Phigh']-1*dP_max,FLUID['Plow']] #[kPa], fluid pressure setpoints
    FLUID['h']=[]; FLUID['s']=[] # initializes 'h' and 's' for FLUID
    for ii in range(FLUID['nstates']): # Fills 'h' and 's' for FLUID
        FLUID['h'].append(RP.REFPROPdll(FLUID['type'],'TP','H',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg]
        FLUID['s'].append(RP.REFPROPdll(FLUID['type'],'TP','S',REF['iUnits'],1,0,FLUID['T'][ii],FLUID['P'][ii],FLUID['MIX'])[1][0]) #[J/kg-K]
        FLUID['M'] = RP.REFPROPdll(FLUID['type'],'TP','M',REF['iUnits'],1,0,FLUID['T'][0],FLUID['P'][0],FLUID['MIX'])[1][0]

    #Solution Settings
    alpha = 0.8 #under-relaxation factor used in updating properties of interest
    tol = 0.1 #[K], maximum allowable temperature tolerancing for cycle solution

    FLUID['mdot'] = FLUID_mdot
    COOLANT['mdot'] = COOLANT_mdot

    [COOLANT,Wpump] = subsys.Fuel_Pump(REF,COOLANT,eta_pump,1,2,RP)
    
    c = []
    con = 0
    flagcon1 = 0
    count1 = 0
    EB = []
    while flagcon1 < 1:
        count1 += 1

        Tcurrent = FLUID['T']
        
        # state 1->2 Compressor w/ isentropic efficiency
        [FLUID,Wcomp] = subsys.Comp_Pump(REF,FLUID,eta_comp,1,2,RP)
        Wcompcheck = FLUID['mdot']*(FLUID['h'][2-1] - FLUID['h'][1-1])
        
        # state 2->3  , FLUID heating in eps_2 from COOLANT
        Q_source = COOLANT['mdot']*(COOLANT['h'][4-1] - COOLANT['h'][3-1])
        
        [COOLANT['h'][5-1],FLUID['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,COOLANT,FLUID,eps_2,alpha,4,5,2,3,'Both')
        
        COOLANT['T'][5-1] = RP.REFPROPdll(COOLANT['type'],'PH','T',REF['iUnits'],1,0,COOLANT['P'][5-1],COOLANT['h'][5-1],COOLANT['MIX'])[1][0] #[K]
        COOLANT['s'][5-1] = RP.REFPROPdll(COOLANT['type'],'PH','S',REF['iUnits'],1,0,COOLANT['P'][5-1],COOLANT['h'][5-1],COOLANT['MIX'])[1][0] #[J/mol-K]
        
        FLUID['T'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][3-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][3-1],FLUID['h'][3-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        Q_in = COOLANT['mdot']*(COOLANT['h'][4-1]-COOLANT['h'][5-1])
        
        # state 3->4 Turbine w/ isentropic efficiency
        [FLUID,Wturb] = subsys.Turbine(REF,FLUID,eta_turb,3,4)
        Wturbcheck = FLUID['mdot']*(FLUID['h'][3-1] - FLUID['h'][4-1])
        
        # state 4->1, CO2 side of heat rejection heat exchanger
        # HOT , COLD
        [FLUID['h'][1-1],COOLANT['h'][3-1]] = subsys.COUTERFLOW_HEAT_EXCHANGER(REF,FLUID,COOLANT,eps_1,alpha,4,1,2,3,'Both')
        
        FLUID['T'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][1-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][1-1],FLUID['h'][1-1],FLUID['MIX'])[1][0] #[J/mol-K]
        
        COOLANT['T'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','T',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[K]
        COOLANT['s'][3-1] = RP.REFPROPdll(COOLANT['type'],'PH','S',REF['iUnits'],1,0,COOLANT['P'][3-1],COOLANT['h'][3-1],COOLANT['MIX'])[1][0] #[J/mol-K]
        
        Q_out = COOLANT['mdot']*(COOLANT['h'][3-1]-COOLANT['h'][2-1])
            
        # Cycle Efficiency
        eta_Cyc = (Wturb-Wcomp)/Q_source
        eta_Carnot = 1 - (min(FLUID['T'])/(max(FLUID['T'])))
        
        # Find the maximum difference between the changes in temperature
        diffT = []       
        for ii in range(len(FLUID['T'])):
            diffT.append(abs(FLUID['T'][ii]-Tcurrent[ii]))
        maxdiffT = max(diffT)
        
        # Energy Balance (cycle)
        EB.append(abs(Q_in+Wcomp-Wturb-Q_out))
        
        #print(EB[count1-1])
        #print(count1-1)
        
        if (maxdiffT < tol and EB[count1-1] < 1e-4):
                flagcon1 = 1
                c.append(count1)
                con = 1 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
        if (count1 > 200):
                flagcon1 = 1
                c.append(count1)
                con = 0 #con!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        Work_net = Wturb - Wcomp
    
    output_full = [
    con, Q_source,
    FLUID['T'][0], FLUID['T'][1], FLUID['T'][2], FLUID['T'][3], FLUID['T'][4], FLUID['T'][5],
    FLUID['P'][0], FLUID['P'][1], FLUID['P'][2], FLUID['P'][3], FLUID['P'][4], FLUID['P'][5],
    FLUID['h'][0], FLUID['h'][1], FLUID['h'][2], FLUID['h'][3], FLUID['h'][4], FLUID['h'][5],
    FLUID['s'][0], FLUID['s'][1], FLUID['s'][2], FLUID['s'][3], FLUID['s'][4], FLUID['s'][5],
    COOLANT['T'][0], COOLANT['T'][1], COOLANT['T'][2], COOLANT['T'][3], COOLANT['T'][4],
    COOLANT['P'][0], COOLANT['P'][1], COOLANT['P'][2], COOLANT['P'][3], COOLANT['P'][4],
    COOLANT['h'][0], COOLANT['h'][1], COOLANT['h'][2], COOLANT['h'][3], COOLANT['h'][4],
    COOLANT['s'][0], COOLANT['s'][1], COOLANT['s'][2], COOLANT['s'][3], COOLANT['s'][4],
    eta_Cyc, Wcomp, Wturb, Wpump, Work_net]
    #return[FLUID,COOLANT,Q_source,eta_Cyc,Wcomp,Wturb,Wpump,Work_net,con]
    return[output_full]