import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import ctREFPROP.ctREFPROP as ct

import ARC_functions_012324 as cyc

cycle = 'DH_RC' # DH_SRC, DH_SC, IH_SRC, IH_SC

# FLUIDtype = 'CO2'
# FLUIDz = 1
# COOLANTtype = 'Toluene'
# FLUID_mdot = 2.009993
# COOLANTmdot = 9.969646
# FLUIDTMax = 873.076
# # COOLANTTMax = 607.110
# COOLANTTin = 275.9743
# FLUIDPlow = 7.400959
# FLUIDPhigh = 25.01747
# COOLANTPop = 2 # always 2
# etacomp = 0.89306
# etaturb = 0.899863
# etapump = 0.9 # always 0.9
# eps_1 = 0.895754
# eps_2 = 0.899941
# # eps_3 = 0.9

optim_row = 54

match optim_row:
    case 2:
        optim_inputs = [5.253874003,7.467589931,25.02203434,873.2764304,275.2856145,0.899897182,0.899976784,0.898041693,0.899699608,4.194977095]
    case 63:
        optim_inputs = [4.661190199,7.413673825,25.02294802,873.0696651,275.2856145,0.898601635,0.899976784,0.885510175,0.899699608,4.194977095]
    case 54:
        optim_inputs = [7.917179347,7.432444174,25.02234783,873.1238804,276.545554,0.899258336,0.899975358,0.898822952,0.898540083,6.251863572]
    case 1:
        optim_inputs = [17.98834164,7.434392348,25.02238786,873.2307509,275.0152402,0.899583139,0.899989312,0.89863478,0.401923189,9.981689118]
    case 135:
        optim_inputs = [17.98834164,7.434392348,25.02238786,873.2183237,275.0151641,0.899583139,0.899989312,0.89863478,0.405157045,9.981689118]
    case 59:
        optim_inputs = [17.99176735,7.441836342,25.02238786,873.2501593,275.0146677,0.899583139,0.899989312,0.899415987,0.410678962,9.962221328]

FLUIDtype = 'CO2'
FLUIDz = 1
COOLANTtype = 'Toluene'
COOLANTPop = 2 # always 2
etapump = 0.9

FLUID_mdot, FLUIDPlow, FLUIDPhigh, FLUIDTMax, COOLANTTin, etacomp, etaturb, eps_1, eps_2, COOLANTmdot = optim_inputs

if cycle == 'DH_NRC':
    [output_full] = cyc.DH_NRC(FLUIDtype, [FLUIDz], COOLANTtype, FLUID_mdot, COOLANTmdot, FLUIDTMax, COOLANTTin, FLUIDPlow, FLUIDPhigh, COOLANTPop, etacomp, etaturb, etapump, eps_1)
elif cycle == 'DH_RC':
    [output_full] = cyc.DH_RC(FLUIDtype, [FLUIDz], COOLANTtype, FLUID_mdot, COOLANTmdot, FLUIDTMax, COOLANTTin, FLUIDPlow, FLUIDPhigh, COOLANTPop, etacomp, etaturb, etapump, eps_1, eps_2)
# elif cycle == 'IH_NRC':
#     [FLUID, COOLANT, Q_source, eta_cyc, Wcomp, Wturb, Wpump, Wnet, con] = cyc.IH_NRC(FLUIDtype, [FLUIDz], COOLANTtype, FLUID_mdot, COOLANTmdot, COOLANTTMax, COOLANTTin, FLUIDPlow, FLUIDPhigh, COOLANTPop, etacomp, etaturb, etapump, eps_1, eps_2)
# elif cycle == 'IH_RC':
#     [FLUID, COOLANT, Q_source, eta_cyc, Wcomp, Wturb, Wpump, Wnet, con] = cyc.IH_RC(FLUIDtype, [FLUIDz], COOLANTtype, FLUID_mdot, COOLANTmdot, COOLANTTMax, COOLANTTin, FLUIDPlow, FLUIDPhigh, COOLANTPop, etacomp, etaturb, etapump, eps_1, eps_2, eps_3)

FLUID = {
    'T': [0, 0, 0, 0, 0, 0],
    'P': [0, 0, 0, 0, 0, 0],
    'h': [0, 0, 0, 0, 0, 0],
    's': [0, 0, 0, 0, 0, 0],
    'mdot': FLUID_mdot
}
COOLANT = {
    'T': [0, 0, 0],
    'P': [0, 0, 0],
    'h': [0, 0, 0],
    's': [0, 0, 0],
    'mdot': COOLANTmdot
}

if cycle == 'DH_NRC':
    output_full = 0
elif cycle == 'DH_RC':
    con, Q_source, FLUID['T'][0], FLUID['T'][1], FLUID['T'][2], FLUID['T'][3], FLUID['T'][4], FLUID['T'][5], FLUID['P'][0], FLUID['P'][1], FLUID['P'][2], FLUID['P'][3], FLUID['P'][4], FLUID['P'][5], FLUID['h'][0], FLUID['h'][1], FLUID['h'][2], FLUID['h'][3], FLUID['h'][4], FLUID['h'][5], FLUID['s'][0], FLUID['s'][1], FLUID['s'][2], FLUID['s'][3], FLUID['s'][4], FLUID['s'][5], COOLANT['T'][0], COOLANT['T'][1], COOLANT['T'][2], COOLANT['P'][0], COOLANT['P'][1], COOLANT['P'][2], COOLANT['h'][0], COOLANT['h'][1], COOLANT['h'][2], COOLANT['s'][0], COOLANT['s'][1], COOLANT['s'][2], eta_Cyc, Wcomp, Wturb, Wpump, Work_net = output_full

print(f'Cycle type: {cycle}')
print(f'is convergant: {con}\n')

print(f'FLUID: {FLUID}')
print(f'COOLANT: {COOLANT}\n\n')

print(f'FLUID Type: {FLUIDtype}')
print(f'FLUID(T): {FLUID["T"]}')
print(f'FLUID(P): {FLUID["P"]}')
print(f'FLUID(h): {FLUID["h"]}')
print(f'FLUID(s): {FLUID["s"]}')
print(f'FLUID(mdot): {FLUID["mdot"]}\n')

print(f'COOLANT Type: {COOLANTtype}')
print(f'COOLANT(T): {COOLANT["T"]}')
print(f'COOLANT(P): {COOLANT["P"]}')
print(f'COOLANT(h): {COOLANT["h"]}')
print(f'COOLANT(s): {COOLANT["s"]}')
print(f'COOLANT(mdot): {COOLANT["mdot"]}\n')

print(f'Q.source: {Q_source}')
print(f'eta.cyc: {eta_Cyc}')
print(f'W.comp: {Wcomp}')
print(f'W.turb: {Wturb}')
print(f'W.pump: {Wpump}')
print(f'W.net: {Work_net}')