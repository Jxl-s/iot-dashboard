import sqlite3

DATABASE_NAME = "intellihouse.db"

# Create initial database, if not present
with sqlite3.connect(DATABASE_NAME) as con:
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
        """INSERT OR IGNORE INTO users (
            id,
            name,
            description,
            avatar,
            temp_threshold,
            humidity_threshold,
            light_threshold
        )
        VALUES (1, 'Default User', 'Default user for testing purposes', '/static/images/default-user.jpg', 24, 50, 400)"""
    )


# Gets the user profile, given the user id
def get_user_by_id(user_id):
    with sqlite3.connect(DATABASE_NAME) as con:
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


# Updates a user's favourite tresholds
def update_user_favourites(user_id, favourites):
    with sqlite3.connect(DATABASE_NAME) as con:
        # Execute a query
        cur = con.cursor()
        cur.execute(
            """UPDATE users SET temp_threshold = ?, humidity_threshold = ?, light_threshold = ? WHERE id = ?""",
            (
                favourites["temperature"],
                favourites["humidity"],
                favourites["light_intensity"],
                user_id,
            ),
        )
