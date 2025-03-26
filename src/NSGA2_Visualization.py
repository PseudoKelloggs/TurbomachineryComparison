import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pymoo.visualization.petal import Petal

optim_case = 4
# Case 1: DH_RC (eta.cyc), turb (mass), comp (mass)
# Case 2: DH_NRC (eta.cyc), turb (mass), comp (mass)
# Case 3: IH_RC (eta.cyc), turb (mass), comp (mass)
# Case 4: IH_NRC (eta.cyc), turb (mass), comp (mass)

if optim_case == 1:
    csv_file_path_norm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\normalized_optimal_objectives_and_solutions_DH_RC_etacyc_turbmass_compmass.csv"
    csv_file_path_denorm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\denormalized_optimal_objectives_and_solutions_DH_RC_etacyc_turbmass_compmass.csv"
    tag = 'case1'
    tag_full = 'DH_RC_etacyc_turbmass_compmass'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    cycle = 'DH_RC'
    obj1_norm_params = "normalization_parameters/normalization_params_`DH_RC`_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "FLUID.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "eta.comp", "eta.turb", "eps.1", "eps.2", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]
elif optim_case == 2:
    csv_file_path_norm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\normalized_optimal_objectives_and_solutions_DH_NRC_etacyc_turbmass_compmass.csv"
    csv_file_path_denorm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\denormalized_optimal_objectives_and_solutions_DH_NRC_etacyc_turbmass_compmass.csv"
    tag = 'case2'
    tag_full = 'DH_NRC_etacyc_turbmass_compmass'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    cycle = 'DH_NRC'
    obj1_norm_params = "normalization_parameters/normalization_params_`DH_NRC`_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "FLUID.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "eta.comp", "eta.turb", "eps.1", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]
elif optim_case == 3:
    csv_file_path_norm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\normalized_optimal_objectives_and_solutions_IH_RC_etacyc_turbmass_compmass.csv"
    csv_file_path_denorm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\denormalized_optimal_objectives_and_solutions_IH_RC_etacyc_turbmass_compmass.csv"
    tag = 'case3'
    tag_full = 'IH_RC_etacyc_turbmass_compmass'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    cycle = 'IH_RC'
    obj1_norm_params = "normalization_parameters/normalization_params_`IH_RC`_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "COOLANT.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "FLUID.T4", "eta.comp", "eta.turb", "eps.1", "eps.2", "eps.3", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]
elif optim_case == 4:
    csv_file_path_norm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\normalized_optimal_objectives_and_solutions_IH_NRC_etacyc_turbmass_compmass.csv"
    csv_file_path_denorm = r"C:\Users\hylandc2\Documents\Research\Code\Current\optimization results\denormalized_optimal_objectives_and_solutions_IH_NRC_etacyc_turbmass_compmass.csv"
    tag = 'case4'
    tag_full = 'IH_NRC_etacyc_turbmass_compmass'
    cycle = 'IH_NRC'
    objectives = ['eta.cyc','mass.turb','mass.comp']
    obj1_norm_params = "normalization_parameters/normalization_params_`IH_NRC`_eta.json"
    obj2_norm_params = "normalization_parameters/normalization_params_turb_mass.json"
    obj3_norm_params = "normalization_parameters/normalization_params_comp_mass.json"
    solution_param_index = ["FLUID.mdot", "FLUID.PRatio", "FLUID.Plow", "FLUID.Phigh", "COOLANT.TMax", "Q.source", "COOLANT.Tin", "FLUID.T1", "FLUID.T3", "eta.comp", "eta.turb", "eps.1", "eps.2", "COOLANT.mdot", "RPM", "W.turb", "W.comp"]


# Function to load data and extract labels
def load_data_and_labels(csv_file_path):
    df = pd.read_csv(csv_file_path)
    objectives_labels = df.columns[:3]  # Assuming first 3 columns are objectives
    solutions_labels = df.columns[3:]  # Remaining columns are solutions
    return df, objectives_labels, solutions_labels

df_norm, objectives_labels, solutions_labels = load_data_and_labels(csv_file_path_norm)
df_denorm, objectives_labels, solutions_labels = load_data_and_labels(csv_file_path_denorm)

# Extract objective columns for plotting
eta_cyc_denorm = -df_denorm['eta.cyc']
mass_turb_denorm = df_denorm['mass.turb']
mass_comp_denorm = df_denorm['mass.comp']

