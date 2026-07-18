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


def login_page():

    st.title("🔐 Login")

    email = st.text_input("Email", key="login_email")

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", width="stretch"):

        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE email = ?
            AND password = ?
            """,
            (
                email,
                hash_password(password)
            )
        )

        user = cursor.fetchone()

        if user:

            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user[0]
            st.session_state["name"] = user[1]
            st.session_state["email"] = user[2]

            st.success(f"Welcome {user[1]}!")

            st.rerun()

        else:

            st.error("Invalid email or password.")


# Backward compatibility
login = login_page


if __name__ == "__main__":
    login_page()