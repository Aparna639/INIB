import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


DATABASE = "Task2_OnlineBanking/banking.db"


def hash_password(password):
    """Convert a password into a secure hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    """Open the registration window."""

    register_window = tk.Toplevel(root)
    register_window.title("Create Account")
    register_window.geometry("400x400")
    register_window.resizable(False, False)

    tk.Label(
        register_window,
        text="Create New Account",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(register_window, text="Username").pack()
    username_entry = tk.Entry(register_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack()
    password_entry = tk.Entry(register_window, width=30, show="*")
    password_entry.pack(pady=5)

    tk.Label(register_window, text="Account Number").pack()
    account_entry = tk.Entry(register_window, width=30)
    account_entry.pack(pady=5)

    def create_account():
        username = username_entry.get().strip()
        password = password_entry.get()
        account_number = account_entry.get().strip()

        if not username or not password or not account_number:
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        password_hash = hash_password(password)

        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (username, password, account_number, balance)
                VALUES (?, ?, ?, ?)
                """,
                (username, password_hash, account_number, 0.0)
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Account created successfully!"
            )

            register_window.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Username or account number already exists."
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Something went wrong:\n{error}"
            )

    tk.Button(
        register_window,
        text="Create Account",
        command=create_account,
        width=20
    ).pack(pady=20)


def login_user():
    """Verify the user's login credentials."""

    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror(
            "Error",
            "Please enter username and password."
        )
        return

    password_hash = hash_password(password)

    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT account_number
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password_hash)
        )

        user = cursor.fetchone()

        connection.close()

        if user:
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!"
            )
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Something went wrong:\n{error}"
        )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Online Banking System")
root.geometry("800x500")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="ONLINE BANKING SYSTEM",
    font=("Arial", 26, "bold")
)
title_label.pack(pady=40)

tk.Label(
    root,
    text="Username",
    font=("Arial", 12)
).pack()

username_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)
username_entry.pack(pady=8)

tk.Label(
    root,
    text="Password",
    font=("Arial", 12)
).pack()

password_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12),
    show="*"
)
password_entry.pack(pady=8)

tk.Button(
    root,
    text="Login",
    command=login_user,
    width=20
).pack(pady=15)

tk.Button(
    root,
    text="Create New Account",
    command=register_user,
    width=20
).pack()

root.mainloop()