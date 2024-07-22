import sqlite3

sqliteConnection = sqlite3.connect('users.db')
cursor = sqliteConnection.cursor()

def example():
  # run query
  data=cursor.execute("SELECT * FROM users;").fetchall()
  
  cursor.execute("INSERT INTO users (name, age) VALUES ('John', '23');")
  # save changes
  sqliteConnection.commit()

  # tidy up
  cursor.close()
  sqliteConnection.close()