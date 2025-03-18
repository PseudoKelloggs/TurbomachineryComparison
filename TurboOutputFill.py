import os
import csv
import sys
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import ctREFPROP.ctREFPROP as ct

import signal
from tqdm import tqdm
import mysql.connector
import multiprocessing as mp
import TURBOMACH_SIZING_091923 as TMS
import TURBOMACH_DATA_012424 as TMD

mydb = mysql.connector.connect(
  host="localhost",
  user="cj",
  password="1701",
  database="sCO2db"
)

impute_secondcon = "'Y'"
componant = 'Comp'  #input('Input name of componant: ')
table = f"`{componant}`"

# Signal handler function
def sigint_handler(signum, frame):
    print("Received Ctrl+C. Stopping the program gracefully...")
    # Perform any cleanup tasks here
    # You can close database connections or save progress if needed
    mydb.close()
    sys.exit(0)  # Use sys.exit(0) to exit the program gracefully
    
# Set the signal handler for Ctrl+C (SIGINT)
signal.signal(signal.SIGINT, sigint_handler)

def getComponantInputs():
    cursor = mydb.cursor()
    
    condition = "WHERE `is.imputed` = 'N'"
    
    simulation_inputs = TMD.TURBOMACH_DATA[componant]['sim_in']
    
    query = f"SELECT {simulation_inputs} FROM {table} {condition}"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def process_row(row):
    cursor = mydb.cursor()
    
    if componant == 'Turb':
        ID,isimputed,FLUID_type,FLUID_z,mdot,FLUID_Plow,FLUID_Phigh,eta_turb,T_in,RPM = row
        [output_values] = TMS.TURBOMACH_TURB(FLUID_type,[FLUID_z],mdot,FLUID_Plow,FLUID_Phigh,eta_turb,T_in,RPM)
    elif componant == 'Comp':
        ID,isimputed,FLUID_type,FLUID_z,mdot,FLUID_Plow,FLUID_Phigh,eta_comp,T_in,RPM = row
        [output_values] = TMS.TURBOMACH_COMP(FLUID_type,[FLUID_z],mdot,FLUID_Plow,FLUID_Phigh,eta_comp,T_in,RPM)
    else:
        raise KeyError(f"Cycle name {componant} not found in ARC_DATA.")
    
    # Construct the update query
    simulation_ouputs = TMD.TURBOMACH_DATA[componant]['sim_out']
    update_query = f"UPDATE {table} SET {simulation_ouputs}, `is.imputed` = {impute_secondcon} WHERE id = {ID}"
    
    # Execute the update query
    cursor.execute(update_query, list(output_values))
    
    # Commit the changes to the database
    mydb.commit()
    
    # close the cursor    
    cursor.close()

# Function to calculate and display a progress bar
def display_progress_bar(completed, total):
    progress = completed / total
    bar_length = 30
    block = int(round(bar_length * progress))
    text = f"[{'#' * block}{'-' * (bar_length - block)}] {progress * 100:.2f}%"
    return text

# The main function to parallelize the processing
def main():
    pool = mp.Pool(processes=mp.cpu_count())  # Use the available CPU cores

    start_time = time.time()
    
    ComponantInputs = getComponantInputs()

    total_simulations = len(ComponantInputs)
    completed_simulations = 0

    # Create a tqdm progress bar
    with tqdm(total=total_simulations, desc="Processing", ascii=True, dynamic_ncols=True) as pbar:  # Set ascii=True to avoid special characters
        for _ in pool.imap_unordered(process_row, ComponantInputs):
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

if __name__ == "__main__":
    main()