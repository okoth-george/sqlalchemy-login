import sqlite3

# Create a new SQLite database (or connect to one if it exists)
conn = sqlite3.connect("my_database.db")  # This will create a file named my_database.db

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
# Insert some users
users = [
    ("jijo", "george@example.com"),
    ("alic", "alice@example.com"),
    ("boob", "bob@example.com")
]

cursor.executemany("INSERT INTO users (username, email) VALUES (?, ?)", users)




# Save changes and close connection
conn.commit()
conn.close()
print("Users inserted successfully.")
print("Database and table created successfully.")
