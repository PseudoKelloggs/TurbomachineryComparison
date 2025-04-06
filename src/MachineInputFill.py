import numpy as np
import mysql.connector
import Library.DataFunctions as DF
import Library.TurboData as TMD

"""
    Setup The Database
    Defines Fill Inputs, CreateTable
    Only function Definitions, NO MAIN
"""
mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="1701",
  database="sCO2db",
  auth_plugin="mysql_native_password"
)

"""
    Creates Tables (SQL) from Turbomachinery Object
    Pass in specific Turbomachinery for comparison
    Raise keyError: Debugging - refrences global TURBOMACHINE_REGISTRY Array for code
"""
def CreateTable(component):
  if component in TMD.TURBOMACH_DATA:
    tm_specs = TMD.TURBOMACH_DATA[component]['specs']
    db_features = TMD.TURBOMACH_DATA[component]['DB_features']
    print("\nTurbomachine Specs: ", tm_specs)
    print("\nDatabase Features: ", db_features)
  else:
    raise KeyError(f"Turbomachinery code name {component} not found in Global Registry")
  
  # Base columns for the SQL table
  base_columns = "id INT AUTO_INCREMENT PRIMARY KEY, `is.imputed` VARCHAR(255), "
    
  # Combining base_columns with db_features
  sql_query = f"CREATE TABLE {{table}} ({base_columns}{db_features})"
  
  cursor = mydb.cursor()
  cursor.execute(sql_query.format(table=component))

"""
    Fills Inputs with Variable Boundaries
    Component = Turbomachiner ; n = number of samples created
    POSSIBLE ERROR: TMD.Turbomachinery[component][var_bounds]
"""
def FillInputs(component,n):
  if component in TMD.Turbomachine:
    var_bounds = TMD.Turbomachine[component][var_bounds]
    print("\nVariable Bounds: ", var_bounds)
  else:
    raise KeyError(f"Turbomachinery code name {component} not found in Global Registry")
  
  input_data = DF.lhs(var_bounds,n)
  
  cursor = mydb.cursor()
  
  #inital part of sql columns
  sql_columns = "`is.imputed`, `FLUID.type`, `FLUID.Phigh`, `FLUID.z`, `FLUID.mdot`, `FLUID.PRatio`, `FLUID.Plow`, "
  sql_columns += TMD.Turbomachine[component][var_bounds]
  sql_columns += " , `FLUID.Tin`,`RPM`"
  
  # Count the number of features by splitting the string by ','
  num_features = len(sql_columns.split(','))

  # Generate the corresponding number of '%s' placeholders
  placeholders = ", ".join(["%s"] * num_features)
    
  sql = f"INSERT INTO {component} ({sql_columns}) VALUES ({placeholders})"
  
  # Looping through the data
  for row in input_data:
    # Calculate 'Phigh' and prepare the values to insert
    Phigh = row[2] * row[3]
    row_list = row.tolist()
    values_list = ['N', 'CO2', Phigh] + [1] + row_list[1:]
    
    # Execute the SQL command
    cursor.execute(sql,values_list)
    mydb.commit()
 
