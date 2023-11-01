import sqlite3
import sys

DATABASE_NAME = "intellihouse.db"

# USAGE:
# python actions.py --create "my username" "my description" "/static/images/my-avatar.jpg"

def main():
    # Get the args, create a user
    action = sys.argv[1]
    name = sys.argv[2]
    description = sys.argv[3]
    avatar = sys.argv[4]

    # Create a user
    with sqlite3.connect(DATABASE_NAME) as con:
        cur = con.cursor()

        if action == "--create":
            cur.execute(
                """INSERT OR IGNORE INTO users (
                name,
                description,
                avatar,
                temp_threshold,
                humidity_threshold,
                light_threshold
            )
            VALUES (?, ?, ?, 24, 50, 400)""",
                (name, description, avatar),
            )

            print("User created, with ID", cur.lastrowid)


if __name__ == "__main__":
    main()
