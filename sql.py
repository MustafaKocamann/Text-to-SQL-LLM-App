import sqlite3

# Connect to db
connection = sqlite3.connect("student.db")

# Create cursor
cursor = connection.cursor()

# Create table
table_info = """
Create Table STUDENT (NAME VARCHAR(22), CLASS VARCHAR(22),
SECTION VARCHAR(22), MARKS INT);
"""

cursor.execute(table_info)

# Insert Values
cursor.execute('''INSERT Into STUDENT values  ('Mustafa', 'Data Science', 'A', 90)''')
cursor.execute('''INSERT Into STUDENT values ('Ville', 'Data Science', 'B', 100)''')
cursor.execute('''INSERT Into STUDENT values ('Mehmet', 'Data Science', 'A', 85)''')
cursor.execute('''INSERT Into STUDENT values ('Heike', 'DEVOPS', 'A', 50)''')
cursor.execute('''INSERT Into STUDENT values ('Alexi', 'DEVOPS', 'A', 50)''')

print("Values Inserted")

data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

# Commit our command
connection.commit()

# Close our connection
connection.close()

