import customtkinter as ctk
from dashboard import Dashboard


class Login:
    def __init__(self):
        self.window = ctk.CTk()

        # Window
        self.window.title("PC Hub - Login")
        self.window.geometry("500x400")

        # Main container
        self.login_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )

        self.login_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Title
        self.title_label = ctk.CTkLabel(
            self.login_frame,
            text="PC HUB",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )
        self.title_label.pack(pady=(0, 30))

        # Username
        self.username_label = ctk.CTkLabel(
            self.login_frame,
            text="Username"
        )
        self.username_label.pack(
            anchor="w",
            pady=(0, 5)
        )

        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            width=280,
            height=38
        )
        self.username_entry.pack()

        # Password
        self.password_label = ctk.CTkLabel(
            self.login_frame,
            text="Password"
        )
        self.password_label.pack(
            anchor="w",
            pady=(18, 5)
        )

        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            width=280,
            height=38,
            show="*"
        )
        self.password_entry.pack()

        # Login button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=280,
            height=38,
            command=self.login
        )
        self.login_button.pack(pady=(25, 8))

        # Exit button
        self.exit_button = ctk.CTkButton(
            self.login_frame,
            text="Exit",
            width=280,
            height=38,
            command=self.window.destroy
        )
        self.exit_button.pack()

        # Press Enter to login
        self.window.bind(
            "<Return>",
            lambda event: self.login()
        )

        # Focus username
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username != "Admin" or password != "Admin123":
            print("Invalid username or password.")
            return

        print("Logged in successfully.")
        self.open_dashboard()

    def open_dashboard(self):
        self.window.withdraw()

        Dashboard(
            parent=self.window,
            on_logout=self.show_login
        )

    def show_login(self):
        self.window.deiconify()
        self.username_entry.focus()


if __name__ == "__main__":
    login = Login()
    login.window.mainloop()