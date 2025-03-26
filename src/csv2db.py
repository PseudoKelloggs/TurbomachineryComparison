import csv
import mysql.connector

# Connect to MySQL Docker database
mydb = mysql.connector.connect(
    host="localhost",
    user="cj",
    password="1701",
    database="sCO2db"
)

# Create cursor
cursor = mydb.cursor()

def create_table(table_name, columns):
    """Create table in the database"""
    # Ensure column definitions are complete and correct before creating the table
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(columns)})"
    cursor.execute(create_table_query)
    mydb.commit()

def insert_data(table_name, columns, data):
    """Insert data into the table"""
    # Note: Removed backticks around `%s` placeholders, they are not needed and incorrect here
    insert_query = f"INSERT INTO `{table_name}` ({', '.join(['`' + column + '`' for column in columns])}) VALUES ({', '.join(['%s' for _ in columns])})"
    cursor.executemany(insert_query, data)
    mydb.commit()

def read_csv(file_path):
    """Read CSV file and return headers and data"""
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        sanitized_headers = [header.replace('.', '_') for header in headers]  # Sanitize column names
        data = [row for row in reader]
    return sanitized_headers, data

def main():
    csv_file = r'C:\Users\hylandc2\Documents\Research\Code\Current\dbBackups\DH_NRC.csv'
    table_name = 'DH_NRC'

    # Read CSV file
    headers, data = read_csv(csv_file)

    # Create table with headers as columns
    create_table(table_name, [f"{header} VARCHAR(255)" for header in headers])

    # Insert data into table
    insert_data(table_name, headers, data)

    print("Data inserted successfully.")

if __name__ == "__main__":
    main()
