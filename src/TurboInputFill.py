import numpy as np
import mysql.connector
import DataFunctions as DF
import TURBOMACH_DATA_012424 as TMD

mydb = mysql.connector.connect(
  host="localhost",
  user="cj",
  password="1701",
  database="sCO2db",
  auth_plugin="mysql_native_password"
)

def CreateTable(componant):
  if componant in TMD.TURBOMACH_DATA:
    tm_specs = TMD.TURBOMACH_DATA[componant]['specs']
    db_features = TMD.TURBOMACH_DATA[componant]['DB_features']
    print("\nTurbomachine Specs: ", tm_specs)
    print("\nDatabase Features: ", db_features)
  else:
    raise KeyError(f"Cycle name {componant} not found in TURBOMACH_DATA")
  
  # Base columns for the SQL table
  base_columns = "id INT AUTO_INCREMENT PRIMARY KEY, `is.imputed` VARCHAR(255), "
    
  # Combining base_columns with db_features
  sql_query = f"CREATE TABLE {{table}} ({base_columns}{db_features})"
  
  cursor = mydb.cursor()
  cursor.execute(sql_query.format(table=componant))

def FillInputs(componant,n):
  if componant in TMD.TURBOMACH_DATA:
    var_bounds = TMD.TURBOMACH_DATA[componant]['Var_bounds']
    print("\nVariable Bounds: ", var_bounds)
  else:
    raise KeyError(f"Cycle name {componant} not found in TURBOMACH_DATA")
  
  input_data = DF.lhs(var_bounds,n)
  
  cursor = mydb.cursor()
  
  #inital part of sql columns
  sql_columns = "`is.imputed`, `FLUID.type`, `FLUID.Phigh`, `FLUID.z`, `FLUID.mdot`, `FLUID.PRatio`, `FLUID.Plow`, "
  sql_columns += "`eta.turb`" if componant == 'Turb' else "`eta.comp`"
  sql_columns += " , `FLUID.Tin`,`RPM`"
  
  # Count the number of features by splitting the string by ','
  num_features = len(sql_columns.split(','))

  # Generate the corresponding number of '%s' placeholders
  placeholders = ", ".join(["%s"] * num_features)
    
  sql = f"INSERT INTO {componant} ({sql_columns}) VALUES ({placeholders})"
  
  # Looping through the data
  for row in input_data:
    # Calculate 'Phigh' and prepare the values to insert
    Phigh = row[2] * row[3]
    row_list = row.tolist()
    values_list = ['N', 'CO2', Phigh] + [1] + row_list[1:]
    
    # Execute the SQL command
    cursor.execute(sql,values_list)
    mydb.commit()
    
    # Print the result
    #print(cursor.rowcount, "data inserted for", componant, "with CO2")

def main():
  componant = 'Turb'
  
  CreateTable(componant)
  print("Table created successfully.")
  
  n = 800
  FillInputs(componant,n)
  print("Inputs successfully filled")
  
  # Close the database connection
  mydb.close()
  
if __name__ == "__main__":
  main()