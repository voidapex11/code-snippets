import sqlite3

sqliteConnection = sqlite3.connect('users.db')
cursor = sqliteConnection.cursor()

def example():
  # run query
  query=cursor.execute("SELECT * FROM users;")
  data=query.fetchall()
  
  cursor.execute("INSERT INTO users (name, age) VALUES ('John', '23');")
  # save changes
  sqliteConnection.commit()

  # tidy up
  cursor.close()
  sqliteConnection.close()