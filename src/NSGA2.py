import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from keras import models
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.visualization.petal import Petal
from pymoo.operators.selection.rnd import RandomSelection
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pymoo.mcdm.pseudo_weights import PseudoWeights
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.pcp import PCP
from pymoo.mcdm.high_tradeoff import HighTradeoffPoints
from pymoo.util.reference_direction import UniformReferenceDirectionFactory

# custom metric function
def rmse(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))

# Register the custom metric function in the custom object scope
keras.utils.get_custom_objects().update({"rmse": rmse})

# Load your pre-trained models
optim_case = 1
# Case 1: DH_RC (eta.cyc), turb (mass), comp (mass)
# Case 2: DH_NRC (eta.cyc), turb (mass), comp (mass)
# Case 3: IH_RC (eta.cyc), turb (mass), comp (mass)
# Case 4: IH_NRC (eta.cyc), turb (mass), comp (mass)
# Case 5: DH_RC (eta.cyc), turb (mass), comp (mass) #  

# Population size
n = 1000

if optim_case == 1:
    obj1_model = models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\DH_RC_model_eta.h5") # DH_RC model, eta.cyc
    obj2_model = models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\turb_model_mass.h5") # turbine model, mass.turb
    obj3_model = models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\comp_model_mass.h5") # compressor model, mass.comp
    tag = 'case1'
    tag_full = 'DH_RC_etacyc_turbmass_compmass'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    cycle = 'DH_RC'
    obj1_norm_params = "normalization_parameters/normalization_params_DH_RC_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "FLUID.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "eta.comp", "eta.turb", "eps.1", "eps.2", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]
elif optim_case == 2:
    obj1_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\DH_NRC_model_eta.h5") # DH_NRC model, eta.cyc
    obj2_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\turb_model_mass.h5") # turbine model, mass.turb
    obj3_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\comp_model_mass.h5") # compressor model, mass.comp
    tag = 'case2'
    tag_full = 'DH_NRC_etacyc_turbmass_compmass'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    cycle = 'DH_NRC'
    obj1_norm_params = "normalization_parameters/normalization_params_DH_NRC_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "FLUID.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "eta.comp", "eta.turb", "eps.1", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]
elif optim_case == 3:
    obj1_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\IH_RC_model_eta.h5") # IH_RC model, eta.cyc
    obj2_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\turb_model_mass.h5") # turbine model, mass.turb
    obj3_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\comp_model_mass.h5") # compressor model, mass.comp
    tag = 'case3'
    tag_full = 'IH_RC_etacyc_turbmass_compmass'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    cycle = 'IH_RC'
    obj1_norm_params = "normalization_parameters/normalization_params_IH_RC_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "COOLANT.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "FLUID.T4", "eta.comp", "eta.turb", "eps.1", "eps.2", "eps.3", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]
elif optim_case == 4:
    obj1_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\IH_NRC_model_eta.h5") # IH_NRC model, eta.cyc
    obj2_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\turb_model_mass.h5") # turbine model, mass.turb
    obj3_model = tf.keras.models.load_model(r"C:\Users\hylandc2\Documents\Research\Code\Current\saved_models\comp_model_mass.h5") # compressor model, mass.comp
    tag = 'case4'
    tag_full = 'IH_NRC_etacyc_turbmass_compmass'
    cycle = 'IH_NRC'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    obj1_norm_params = "normalization_parameters/normalization_params_IH_NRC_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "COOLANT.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "FLUID.T3", "eta.comp", "eta.turb", "eps.1", "eps.2", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]

