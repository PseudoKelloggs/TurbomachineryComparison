import mysql.connector
import matplotlib.pyplot as plt

# ------------------------------------------------------
# Connects to the MySQL database and retrieves data
# for specific turbomachinery from the given table.
# Returns transposed lists: Ns, Ds, Efficiency, Work.
# ------------------------------------------------------
def fetch_turbo_data(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="1701",
        database="sCO2db"
    )
    cursor = mydb.cursor()
    query = f"""
    SELECT `Ns`, `Ds`, `eta.turb`, `W.turb`
    FROM `{table_name}`
    WHERE `is.imputed` = 'Y'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    return list(zip(*results))  # Transpose rows -> columns

# ------------------------------------------------------
# Main plotting function. It fetches data for axial and 
# radial turbines and generates two comparison plots:
# 1. Ns vs Ds (Specific Speed vs Diameter)
# 2. Efficiency vs Turbine Work
# Each plot is saved as a PNG and also displayed.
# ------------------------------------------------------
def plot_comparison():
    axial_Ns, axial_Ds, axial_eta, axial_work = fetch_turbo_data('AxTurb')
    radial_Ns, radial_Ds, radial_eta, radial_work = fetch_turbo_data('RadTurb')

    # ----------- Plot 1: Ns vs Ds -------------------
    plt.figure()
    plt.scatter(axial_Ns, axial_Ds, label='Axial Turbine', marker='o')
    plt.scatter(radial_Ns, radial_Ds, label='Radial Turbine', marker='x')
    plt.xlabel('Specific Speed (Ns)')
    plt.ylabel('Specific Diameter (Ds)')
    plt.title('Specific Speed vs Specific Diameter')
    plt.legend()
    plt.grid(True)
    plt.savefig("Ns_vs_Ds.png")

    # ----------- Plot 2: Efficiency vs Work --------
    plt.figure()
    plt.scatter(axial_eta, axial_work, label='Axial Turbine', marker='o')
    plt.scatter(radial_eta, radial_work, label='Radial Turbine', marker='x')
    plt.xlabel('Turbine Efficiency (η)')
    plt.ylabel('Turbine Work Output [W]')
    plt.title('Efficiency vs Turbine Work')
    plt.legend()
    plt.grid(True)
    plt.savefig("Efficiency_vs_Work.png")

    # ----------- Show interactive windows ----------
    plt.show()

# ------------------------------------------------------
# Main execution trigger: only runs if script is launched
# directly. Prevents accidental execution if imported.
# ------------------------------------------------------
if __name__ == "__main__":
    plot_comparison()
