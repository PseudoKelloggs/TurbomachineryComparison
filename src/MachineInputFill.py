import numpy as np
import sys
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
  specs = component.get_specs()
  db_features = component.get_db_schema()
  
  table_name = specs['code']
  base_columns = "id INT AUTO_INCREMENT PRIMARY KEY, `is.imputed` VARCHAR(255), "
  sql_query = f"CREATE TABLE `{table_name}` ({base_columns}{db_features})"
  
  cursor = mydb.cursor()
  cursor.execute(sql_query.format(table=component))


"""
    Fills Inputs with Variable Boundaries
    Component = Turbomachiner ; n = number of samples created
    POSSIBLE ERROR: TMD.Turbomachinery[component][var_bounds]
"""
def FillInputs(component, n):
    var_bounds = component.get_bounds()
    input_data = DF.lhs(var_bounds, n)

    specs = component.get_specs()
    table_name = specs['code']

    cursor = mydb.cursor()

    sql_columns = "`is.imputed`, `FLUID.type`, `FLUID.Phigh`, `FLUID.z`, `FLUID.mdot`, `FLUID.PRatio`, `FLUID.Plow`, `eta.turb`, `FLUID.Tin`, `RPM`"
    placeholders = ", ".join(["%s"] * len(sql_columns.split(',')))
    sql = f"INSERT INTO `{table_name}` ({sql_columns}) VALUES ({placeholders})"

    for row in input_data:
        Phigh = row[2] * row[3]
        values = ['N', 'CO2', Phigh] + row.tolist()
        print("\n--- SQL DEBUG ---", flush=True)
        print(f"sql_columns:\n{sql_columns}", flush=True)
        print(f"placeholders:\n{placeholders}", flush=True)
        print(f"# of placeholders: {placeholders.count('%s')}", flush=True)
        print(f"values ({len(values)}):\n{values}", flush=True)
        cursor.execute(sql, values)
        mydb.commit()
 