# Cycle parameters `DH_RC`: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`FLUID.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`eta.comp`,`eta.turb`,`eps.1`,`eps.2`,`COOLANT.mdot`,`eta.cyc`"
# Cycle parameters `DH_NRC`: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`FLUID.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`eta.comp`,`eta.turb`,`eps.1`,`COOLANT.mdot`,`eta.cyc`"
# Cycle parameters `IH_RC`: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`COOLANT.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`FLUID.T4`,`eta.comp`,`eta.turb`,`eps.1`,`eps.2`,`eps.3`,`COOLANT.mdot`,`eta.cyc`"
# Cycle parameters `IH_NRC`: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`COOLANT.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`FLUID.T3`,`eta.comp`,`eta.turb`,`eps.1`,`eps.2`,`COOLANT.mdot`,`eta.cyc`"

# Turbine parameters: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`eta.turb`,`FLUID.Tin_turb`(FLUID.TMax/FLUID.T4/3),`RPM`,`mass.turb`,`W.turb`"
# Compressor parameters: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`eta.comp`,`FLUID.Tin_comp(FLUID.T1)`,`RPM`,`mass.comp`,`W.comp`"

# Combined parameters case 1: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`FLUID.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`eta.comp`,`eta.turb`,`eps.1`,`eps.2`,`COOLANT.mdot`,`RPM`,`W.turb`,`W.comp`"
# Combined parameters case 2: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`FLUID.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`eta.comp`,`eta.turb`,`eps.1`,`COOLANT.mdot`,`RPM`,`W.turb`,`W.comp`"
# Combined parameters case 3: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`COOLANT.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`FLUID.T4`,`eta.comp`,`eta.turb`,`eps.1`,`eps.2`,`eps.3`,`COOLANT.mdot`,`RPM`,`W.turb`,`W.comp`"
# Combined parameters case 4: "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`COOLANT.TMax`,`Q.source`,`COOLANT.Tin`,`FLUID.T1`,`FLUID.T3`,`eta.comp`,`eta.turb`,`eps.1`,`eps.2`,`COOLANT.mdot`,`RPM`,`W.turb`,`W.comp`"

