import bcrypt

from app.auth.database import db


class Login:

    def __init__(self):
        pass

    # ---------------------------------------
    # Login User
    # ---------------------------------------

    def authenticate(
        self,
        username_or_email,
        password
    ):

        # Search by username or email
        user = db.fetch_one(

            """
            SELECT
                id,
                username,
                email,
                password

            FROM users

            WHERE username=?
               OR email=?
            """,

            (

                username_or_email,
                username_or_email

            )

        )

        # User not found
        if user is None:

            return False, "User not found."

        user_id = user[0]
        username = user[1]
        email = user[2]
        hashed_password = user[3]

        # Verify password
        password_matches = bcrypt.checkpw(

            password.encode(),

            hashed_password.encode()

        )

        if not password_matches:

            return False, "Incorrect password."

        # Update last login
        db.execute(

            """
            UPDATE users

            SET last_login=CURRENT_TIMESTAMP

            WHERE id=?
            """,

            (user_id,)

        )

        return True, {

            "id": user_id,

            "username": username,

            "email": email

        }