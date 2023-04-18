import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="change-me",
  port = 3306
)
cur = mydb.cursor()
cur.execute("USE devopsroles")
sql_stmt = f"SELECT * FROM test_table"
cur.execute(sql_stmt)
response = cur.fetchall()
for row in response:
    print(row[0], row[1])
cur.close()
mydb.close()