import subprocess
import time
import socket
import os
import Library.TurboData as TMD
from src import MachineInputFill as MIF
#from src import MachineOutputFill as MOF

#DOCKER NEEDS TO BE OPENED AND RUNNING 
#Docker bat setup 
def run_batch_file(batch_file_relative_path):
    full_path = os.path.abspath(batch_file_relative_path)
    quoted_path = f'"{full_path}"'  # wrap in quotes to handle spaces

    print(f"Trying to run: {quoted_path}")
    print(f"Working dir: {os.getcwd()}")

    try:
        result = subprocess.run(quoted_path, shell=True, check=True, capture_output=True, text=True)
        print("Database setup complete.")
        print("Output:\n", result.stdout)
        print("Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run batch file: {e}")
        print("Output:\n", e.stdout)
        print("Errors:\n", e.stderr)
        exit(1)

#For Data Visualization (DataGrip), Connect the docker server here now
def wait_for_user(message):
    input(f"{message}\nPress Enter when ready...")


def run_python_script(script_name):
    try:
        print(f"Executing {script_name}...")
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")
        exit(1)

if __name__ == "__main__":
   
    # Step 1: Start the MySQL database using the batch file
    #run_batch_file("dbsetup/startupDB.bat")

    # Step 2: Wait for user to connect DataGrip to Docker DB
    wait_for_user("Connect to the MySQL Docker container using DataGrip.")

    #Define Component (Axial Turbine)
    axialTurbine = TMD.Turbomachine(
        name = 'Axial Turbine',
        code = 'AxTurb',
        var_bounds=[
        (0.85, 1),      # FLUID.z (Fluid Mix Ratio)
        (5, 150),        # FLUID.mdot (Mass Flow Rate [kg/s])
        (1.5, 10.0),     # FLUID.PRatio (Pressure Ratio)
        (.1, 15.0),     # FLUID.Plow (Low Pressure [MPa])
        (0.85, 0.93),     # eta.turb (Turbine Efficiency)
        (500, 1600),     # FLUID.Tin (Inlet Temperature [K])
        (3000, 30000) # RPM (Rotational Speed [RPM])
        ]
    )
    TMD.TURBOMACHINE_REGISTRY[axialTurbine.get_specs()['code'].lower()] = axialTurbine

    #Sample Size
    n = 50

    #Step 3: Run TurboInputFill
    MIF.CreateTable(axialTurbine)
    print("Table Created Successfully")

    MIF.FillInputs(axialTurbine, n)
    print("Tables Filled Correctly")
 
    #MIF.mydb.close()
    #print("Inputs Completed - Inputs Filled - Runnint Outputs")

    #Define Component (Radial Turbine)
    radialTurbine = TMD.Turbomachine(
        name = 'Radial Turbine',
        code = 'RadTurb',
        var_bounds=[
        (1, 1),      # FLUID.z (Fluid Mix Ratio)
        (1, 20),        # FLUID.mdot (Mass Flow Rate [kg/s])
        (2, 20),     # FLUID.PRatio (Pressure Ratio)
        (.05, 5),     # FLUID.Plow (Low Pressure [MPa])
        (0.75, 0.9),     # eta.turb (Turbine Efficiency)
        (350, 1300),     # FLUID.Tin (Inlet Temperature [K])
        (20000, 120000) # RPM (Rotational Speed [RPM])
        ]
    )

    MIF.CreateTable(radialTurbine)
    print("Table Created Successfully")

    MIF.FillInputs(radialTurbine, n)
    print("Tables Filled Correctly")
 
    MIF.mydb.close()
    print("Inputs Completed - Inputs Filled - Runnint Outputs")

    # Step 4: Run TurboOutputFill to further populate DB
    #MOF.run_Output(axialTurbine,'Turb')