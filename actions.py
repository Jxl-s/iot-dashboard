import os
import sqlite3
import sys
from tkinter import filedialog
import shutil
import random
import string
import requests


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for i in range(length))


DATABASE_NAME = "intellihouse.db"


# USAGE:
# python actions.py --create "my username" "my description"
# python actions.py --login 2
# python actions.py --logout
def main():
    # Get the args, create a user
    action = sys.argv[1]

    # Create a user
    with sqlite3.connect(DATABASE_NAME) as con:
        cur = con.cursor()

        if action == "--create":
            name = sys.argv[2]
            description = sys.argv[3] if len(sys.argv) > 3 else "No Description"

            avatar_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )

            if avatar_path:
                _, extension = os.path.splitext(os.path.basename(avatar_path))
                random_name = generate_random_string(16) + extension

                new_path = os.path.join("./static/images/", random_name)

                shutil.copy(avatar_path, new_path)
                avatar_path = f"/static/images/{random_name}"
            else:
                avatar_path = "/static/images/default-user.png"

            # TODO: wait for a scan to happen
            rfid_tag = f"{random.randint(0, 255)}_{random.randint(0, 255)}_{random.randint(0, 255)}_{random.randint(0, 255)}"
            cur.execute(
                """INSERT OR IGNORE INTO users (
                rfid_tag,
                name,
                description,
                avatar,
                temp_threshold,
                humidity_threshold,
                light_threshold
            )
            VALUES (?, ?, ?, ?, 24, 50, 400)""",
                (rfid_tag, name, description, avatar_path),
            )

            print(f"User created, with ID ({cur.lastrowid}), with tag ({rfid_tag})")

        if action == "--login":
            userid = sys.argv[2]
            requests.post(f"http://localhost:3333/login/{userid}")

        if action == "--logout":
            requests.post("http://localhost:3333/logout")


if __name__ == "__main__":
    main()