class MyProblem(Problem):
    def __init__(self):
        if optim_case == 1:
            super().__init__(n_var=16,
                            n_obj=3,
                            #xl=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Lower bounds of variables
                            #xu=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.56, 1.0, 1.0]))  # Upper bounds of variables
                            xl=np.array([4.1344, 0.0, 0.1182, 0.5652, 0.7105, 0.0, 0.0, 0.0, 0.5, 0.5, 0.99, 0.99, 64.8743, 0.0, 2.4550, 0.4122]),  # Lower bounds of variables
                            xu=np.array([4.7594, 1.0, 0.3, 0.6634, 0.7772, 1.0, 11.28, 1.0, 0.5, 0.5, 1.0, 1.0, 66.3029, 0.56, 2.4883, 0.4314]))  # Upper bounds of variables
            
        elif optim_case == 2:
            super().__init__(n_var=15,
                            n_obj=3,
                            xl=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Lower bounds of variables
                            xu=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.56, 1.0, 1.0]))  # Upper bounds of variables
            
        elif optim_case == 3:
            super().__init__(n_var=18,
                            n_obj=3,
                            xl=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Lower bounds of variables
                            xu=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.56, 1.0, 1.0]))  # Upper bounds of variables
            
        elif optim_case == 4:
            super().__init__(n_var=17,
                            n_obj=3,
                            xl=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Lower bounds of variables
                            xu=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.56, 1.0, 1.0]))  # Upper bounds of variables
        
        elif optim_case == 5:
            super().__init__(n_var=16,
                            n_obj=3,
                            xl=np.array([4.1344, 0.0, 0.1182, 0.5652, 0.7105, 0.0, 0.0, 0.0, 0.5, 0.5, 0.99, 0.99, 64.8743, 0.0, 2.4550, 0.4122]),  # Lower bounds of variables
                            xu=np.array([4.7594, 1.0, 0.3, 0.6634, 0.7772, 1.0, 11.28, 1.0, 0.5, 0.5, 1.0, 1.0, 66.3029, 0.56, 2.4883, 0.4314]))  # Upper bounds of variables

        else:
            # Raise a KeyError with a message indicating the unrecognized optimization case number
            raise KeyError(f"The provided optimization case number '{optim_case}' is not recognized.")

    def _evaluate(self, x, out, *args, **kwargs):
        
        if optim_case == 1:
            common_inputs = x[:, 0:4]
            obj1_input = np.column_stack((common_inputs,x[:, 4:13]))
            obj2_input = np.column_stack((common_inputs,x[:, 9],x[:, 4],x[:, 13],x[:, 14]))
            obj3_input = np.column_stack((common_inputs,x[:, 8],x[:, 7],x[:, 13],x[:, 15]))
            
            obj_1 = obj1_model.predict(obj1_input).flatten()
            obj_2 = obj2_model.predict(obj2_input).flatten()
            obj_3 = obj3_model.predict(obj3_input).flatten()

            out["F"] = np.column_stack([-obj_1, obj_2, obj_3])  # Maximize eta_cyc, minimize mass_turb & mass_comp
            
        elif optim_case == 2:
            common_inputs = x[:, 0:4]
            obj1_input = np.column_stack((common_inputs,x[:, 4:12]))
            obj2_input = np.column_stack((common_inputs,x[:, 9],x[:, 4],x[:, 12],x[:, 13]))
            obj3_input = np.column_stack((common_inputs,x[:, 8],x[:, 7],x[:, 12],x[:, 14]))
            
            obj_1 = obj1_model.predict(obj1_input).flatten()
            obj_2 = obj2_model.predict(obj2_input).flatten()
            obj_3 = obj3_model.predict(obj3_input).flatten()

            out["F"] = np.column_stack([-obj_1, obj_2, obj_3])  # Maximize eta_cyc, minimize mass_turb & mass_comp
        
        elif optim_case == 3:
            common_inputs = x[:, 0:4]
            obj1_input = np.column_stack((common_inputs,x[:, 4:15]))
            obj2_input = np.column_stack((common_inputs,x[:, 10],x[:, 8],x[:, 15],x[:, 16]))
            obj3_input = np.column_stack((common_inputs,x[:, 9],x[:, 7],x[:, 15],x[:, 17]))
            
            obj_1 = obj1_model.predict(obj1_input).flatten()
            obj_2 = obj2_model.predict(obj2_input).flatten()
            obj_3 = obj3_model.predict(obj3_input).flatten()

            out["F"] = np.column_stack([-obj_1, obj_2, obj_3])  # Maximize eta_cyc, minimize mass_turb & mass_comp
            
        elif optim_case == 4:
            common_inputs = x[:, 0:4]
            obj1_input = np.column_stack((common_inputs,x[:, 4:14]))
            obj2_input = np.column_stack((common_inputs,x[:, 10],x[:, 8],x[:, 14],x[:, 15]))
            obj3_input = np.column_stack((common_inputs,x[:, 9],x[:, 7],x[:, 14],x[:, 16]))
            
            obj_1 = obj1_model.predict(obj1_input).flatten()
            obj_2 = obj2_model.predict(obj2_input).flatten()
            obj_3 = obj3_model.predict(obj3_input).flatten()

            out["F"] = np.column_stack([-obj_1, obj_2, obj_3])  # Maximize eta_cyc, minimize mass_turb & mass_comp
        
        else:
            # Raise a KeyError with a message indicating the unrecognized optimization case number
            raise KeyError(f"The provided optimization case number '{optim_case}' is not recognized.")


# Selection
selection = RandomSelection()

# Instantiate problem
problem = MyProblem()

