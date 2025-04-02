import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="cj",
  password="1701",
  database="sCO2db"
)

def exec_query_test(query:str) -> dict:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1701",
        database="sCO2db"
    )
    mycursor = mydb.cursor()
    mycursor.execute(query)
