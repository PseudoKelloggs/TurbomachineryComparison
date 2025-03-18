import os
import ctREFPROP.ctREFPROP as ct
#Script comtaining sCO2 Cycle subsystems for referance in cycle code

os.environ['RPPREFIX'] = r'C:\Program Files (x86)\REFPROP'

root = os.environ['RPPREFIX']
RP = ct.REFPROPFunctionLibrary(os.path.join(root, 'REFPRP64.dll'))
RP.SETPATHdll(root)

#Compressor Pump
def Comp_Pump(REF,FLUID,eta,state1,state2,RP): # returns [FLUID,WORK]
    if eta > 1.0:
        print('ERROR: isentropic efficiency of compressor/pump cannot exceed 1')
        return []
    else:
        # Ideal
        h2s = RP.REFPROPdll(FLUID['type'],'PS','H',REF['iUnits'],1,0,FLUID['P'][state2-1],FLUID['s'][state1-1],FLUID['MIX'])[1][0] #[J/mol]
        WORK_IDEAL = FLUID['mdot']*(h2s - FLUID['h'][state1-1]) # [W]
    
        # REAL
        WORK = WORK_IDEAL/eta  # [W]
        h2 = (h2s-FLUID['h'][state1-1])/eta + FLUID['h'][state1-1] # [J/kg]
    
        # update outlet state
        FLUID['h'][state2-1] = h2
        FLUID['T'][state2-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][state2-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][state2-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][state2-1],FLUID['MIX'])[1][0] #[J/mol-K]

        return [FLUID,WORK]

#Fuel Pump
def Fuel_Pump(REF,FLUID,eta,state1,state2,RP): # returns [FLUID,WORK]
    if eta > 1.0:
        print('ERROR: isentropic efficiency of compressor/pump cannot exceed 1')
        return []
    else:
        # Ideal
        h2s = RP.REFPROPdll(FLUID['type'],'PS','H',REF['iUnits'],1,0,FLUID['P'][state2-1],FLUID['s'][state1-1],FLUID['MIX'])[1][0] #[J/mol]
        WORK_IDEAL = FLUID['mdot']*(h2s - FLUID['h'][state1-1]) # [W]
    
        # REAL
        WORK = WORK_IDEAL/eta  # [W]
        h2 = (h2s-FLUID['h'][state1-1])/eta + FLUID['h'][state1-1] # [J/kg]
    
        # update outlet state
        FLUID['h'][state2-1] = h2
        FLUID['T'][state2-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][state2-1],FLUID['MIX'])[1][0] #[K]
        FLUID['s'][state2-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][2-1],FLUID['h'][state2-1],FLUID['MIX'])[1][0] #[J/mol-K]

        return [FLUID,WORK]

# Counterflow heat exchanger
def COUTERFLOW_HEAT_EXCHANGER(REF,FLUIDA,FLUIDB,eps,alpha,stateA1,stateA2,stateB1,stateB2,solvefor): # returns [hAout,hBout]
    #1 -> 2   (stream A) Hot Stream 
    #2 <- 1   (stream B) Cold Stream 
    if eps > 1.0:
        print('ERROR: heat exchanger effectiveness cannot exceed 1')
        return []

    if FLUIDA['T'][stateA1-1] > FLUIDB['T'][stateB1-1]: # check if heat transfer can occur in the present direction
        
        #detrmine possible outlet properties for both stream A and stream B
        hA = RP.REFPROPdll(FLUIDA['type'],'PT','H',REF['iUnits'],1,0,FLUIDA['P'][stateA2-1],FLUIDB['T'][stateB1-1],FLUIDA['MIX'])[1][0] #[J/mol]
        hB = RP.REFPROPdll(FLUIDB['type'],'PT','H',REF['iUnits'],1,0,FLUIDB['P'][stateB2-1],FLUIDA['T'][stateA1-1],FLUIDB['MIX'])[1][0] #[J/mol]
        #determine possible heat transfer from counterflow heat exchanger
        QA = abs(FLUIDA['mdot']*(FLUIDA['h'][stateA1-1] - hA)) #[W]
        QB = abs(FLUIDB['mdot']*(FLUIDB['h'][stateB1-1] - hB)) #[W]

        Qmax = min([QA,QB]) #identify limiting max heat transfer rate 
    
        Q = eps*Qmax #portion of heat transfer actually achieved
        
    else:
        Q = 1
        
    #Solve for actual outlet enthlapies
    
    #hot stream cools down
    hAactual = -(Q/FLUIDA['mdot']) + FLUIDA['h'][stateA1-1] #[J/mol], outlet enthalpy for stream A 
    #cold stream heats up
    hBactual = (Q/FLUIDB['mdot']) + FLUIDB['h'][stateB1-1] #[J/mol], outlet enthalpy for stream B
    
    #update outlet state calculations (under-relaxation?)
    if solvefor == 'Hot':
       hAout =  FLUIDA['h'][stateA2-1] - alpha*(FLUIDA['h'][stateA2-1]-hAactual)
       hBout =  FLUIDB['h'][stateB2-1]
       return [hAout,hBout]
    elif solvefor == 'Cold':
        hAout = FLUIDA['h'][stateA2-1]
        hBout = FLUIDB['h'][stateB2-1] - alpha*(FLUIDB['h'][stateB2-1]-hBactual)
        return [hAout,hBout]
    elif solvefor == 'Both':
       hAout = FLUIDA['h'][stateA2-1] - alpha*(FLUIDA['h'][stateA2-1]-hAactual)
       hBout = FLUIDB['h'][stateB2-1] - alpha*(FLUIDB['h'][stateB2-1]-hBactual)
       return [hAout,hBout]
   
# mass flow rate required for heating in combuster
def COMBUSTION_HEATING(REF,FLUID,eps,alpha,state1,state2,Q_combustion):
    if eps > 1.0:
        print('ERROR: heat exchanger effectiveness cannot exceed 1')
        return []
    
    Q = Q_combustion
    
    hstate1 = FLUID['h'][state1-1]
    hstate2 = FLUID['h'][state2-1]
    
    mdot_req = Q/(hstate2 - hstate1)
    
    if mdot_req <= 0:
        mdot_req = FLUID['mdot']/2 
    
    return mdot_req

#Turbine function
def Turbine(REF,FLUID,eta,state1,state2):
    if eta > 1.0:
        print('ERROR: isentropic efficiency of turbine cannot exceed 1')
        return []
    
    #Ideal
    h2s =  RP.REFPROPdll(FLUID['type'],'PS','H',REF['iUnits'],1,0,FLUID['P'][state2-1],FLUID['s'][state1-1],FLUID['MIX'])[1][0] #[J/mol]
    WORK_IDEAL = FLUID['mdot']*(FLUID['h'][state1-1] - h2s)
    
    #Real
    WORK = eta*WORK_IDEAL #[W]
    h2 = FLUID['h'][state1-1] - eta*(FLUID['h'][state1-1] - h2s)
    
    #update outlet state
    FLUID['h'][state2-1] = h2
    FLUID['T'][state2-1] = RP.REFPROPdll(FLUID['type'],'PH','T',REF['iUnits'],1,0,FLUID['P'][state2-1],FLUID['h'][state2-1],FLUID['MIX'])[1][0] #[K]
    FLUID['s'][state2-1] = RP.REFPROPdll(FLUID['type'],'PH','S',REF['iUnits'],1,0,FLUID['P'][state2-1],FLUID['h'][state2-1],FLUID['MIX'])[1][0] #[J/mol-K]   
    
    return [FLUID,WORK]

       
       
