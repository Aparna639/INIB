import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


DATABASE = "Task2_OnlineBanking/banking.db"


def hash_password(password):
    """Convert a password into a hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    """Open the registration window."""

    register_window = tk.Toplevel(root)
    register_window.title("Create New Account")
    register_window.geometry("700x550")
    register_window.resizable(False, False)
    register_window.configure(bg=BACKGROUND)

    # ---------------- HEADER ----------------

    header_frame = tk.Frame(
        register_window,
        bg=DARK_BLUE,
        height=110
    )

    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="CREATE YOUR ACCOUNT",
        font=("Arial", 24, "bold"),
        bg=DARK_BLUE,
        fg=WHITE
    ).pack(pady=(25, 5))

    tk.Label(
        header_frame,
        text="Join our secure online banking system",
        font=("Arial", 11),
        bg=DARK_BLUE,
        fg="#D6EAF8"
    ).pack()

    # ---------------- REGISTRATION CARD ----------------

    register_card = tk.Frame(
        register_window,
        bg=WHITE,
        width=450,
        height=350
    )

    register_card.pack(pady=25)
    register_card.pack_propagate(False)

    tk.Label(
        register_card,
        text="Account Registration",
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(20, 5))

    tk.Label(
        register_card,
        text="Enter your details below",
        font=("Arial", 10),
        bg=WHITE,
        fg=LIGHT_TEXT
    ).pack(pady=(0, 15))

    # ---------------- USERNAME ----------------

    tk.Label(
        register_card,
        text="Username",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=60)

    username_entry = tk.Entry(
        register_card,
        width=32,
        font=("Arial", 12),
        relief="solid",
        bd=1
    )

    username_entry.pack(pady=(5, 12))

    # ---------------- PASSWORD ----------------

    tk.Label(
        register_card,
        text="Password",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=60)

    password_entry = tk.Entry(
        register_card,
        width=32,
        font=("Arial", 12),
        show="*",
        relief="solid",
        bd=1
    )

    password_entry.pack(pady=(5, 12))

    # ---------------- ACCOUNT NUMBER ----------------

    tk.Label(
        register_card,
        text="Account Number",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=60)

    account_entry = tk.Entry(
        register_card,
        width=32,
        font=("Arial", 12),
        relief="solid",
        bd=1
    )

    account_entry.pack(pady=(5, 15))

    # ---------------- CREATE ACCOUNT ----------------

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
                (
                    username,
                    password_hash,
                    account_number,
                    0.0
                )
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

    create_button = tk.Button(
        register_card,
        text="CREATE ACCOUNT",
        command=create_account,
        width=25,
        height=2,
        font=("Arial", 10, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2"
    )

    create_button.pack(pady=5)


def open_dashboard(username, account_number):
    """Open the banking dashboard."""

    dashboard = tk.Toplevel(root)

    dashboard.title("Banking Dashboard")
    dashboard.geometry("750x600")
    dashboard.resizable(False, False)
    dashboard.configure(bg=BACKGROUND)

    # ---------------- GET CURRENT BALANCE ----------------

    try:

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE username = ?
            AND account_number = ?
            """,
            (username, account_number)
        )

        result = cursor.fetchone()

        connection.close()

        if result:
            balance = result[0]
        else:
            balance = 0.0

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Something went wrong: {error}"
        )

        return

    # =====================================================
    # HEADER
    # =====================================================

    header_frame = tk.Frame(
        dashboard,
        bg=DARK_BLUE,
        height=115
    )

    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="ONLINE BANKING",
        font=("Arial", 24, "bold"),
        bg=DARK_BLUE,
        fg=WHITE
    ).pack(pady=(22, 3))

    tk.Label(
        header_frame,
        text=f"Welcome, {username}!",
        font=("Arial", 11),
        bg=DARK_BLUE,
        fg="#D6EAF8"
    ).pack()

    # =====================================================
    # ACCOUNT NUMBER
    # =====================================================

    tk.Label(
        dashboard,
        text=f"Account Number: {account_number}",
        font=("Arial", 11, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    ).pack(pady=(18, 4))

    # =====================================================
    # BALANCE CARD
    # =====================================================

    balance_card = tk.Frame(
        dashboard,
        bg=WHITE,
        width=500,
        height=145
    )

    balance_card.pack(pady=12)
    balance_card.pack_propagate(False)

    tk.Label(
        balance_card,
        text="CURRENT BALANCE",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=LIGHT_TEXT
    ).pack(pady=(18, 4))

    balance_label = tk.Label(
        balance_card,
        text=f"₹ {balance:.2f}",
        font=("Arial", 30, "bold"),
        bg=WHITE,
        fg=DARK_BLUE
    )

    balance_label.pack()

    # =====================================================
    # DEPOSIT MONEY
    # =====================================================

    def deposit_money():

        deposit_window = tk.Toplevel(dashboard)

        deposit_window.title("Deposit Money")
        deposit_window.geometry("400x300")
        deposit_window.resizable(False, False)
        deposit_window.configure(bg=BACKGROUND)

        tk.Label(
            deposit_window,
            text="DEPOSIT MONEY",
            font=("Arial", 20, "bold"),
            bg=DARK_BLUE,
            fg=WHITE
        ).pack(
            fill="x",
            ipady=15
        )

        tk.Label(
            deposit_window,
            text="Enter amount",
            font=("Arial", 11, "bold"),
            bg=BACKGROUND,
            fg=TEXT
        ).pack(
            pady=(25, 5)
        )

        amount_entry = tk.Entry(
            deposit_window,
            width=25,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        amount_entry.pack(pady=5)

        def process_deposit():

            amount_text = amount_entry.get().strip()

            if not amount_text:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter an amount."
                )

                return

            try:

                amount = float(amount_text)

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid number."
                )

                return

            if amount <= 0:

                messagebox.showerror(
                    "Invalid Amount",
                    "Deposit amount must be greater than zero."
                )

                return

            try:

                connection = sqlite3.connect(DATABASE)
                cursor = connection.cursor()

                # Update balance

                cursor.execute(
                    """
                    UPDATE users
                    SET balance = balance + ?
                    WHERE username = ?
                    AND account_number = ?
                    """,
                    (
                        amount,
                        username,
                        account_number
                    )
                )

                # Record transaction

                cursor.execute(
                    """
                    INSERT INTO transactions
                    (account_number, transaction_type, amount)
                    VALUES (?, ?, ?)
                    """,
                    (
                        account_number,
                        "Deposit",
                        amount
                    )
                )

                connection.commit()

                # Get updated balance

                cursor.execute(
                    """
                    SELECT balance
                    FROM users
                    WHERE username = ?
                    AND account_number = ?
                    """,
                    (
                        username,
                        account_number
                    )
                )

                new_balance = cursor.fetchone()[0]

                connection.close()

                # Update dashboard

                balance_label.config(
                    text=f"₹ {new_balance:.2f}"
                )

                messagebox.showinfo(
                    "Deposit Successful",
                    f"₹ {amount:.2f} deposited successfully!"
                )

                deposit_window.destroy()

            except sqlite3.Error as error:

                messagebox.showerror(
                    "Database Error",
                    f"Something went wrong: {error}"
                )

        tk.Button(
            deposit_window,
            text="DEPOSIT",
            command=process_deposit,
            width=22,
            height=2,
            font=("Arial", 10, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2"
        ).pack(pady=15)

    # =====================================================
    # WITHDRAW MONEY
    # =====================================================

    def withdraw_money():

        withdraw_window = tk.Toplevel(dashboard)

        withdraw_window.title("Withdraw Money")
        withdraw_window.geometry("400x300")
        withdraw_window.resizable(False, False)
        withdraw_window.configure(bg=BACKGROUND)

        tk.Label(
            withdraw_window,
            text="WITHDRAW MONEY",
            font=("Arial", 20, "bold"),
            bg=DARK_BLUE,
            fg=WHITE
        ).pack(
            fill="x",
            ipady=15
        )

        tk.Label(
            withdraw_window,
            text="Enter amount",
            font=("Arial", 11, "bold"),
            bg=BACKGROUND,
            fg=TEXT
        ).pack(
            pady=(25, 5)
        )

        amount_entry = tk.Entry(
            withdraw_window,
            width=25,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        amount_entry.pack(pady=5)

        def process_withdrawal():

            amount_text = amount_entry.get().strip()

            if not amount_text:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter an amount."
                )

                return

            try:

                amount = float(amount_text)

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid number."
                )

                return

            if amount <= 0:

                messagebox.showerror(
                    "Invalid Amount",
                    "Withdrawal amount must be greater than zero."
                )

                return

            try:

                connection = sqlite3.connect(DATABASE)
                cursor = connection.cursor()

                # Get current balance

                cursor.execute(
                    """
                    SELECT balance
                    FROM users
                    WHERE username = ?
                    AND account_number = ?
                    """,
                    (
                        username,
                        account_number
                    )
                )

                result = cursor.fetchone()

                if not result:

                    connection.close()

                    messagebox.showerror(
                        "Error",
                        "Account not found."
                    )

                    return

                current_balance = result[0]

                # Check balance

                if amount > current_balance:

                    connection.close()

                    messagebox.showerror(
                        "Insufficient Funds",
                        "You do not have enough balance."
                    )

                    return

                # Update balance

                cursor.execute(
                    """
                    UPDATE users
                    SET balance = balance - ?
                    WHERE username = ?
                    AND account_number = ?
                    """,
                    (
                        amount,
                        username,
                        account_number
                    )
                )

                # Record transaction

                cursor.execute(
                    """
                    INSERT INTO transactions
                    (account_number, transaction_type, amount)
                    VALUES (?, ?, ?)
                    """,
                    (
                        account_number,
                        "Withdrawal",
                        amount
                    )
                )

                connection.commit()

                # Get new balance

                cursor.execute(
                    """
                    SELECT balance
                    FROM users
                    WHERE username = ?
                    AND account_number = ?
                    """,
                    (
                        username,
                        account_number
                    )
                )

                new_balance = cursor.fetchone()[0]

                connection.close()

                balance_label.config(
                    text=f"₹ {new_balance:.2f}"
                )

                messagebox.showinfo(
                    "Withdrawal Successful",
                    f"₹ {amount:.2f} withdrawn successfully!"
                )

                withdraw_window.destroy()

            except sqlite3.Error as error:

                messagebox.showerror(
                    "Database Error",
                    f"Something went wrong: {error}"
                )

        tk.Button(
            withdraw_window,
            text="WITHDRAW",
            command=process_withdrawal,
            width=22,
            height=2,
            font=("Arial", 10, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2"
        ).pack(pady=15)

    # =====================================================
    # TRANSACTION HISTORY
    # =====================================================

    def show_transaction_history():

        history_window = tk.Toplevel(dashboard)

        history_window.title("Transaction History")
        history_window.geometry("700x450")
        history_window.resizable(False, False)
        history_window.configure(bg=BACKGROUND)

        tk.Label(
            history_window,
            text="TRANSACTION HISTORY",
            font=("Arial", 22, "bold"),
            bg=DARK_BLUE,
            fg=WHITE
        ).pack(
            fill="x",
            ipady=15
        )

        history_text = tk.Text(
            history_window,
            width=75,
            height=17,
            font=("Courier New", 10),
            bg=WHITE,
            fg=TEXT,
            relief="solid",
            bd=1
        )

        history_text.pack(
            padx=25,
            pady=20
        )

        try:

            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT transaction_type, amount, transaction_date
                FROM transactions
                WHERE account_number = ?
                ORDER BY transaction_date DESC
                """,
                (account_number,)
            )

            transactions = cursor.fetchall()

            connection.close()

            if not transactions:

                history_text.insert(
                    tk.END,
                    "No transactions found."
                )

            else:

                history_text.insert(
                    tk.END,
                    f"{'DATE & TIME':<22}"
                    f"{'TYPE':<15}"
                    f"{'AMOUNT':>12}\n"
                )

                history_text.insert(
                    tk.END,
                    "-" * 50 + "\n"
                )

                for transaction in transactions:

                    transaction_type = transaction[0]
                    amount = transaction[1]
                    transaction_date = transaction[2]

                    history_text.insert(
                        tk.END,
                        f"{transaction_date:<22}"
                        f"{transaction_type:<15}"
                        f"₹{amount:>10.2f}\n"
                    )

            history_text.config(
                state=tk.DISABLED
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Something went wrong: {error}"
            )

    # =====================================================
    # BUTTON FRAME
    # =====================================================

    button_frame = tk.Frame(
        dashboard,
        bg=BACKGROUND
    )

    button_frame.pack(pady=8)

    # Deposit button

    tk.Button(
        button_frame,
        text="Deposit Money",
        command=deposit_money,
        width=20,
        height=2,
        font=("Arial", 10, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2"
    ).grid(
        row=0,
        column=0,
        padx=8
    )

    # Withdraw button

    tk.Button(
        button_frame,
        text="Withdraw Money",
        command=withdraw_money,
        width=20,
        height=2,
        font=("Arial", 10, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2"
    ).grid(
        row=0,
        column=1,
        padx=8
    )

    # Transaction history button

    tk.Button(
        dashboard,
        text="Transaction History",
        command=show_transaction_history,
        width=43,
        height=2,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=BLUE,
        activeforeground=DARK_BLUE,
        relief="solid",
        bd=1,
        cursor="hand2"
    ).pack(pady=7)

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout():

        dashboard.destroy()

        username_entry.delete(
            0,
            tk.END
        )

        password_entry.delete(
            0,
            tk.END
        )

    tk.Button(
        dashboard,
        text="Logout",
        command=logout,
        width=20,
        height=2,
        font=("Arial", 10, "bold"),
        bg=DARK_BLUE,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2"
    ).pack(pady=7)
def login_user():
    """Verify login credentials."""

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
            WHERE username = ?
            AND password = ?
            """,
            (username, password_hash)
        )

        user = cursor.fetchone()

        connection.close()

        if user:

            account_number = user[0]

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!"
            )

            open_dashboard(
                username,
                account_number
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



root = tk.Tk()

root.title("Online Banking System")
root.geometry("700x550")
root.resizable(False, False)

# ---------------- COLORS ----------------

BACKGROUND = "#EAF2F8"
DARK_BLUE = "#123B5D"
BLUE = "#1976D2"
WHITE = "#FFFFFF"
TEXT = "#1F2937"
LIGHT_TEXT = "#64748B"


# ---------------- BACKGROUND ----------------

root.configure(bg=BACKGROUND)


# ---------------- HEADER ----------------

header_frame = tk.Frame(
    root,
    bg=DARK_BLUE,
    height=120
)

header_frame.pack(
    fill="x"
)

header_frame.pack_propagate(False)


tk.Label(
    header_frame,
    text="ONLINE BANKING",
    font=("Arial", 28, "bold"),
    bg=DARK_BLUE,
    fg=WHITE
).pack(pady=(25, 5))


tk.Label(
    header_frame,
    text="Secure • Simple • Fast",
    font=("Arial", 11),
    bg=DARK_BLUE,
    fg="#D6EAF8"
).pack()


# ---------------- LOGIN CARD ----------------

login_card = tk.Frame(
    root,
    bg=WHITE,
    width=450,
    height=330
)

login_card.pack(
    pady=35
)

login_card.pack_propagate(False)


tk.Label(
    login_card,
    text="Welcome Back!",
    font=("Arial", 20, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(pady=(25, 5))


tk.Label(
    login_card,
    text="Login to access your account",
    font=("Arial", 10),
    bg=WHITE,
    fg=LIGHT_TEXT
).pack(pady=(0, 20))


# ---------------- USERNAME ----------------

tk.Label(
    login_card,
    text="Username",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", padx=70)


username_entry = tk.Entry(
    login_card,
    width=32,
    font=("Arial", 12),
    relief="solid",
    bd=1
)

username_entry.pack(pady=(5, 15))


# ---------------- PASSWORD ----------------

tk.Label(
    login_card,
    text="Password",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", padx=70)


password_entry = tk.Entry(
    login_card,
    width=32,
    font=("Arial", 12),
    show="*",
    relief="solid",
    bd=1
)

password_entry.pack(pady=(5, 20))


# ---------------- LOGIN BUTTON ----------------

login_button = tk.Button(
    login_card,
    text="LOGIN",
    command=login_user,
    width=25,
    height=2,
    font=("Arial", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2"
)

login_button.pack(pady=5)


# ---------------- REGISTER BUTTON ----------------

register_button = tk.Button(
    login_card,
    text="Create New Account",
    command=register_user,
    font=("Arial", 10),
    bg=WHITE,
    fg=BLUE,
    activeforeground=DARK_BLUE,
    relief="flat",
    cursor="hand2"
)

register_button.pack(pady=8)


# ---------------- START APPLICATION ----------------

root.mainloop()