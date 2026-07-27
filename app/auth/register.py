import bcrypt

from app.auth.database import db


class Register:

    def __init__(self):
        pass

    # ---------------------------------------
    # Register User
    # ---------------------------------------

    def create_user(
        self,
        username,
        email,
        password
    ):

        # Check username
        existing_user = db.fetch_one(

            """
            SELECT id
            FROM users
            WHERE username=%s
            """,

            (username,)

        )

        if existing_user:

            return False, "Username already exists."

        # Check email
        existing_email = db.fetch_one(

            """
            SELECT id
            FROM users
            WHERE email=%s
            """,

            (email,)

        )

        if existing_email:

            return False, "Email already registered."

        # Encrypt password
        hashed_password = bcrypt.hashpw(

            password.encode(),

            bcrypt.gensalt()

        ).decode()

        # Insert user
        db.execute(

            """
            INSERT INTO users
            (
                username,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,

            (
                username,
                email,
                hashed_password
            )

        )

        return True, "Registration Successful."