# Configure algorithm and other elements
algorithm = NSGA2(
    pop_size=n,
    #n_offsprings=10,
    #crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    #mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True)

# Optimize
res = minimize(problem,
               algorithm,
               termination=('n_gen', 100))

# Extract and print the results
optimal_solutions = res.X
optimal_objectives = res.F

print("Optimal solutions:", optimal_solutions)
print("Optimal objectives:", optimal_objectives)

print(optimal_objectives[0])
print(optimal_solutions[0])

row = 0
obj = [-optimal_objectives[row][0],optimal_objectives[row][1],optimal_objectives[row][2]]
print(f"obj:\n {obj}")

obj_array = np.array(obj)

# plot = Petal(bounds=[0,1],
#              cmap="tab20",
#              labels=objectives,
#              title=("Objectives", {'pad': 20}))

# plot.add(obj_array)
# plot.show()

with open(obj1_norm_params, "r") as f:
    cyc_params = json.load(f)
with open(obj2_norm_params, "r") as f:
    turb_params = json.load(f)
with open(obj3_norm_params, "r") as f:
    comp_params = json.load(f)

# Initialize an empty dictionary for solution_params
solution_params = {}

# Fill the solution_params dictionary by iterating over the solution_param_index
for param in solution_param_index:
    if param in cyc_params['min_values']:
        solution_params[param] = [cyc_params['min_values'][param], cyc_params['max_values'][param]]
    elif param in turb_params['min_values']:
        solution_params[param] = [turb_params['min_values'][param], turb_params['max_values'][param]]
    elif param in comp_params['min_values']:
        solution_params[param] = [comp_params['min_values'][param], comp_params['max_values'][param]]

# Apply denormalization
denorm_optim_sol = optimal_solutions.copy()
for i, param in enumerate(solution_param_index):
    min_val, max_val = solution_params[param]
    denorm_optim_sol[:, i] = (optimal_solutions[:, i] * (max_val - min_val)) + min_val

denorm_optim_obj = optimal_objectives.copy()
# Assuming the objectives correspond to parameters in cyc_params, adjust as necessary
for i, obj in enumerate(['eta.cyc', 'mass.turb', 'mass.comp']):  # Adjust based on your actual objectives
    if obj in cyc_params['min_values']:  # Adjust this condition if objectives can also be turbine or compressor parameters
        min_val = cyc_params['min_values'][obj]
        max_val = cyc_params['max_values'][obj]
        denorm_optim_obj[:, i] = (optimal_objectives[:, i] * (max_val - min_val)) + min_val

print("Denormalized Optimal solutions:", denorm_optim_sol)
print("Denormalized Optimal objectives:", denorm_optim_obj)

# Combine the denormalized solutions and objectives
combined_data = np.hstack((denorm_optim_obj, denorm_optim_sol))
combined_raw_data = np.hstack((optimal_objectives, optimal_solutions))

# Define the column headers, add objective names
column_headers = objectives + solution_param_index 

# Create a DataFrame with the combined data and column headers
df = pd.DataFrame(combined_data, columns=column_headers)
df_norm = pd.DataFrame(combined_raw_data, columns=column_headers)

# Define the directory path
results_dir = "optimization results"

# Ensure the directory exists
os.makedirs(results_dir, exist_ok=True)

# Define the paths for the CSV files within the new directory
filename_denorm = f"denormalized_optimal_objectives_and_solutions_{tag_full}.csv"
filename_norm = f"normalized_optimal_objectives_and_solutions_{tag_full}.csv"

csv_file_path = os.path.join(results_dir, filename_denorm)
csv_file_path_norm = os.path.join(results_dir, filename_norm)

plot_dir = r"C:\Users\hylandc2\Documents\Research\Images"

# Save the DataFrames to CSV files in the specified directory
def save_optim_solutions_objectives():        
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")

    df_norm.to_csv(csv_file_path_norm, index=False)
    print(f"Norm data saved to {csv_file_path_norm}")

def generate_and_save_scatter_plots():
    # 3D Scatter Plot
    fig = plt.figure(figsize=(8,6),layout='constrained')
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(-denorm_optim_obj[:, 0], denorm_optim_obj[:, 1], denorm_optim_obj[:, 2])
    ax.set_xlabel(f'{objectives[0]}', labelpad=15, fontsize=12)
    ax.set_ylabel(f'{objectives[1]}', labelpad=15, fontsize=12)
    ax.set_zlabel(f'{objectives[2]}', labelpad=15, fontsize=12)
    ax.view_init(elev=25, azim=130)
    #plt.title(f'3D Scatter Plot of Objectives (Denormalized Data), {cycle}')
    
    # Save 3D plot
    plot_filename_3d = f"3D_{cycle}_Objectives.png"
    plot_path_3d = os.path.join(plot_dir, plot_filename_3d)
    plt.savefig(plot_path_3d, bbox_inches='tight')
    #plt.close(fig)  # Close the figure to free memory
    
    # 2D Scatter Plot for eta.cyc vs mass.turb
    fig2, ax2 = plt.subplots(layout='constrained')
    ax2.scatter(-denorm_optim_obj[:, 0], denorm_optim_obj[:, 1])
    ax2.set_xlabel(f'{objectives[0]}', labelpad=15, fontsize=12)
    ax2.set_ylabel(f'{objectives[1]}', labelpad=15, fontsize=12)
    #plt.title(f'{objectives[0]} vs {objectives[1]} (Denormalized Data)')
    
    # Save eta.cyc vs mass.turb plot
    plot_filename_2d_turb = f"2D_{cycle}_eta_cyc_vs_mass_turb.png"
    plot_path_2d_turb = os.path.join(plot_dir, plot_filename_2d_turb)
    plt.savefig(plot_path_2d_turb, bbox_inches='tight')
    #plt.close(fig2)  # Close the figure to free memory

    # 2D Scatter Plot for eta.cyc vs mass.comp
    fig3, ax3 = plt.subplots(layout='constrained')
    ax3.scatter(-denorm_optim_obj[:, 0], denorm_optim_obj[:, 2])
    ax3.set_xlabel(f'{objectives[0]}', labelpad=15, fontsize=12)
    ax3.set_ylabel(f'{objectives[2]}', labelpad=15, fontsize=12)
    #plt.title(f'{objectives[0]} vs {objectives[2]} (Denormalized Data)')
    
    # Save eta.cyc vs mass.comp plot
    plot_filename_2d_comp = f"2D_{cycle}_eta_cyc_vs_mass_comp.png"
    plot_path_2d_comp = os.path.join(plot_dir, plot_filename_2d_comp)
    plt.savefig(plot_path_2d_comp, bbox_inches='tight')
    #plt.close(fig3)  # Close the figure to free memory
    
    print(f"Plots saved in {plot_dir}")

save_model = input("Do you want to save the optimized objectives/solutions and their plots? (yes/no): ")
if save_model.lower() == 'yes':
    save_optim_solutions_objectives()
    generate_and_save_scatter_plots()
else:
    print('end')

# Multi-Criteria Decistion Making
# Psudo Weights

# ref_dirs = get_reference_directions("das-dennis", 16, n_partitions=12)
# #F = problem.pareto_front(ref_dirs)
# F = res.F

# weights = np.array([0.4, 0.2, 0.4])
# a, pseudo_weights_a = PseudoWeights(weights).do(F, return_pseudo_weights=True)

# weights = np.array([0.3, 0.4, 0.3])
# b, pseudo_weights_b = PseudoWeights(weights).do(F, return_pseudo_weights=True)

# plot = Petal(bounds=(0, 1), reverse=True)
# plot.add(F[[a, b]])
# plot.show()

# print(f'F\n{F}')
# print(f'a\n{a}')
# print(f'b\n{b}')
# print(f'pwa\n{pseudo_weights_a}')
# print(f'pwb\n{pseudo_weights_b}')

# print('end')
# High Trade -off Points

# pf = np.loadtxt("knee-2d.out")
# dm = HighTradeoffPoints()

# I = dm(pf)

# plot = Scatter()
# plot.add(pf, alpha=0.2)
# plot.add(pf[I], color="red", s=100)
# plot.show()