# Extract normalized objectives for the Petal plot
eta_cyc_norm = -df_norm['eta.cyc']
mass_turb_norm = df_norm['mass.turb']
mass_comp_norm = df_norm['mass.comp']

# Define the index of the solution you're interested in
selected_index = 1  # Update this based on your criteria

# Extract the specific optimal normalized objectives and solutions
optimal_objectives = df_norm.iloc[selected_index, :3].values
optimal_objectives = np.array([-optimal_objectives[0], optimal_objectives[1]*10, optimal_objectives[2]*10])
optimal_solutions = df_norm.iloc[selected_index, 3:].values

# 3D Scatter Plot for Denormalized Data
fig = plt.figure(figsize=(8,6),layout='constrained')
ax = fig.add_subplot(111, projection='3d')
ax.scatter(eta_cyc_denorm, mass_turb_denorm, mass_comp_denorm)
ax.set_xlabel('eta.cyc', labelpad=15, fontsize=12)
ax.set_ylabel('mass.turb [kg]', labelpad=15, fontsize=12)
ax.set_zlabel('mass.comp [kg]', labelpad=15, fontsize=12)
ax.view_init(elev=25, azim=130)
#plt.title('3D Objective Pareto Front', pad=0, fontsize=16)
# Adjust layout to make sure labels and title are visible

# 2D Scatter Plots for each pair of objectives
fig2, ax2 = plt.subplots(layout='constrained')
ax2.scatter(eta_cyc_denorm, mass_turb_denorm)
ax2.set_xlabel('eta.cyc', labelpad=15, fontsize=12)
ax2.set_ylabel('mass.turb [kg]', labelpad=15, fontsize=12)
#plt.title('eta.cyc vs mass.turb (Denormalized Data)', pad=20, fontsize=16)

fig3, ax3 = plt.subplots(layout='constrained')
ax3.scatter(eta_cyc_denorm, mass_comp_denorm)
ax3.set_xlabel('eta.cyc', labelpad=15, fontsize=12)
ax3.set_ylabel('mass.comp [kg]', labelpad=15, fontsize=12)
#plt.title('eta.cyc vs mass.comp (Denormalized Data)', pad=20, fontsize=16)

fig4, ax4 = plt.subplots(layout='constrained')
ax4.scatter(mass_comp_denorm, mass_turb_denorm)
ax4.set_xlabel('mass.comp [kg]', labelpad=15, fontsize=12)
ax4.set_ylabel('mass.turb [kg]', labelpad=15, fontsize=12)
#plt.title('eta.cyc vs mass.comp (Denormalized Data)', pad=20, fontsize=16)
plt.show()

# Extract objective columns for plotting
eta_cyc_denorm = -df_denorm['eta.cyc']
mass_turb_denorm = df_denorm['mass.turb']
mass_comp_denorm = df_denorm['mass.comp']

# Plot surface using existing data points
# You can use Delaunay triangulation to create a surface from the data points
from scipy.spatial import Delaunay

# Combine x, y, and z into a single array
data_points = np.array([eta_cyc_denorm, mass_turb_denorm, mass_comp_denorm]).T

# Perform Delaunay triangulation
tri = Delaunay(data_points)

# Plot the triangulation surface
fig_s1 = plt.figure()
ax_s1 = fig_s1.add_subplot(111, projection='3d')
ax_s1.plot_trisurf(eta_cyc_denorm, mass_turb_denorm, mass_comp_denorm, triangles=tri.simplices, antialiased = True, color='Blue', edgecolor='none', alpha=0.75)
ax_s1.set_xlabel('eta.cyc', fontsize=12)
ax_s1.set_ylabel('mass.turb [kg]', fontsize=12)
ax_s1.set_zlabel('mass.comp [kg]', fontsize=12)
ax_s1.set_xticklabels([])
ax_s1.set_yticklabels([])
ax_s1.set_zticklabels([])
ax_s1.view_init(elev=25, azim=130)

