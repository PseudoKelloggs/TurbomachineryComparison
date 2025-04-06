"""
import os
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import ctREFPROP.ctREFPROP as ct
"""
import sys
import time
import signal
from tqdm import tqdm
import mysql.connector
import multiprocessing as mp
import Library.TurboSizing as TMS
import Library.TurboData as TMD

"""
    DESCRIPTION
    Defines ... ... ..
    Only function Definitions, NO MAIN

"""
mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="1701",
  database="sCO2db"
)

impute_secondcon = "'Y'"

"""
    Signal Handler Functions
    Ends program on Ctrl+C
"""
def sigint_handler(signum, frame):
    print("Received Ctrl+C. Stopping the program gracefully...")
    # Perform any cleanup tasks here
    # You can close database connections or save progress if needed
    mydb.close()
    sys.exit(0)  # Use sys.exit(0) to exit the program gracefully

# Set the signal handler for Ctrl+C (SIGINT)
signal.signal(signal.SIGINT, sigint_handler)

"""
Retrieves simulation input rows from the database for the given component 
where `is.imputed` is marked as 'N'. This typically fetches rows that 
have not yet been processed by the output fill logic.
"""
def getComponantInputs(component):
    table = f"`{component}`"

    cursor = mydb.cursor()
    
    condition = "WHERE `is.imputed` = 'N'"
    
    simulation_inputs = TMD.Turbomachine[component][component.getComponantInputs()]
    
    query = f"SELECT {simulation_inputs} FROM {table} {condition}"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

"""
    Defines the variables by the type (Comp or Turb for now)

"""
def process_row(component,type,row):
    cursor = mydb.cursor()
    table = f"`{component}`"

    if type == 'Turb':
        ID,isimputed,FLUID_type,FLUID_z,mdot,FLUID_Plow,FLUID_Phigh,eta_turb,T_in,RPM = row
        [output_values] = TMS.TURBOMACH_TURB(FLUID_type,[FLUID_z],mdot,FLUID_Plow,FLUID_Phigh,eta_turb,T_in,RPM)
    elif type == 'Comp':
        ID,isimputed,FLUID_type,FLUID_z,mdot,FLUID_Plow,FLUID_Phigh,eta_comp,T_in,RPM = row
        [output_values] = TMS.TURBOMACH_COMP(FLUID_type,[FLUID_z],mdot,FLUID_Plow,FLUID_Phigh,eta_comp,T_in,RPM)
    else:
        raise KeyError(f"Cycle name {type} not found in ARC_DATA.")

    # Construct the update query
    simulation_outputs = component.get_sim_output_fields()
    update_query = f"UPDATE {table} SET {simulation_outputs}, `is.imputed` = {impute_secondcon}"
    
    # Execute the update query
    cursor.execute(update_query, list(output_values))
    
    # Commit the changes to the database
    mydb.commit()
    
    # close the cursor    
    cursor.close()

    """
        Function to Calc and Display a Progress bar
    """
def display_progress_bar(completed, total):
    progress = completed / total
    bar_length = 30
    block = int(round(bar_length * progress))
    text = f"[{'#' * block}{'-' * (bar_length - block)}] {progress * 100:.2f}%"
    return text



def run_Output(component,type):
    pool = mp.Pool(processes=mp.cpu_count())  # Use the available CPU cores

    start_time = time.time()
    
    ComponantInputs = getComponantInputs(component)

    total_simulations = len(ComponantInputs)
    completed_simulations = 0

    # Create a tqdm progress bar
    with tqdm(total=total_simulations, desc="Processing", ascii=True, dynamic_ncols=True) as pbar:  # Set ascii=True to avoid special characters
        for _ in pool.imap_unordered(process_row(component,type), ComponantInputs):
            completed_simulations += 1
            pbar.update(1)  # Update the progress bar

    end_time = time.time()
    total_run_time = end_time - start_time
    average_time_per_instance = total_run_time / len(ComponantInputs)

    # Calculate estimated time to completion
    estimated_time_remaining = (total_simulations - completed_simulations) * average_time_per_instance

    # Display the progress bar
    progress_text = display_progress_bar(completed_simulations, total_simulations)

    print(f"Total run time: {total_run_time:.2f} seconds")
    print(f"Average time per instance: {average_time_per_instance:.2f} seconds")
    print(f"Estimated time to completion: {estimated_time_remaining:.2f} seconds")
    print("Progress:", progress_text)

    # Close the database connection
    mydb.close()