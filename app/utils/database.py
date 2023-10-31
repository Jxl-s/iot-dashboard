import sqlite3

con = sqlite3.connect("intellihouse.db")

# Create the table, if it does not exist
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        avatar TEXT,

        temp_threshold INTEGER,
        humidity_threshold INTEGER,
        light_threshold INTEGER
    )"""
)

# Create the default user if it does not exist
cur.execute(
    """INSERT OR IGNORE INTO users (id, name, description, avatar, temp_threshold, humidity_threshold, light_threshold)
        VALUES (1, 'Default User', 'Default user for testing purposes', '/static/images/default-user.jpg', 24, 50, 400)"""
)


def get_user_by_id(user_id):
    # Execute a query
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cur.fetchone()

    # If the user does not exist, return None
    if result is None:
        return None

    # Return with the correct structure
    return {
        "name": result[1],
        "description": result[2],
        "avatar": result[3],
        "favourites": {
            "temperature": result[4],
            "humidity": result[5],
            "light_intensity": result[6],
        },
    }