fig_s2 = plt.figure()
ax_s2 = fig_s2.add_subplot(111, projection='3d')
ax_s2.plot_trisurf(eta_cyc_denorm, mass_turb_denorm, mass_comp_denorm, triangles=tri.simplices, antialiased = True, color='Blue', edgecolor='none', alpha=0.75)
ax_s2.set_xlabel('eta.cyc', fontsize=12)
ax_s2.set_ylabel('mass.turb [kg]', fontsize=12)
ax_s2.set_zlabel('mass.comp [kg]', fontsize=12)
ax_s2.set_xticklabels([])
ax_s2.set_yticklabels([])
ax_s2.set_zticklabels([])
ax_s2.view_init(elev=8, azim=-130)

fig_s3 = plt.figure()
ax_s3 = fig_s3.add_subplot(111, projection='3d')
ax_s3.plot_trisurf(eta_cyc_denorm, mass_turb_denorm, mass_comp_denorm, triangles=tri.simplices, antialiased = True, color='Blue', edgecolor='none', alpha=0.75)
ax_s3.set_xlabel('eta.cyc', fontsize=12)
ax_s3.set_ylabel('mass.turb [kg]', fontsize=12)
ax_s3.set_zlabel('mass.comp [kg]', fontsize=12)
ax_s3.set_xticklabels([])
ax_s3.set_yticklabels([])
ax_s3.set_zticklabels([])
ax_s3.view_init(elev=8, azim=-32)

plt.show()

# Petal Plot for Normalized Data (objectives)
plot_obj = Petal(bounds=[0,1],
             cmap="tab20",
             labels=["eta.cyc","mass.comp","mass.turb"],
             title=("Objectives", {'pad': 20}))


plot_obj.add(optimal_objectives)
plot_obj.show()

# Petal Plot for Normalized Data (solutions)
plot_sol = Petal(bounds=[0,1],
             cmap="tab20",
             labels=solution_param_index,
             title=("Solutions", {'pad': 20}))

plot_sol.add(optimal_solutions)
plot_sol.show()

# Petal plot for 6 objectives/solutions
rows = [0,1,2,3]

# Invert the first value (eta.cyc) in each set of objectives for plot_obj_4
optim_obj_r1 = np.array([[-df_norm.iloc[rows[0], 0], df_norm.iloc[rows[0], 1]*10, df_norm.iloc[rows[0], 2]*10],
                         [-df_norm.iloc[rows[1], 0], df_norm.iloc[rows[1], 1]*10, df_norm.iloc[rows[1], 2]*10],])
optim_obj_r2 = np.array([[-df_norm.iloc[rows[2], 0], df_norm.iloc[rows[2], 1]*10, df_norm.iloc[rows[2], 2]*10],
                         [-df_norm.iloc[rows[3], 0], df_norm.iloc[rows[3], 1]*10, df_norm.iloc[rows[3], 2]*10],])

# Plot 4 selected objectives
plot_obj_4 = Petal(bounds=[0,1],
             cmap="tab20",
             labels=["eta.cyc","mass.comp","mass.turb"],
             #labels=["obj.1","obj.2","obj.3"],
             title=["Objective %s" % t for t in ["A", "B", "C", "D"]])

plot_obj_4.add(optim_obj_r1)
plot_obj_4.add(optim_obj_r2)

# Display the plot with adjusted padding
plt.figure(figsize=(8, 6))  # You can adjust the figure size as needed
plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)  # Adjust the padding here
plot_obj_4.show()

optim_sol_r1 = np.array([df_norm.iloc[rows[0], 3:].values, df_norm.iloc[rows[1], 3:].values])
optim_sol_r2 = np.array([df_norm.iloc[rows[2], 3:].values, df_norm.iloc[rows[3], 3:].values])
# Invert the first value (eta.cyc) in each set of objectives for plot_sol_4
plot_sol_4 = Petal(bounds=[0,1],
             cmap="tab20",
             labels=solution_param_index,
             #labels=['sol.1','sol.2','sol.3','sol.4','sol.5','sol.6','sol.7','sol.8','sol.9','sol.10','sol.11','sol.12','sol.13','sol.14','sol.14','sol.15'],
             title=["Solutions %s" % t for t in ["A", "B", "C", "D"]])
             #title=[["Solution A", "Solution B", "Solution C", "Solution D"], {'pad': 20}])
plot_sol_4.add(optim_sol_r1)
plot_sol_4.add(optim_sol_r2)

# Display the solutions plot with adjusted padding
plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)  # Adjust the padding here
plot_sol_4.show()