import streamlit as st
import sqlite3
import hashlib

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup_page():

    st.title("📝 Create Account")

    name = st.text_input(
        "Full Name",
        key="signup_name"
    )

    email = st.text_input(
        "Email",
        key="signup_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password",
        key="signup_confirm"
    )

    if st.button(
        "Create Account",
        width="stretch"
    ):

        if not name or not email or not password or not confirm:
            st.error("Please fill all fields.")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        try:

            cursor.execute(
                """
                INSERT INTO users(name,email,password)
                VALUES(?,?,?)
                """,
                (
                    name,
                    email,
                    hash_password(password)
                )
            )

            conn.commit()

            st.success("Account created successfully!")

            st.info("You can now login from the Login tab.")

        except sqlite3.IntegrityError:

            st.error("Email already exists.")


# Backward compatibility
signup = signup_page


if __name__ == "__main__":
    signup_page()