import customtkinter as ctk
from tkinter import messagebox
from frontend.dashboard import Dashboard


class LoginWindow:

    def __init__(self, root):
        self.root = root

        # ======================================================
        # COLORS
        # ======================================================

        self.BLUE = "#1769D1"
        self.DARK_BLUE = "#0B3D91"
        self.LIGHT_BLUE = "#EAF3FF"

        self.WHITE = "#FFFFFF"
        self.BG = "#F5F7FA"

        self.DARK = "#17202A"
        self.GRAY = "#6B7280"
        self.LIGHT_GRAY = "#9CA3AF"

        self.BORDER = "#D7E0EA"
        self.INPUT_BG = "#F8FAFC"

        # ======================================================
        # WINDOW
        # ======================================================

        self.root.title("Aztech Computer Store - POS")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)

        self.root.configure(
            fg_color=self.BG
        )

        self.create_login()

    # ==========================================================
    # LOGIN DESIGN
    # ==========================================================

    def create_login(self):

        # ======================================================
        # MAIN CONTAINER
        # ======================================================

        main = ctk.CTkFrame(
            self.root,
            fg_color=self.WHITE,
            corner_radius=0
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ======================================================
        # LEFT BRANDING PANEL
        # ======================================================

        left = ctk.CTkFrame(
            main,
            width=520,
            fg_color=self.BLUE,
            corner_radius=0
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        # ======================================================
        # TOP DARK BLUE STRIP
        # ======================================================

        ctk.CTkFrame(
            left,
            height=12,
            fg_color=self.DARK_BLUE,
            corner_radius=0
        ).pack(
            fill="x",
            side="top"
        )

        # ======================================================
        # BRAND CONTENT
        # ======================================================

        brand = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        brand.place(
            relx=0.5,
            rely=0.47,
            anchor="center"
        )

        # ======================================================
        # COMPUTER ICON
        # ======================================================

        icon_box = ctk.CTkFrame(
            brand,
            width=145,
            height=115,
            fg_color=self.WHITE,
            corner_radius=15
        )

        icon_box.pack(
            pady=(0, 25)
        )

        icon_box.pack_propagate(False)

        # Monitor body
        monitor = ctk.CTkFrame(
            icon_box,
            width=82,
            height=55,
            fg_color=self.BLUE,
            corner_radius=5
        )

        monitor.place(
            relx=0.5,
            rely=0.39,
            anchor="center"
        )

        # Monitor screen
        screen = ctk.CTkFrame(
            monitor,
            width=68,
            height=41,
            fg_color=self.WHITE,
            corner_radius=2
        )

        screen.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Monitor stand
        ctk.CTkFrame(
            icon_box,
            width=8,
            height=14,
            fg_color=self.BLUE,
            corner_radius=2
        ).place(
            relx=0.5,
            rely=0.68,
            anchor="center"
        )

        # Monitor base
        ctk.CTkFrame(
            icon_box,
            width=48,
            height=7,
            fg_color=self.BLUE,
            corner_radius=3
        ).place(
            relx=0.5,
            rely=0.78,
            anchor="center"
        )

        # ======================================================
        # STORE NAME
        # ======================================================

        ctk.CTkLabel(
            brand,
            text="AZTECH",
            font=ctk.CTkFont(
                size=42,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack()

        ctk.CTkLabel(
            brand,
            text="computer store",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color="#DCEBFF"
        ).pack(
            pady=(0, 8)
        )

        ctk.CTkLabel(
            brand,
            text="POINT OF SALE SYSTEM",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack()

        # ======================================================
        # STORE DESCRIPTION
        # ======================================================

        ctk.CTkLabel(
            brand,
            text="COMPUTER PARTS  •  ACCESSORIES  •  SERVICES",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color="#DCEBFF"
        ).pack(
            pady=(15, 0)
        )

        # ======================================================
        # RIGHT LOGIN PANEL
        # ======================================================

        right = ctk.CTkFrame(
            main,
            fg_color=self.WHITE,
            corner_radius=0
        )

        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ======================================================
        # LOGIN CARD
        # ======================================================

        card = ctk.CTkFrame(
            right,
            width=410,
            height=500,
            fg_color=self.WHITE,
            corner_radius=0
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        # ======================================================
        # STAFF LOGIN
        # ======================================================

        ctk.CTkLabel(
            card,
            text="STAFF LOGIN",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.BLUE
        ).pack(
            pady=(20, 8)
        )

        # ======================================================
        # WELCOME
        # ======================================================

        ctk.CTkLabel(
            card,
            text="Welcome Back!",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack()

        ctk.CTkLabel(
            card,
            text="Login to continue to your POS system",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.GRAY
        ).pack(
            pady=(7, 32)
        )

        # ======================================================
        # USERNAME LABEL
        # ======================================================

        ctk.CTkLabel(
            card,
            text="Username",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.DARK,
            anchor="w"
        ).pack(
            fill="x",
            padx=30
        )

        # ======================================================
        # USERNAME ENTRY
        # ======================================================

        self.username_entry = ctk.CTkEntry(
            card,
            width=350,
            height=46,
            corner_radius=8,
            border_width=1,
            border_color=self.BORDER,
            fg_color=self.INPUT_BG,
            text_color=self.DARK,
            placeholder_text="Enter username",
            placeholder_text_color=self.LIGHT_GRAY,
            font=ctk.CTkFont(
                size=13
            )
        )

        self.username_entry.pack(
            padx=30,
            pady=(8, 22)
        )

        # ======================================================
        # PASSWORD LABEL
        # ======================================================

        ctk.CTkLabel(
            card,
            text="Password",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.DARK,
            anchor="w"
        ).pack(
            fill="x",
            padx=30
        )

        # ======================================================
        # PASSWORD FRAME
        # ======================================================

        password_frame = ctk.CTkFrame(
            card,
            width=350,
            height=46,
            fg_color=self.INPUT_BG,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=8
        )

        password_frame.pack(
            padx=30,
            pady=(8, 25)
        )

        password_frame.pack_propagate(False)

        # ======================================================
        # PASSWORD ENTRY
        # ======================================================

        self.password_entry = ctk.CTkEntry(
            password_frame,
            height=44,
            fg_color="transparent",
            border_width=0,
            text_color=self.DARK,
            placeholder_text="Enter password",
            placeholder_text_color=self.LIGHT_GRAY,
            show="•",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.password_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        # ======================================================
        # SHOW PASSWORD
        # ======================================================

        self.show_password = False

        self.show_button = ctk.CTkButton(
            password_frame,
            text="Show",
            width=55,
            height=30,
            corner_radius=6,
            fg_color="transparent",
            hover_color=self.LIGHT_BLUE,
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            command=self.toggle_password
        )

        self.show_button.pack(
            side="right",
            padx=5
        )

        # ======================================================
        # LOGIN BUTTON
        # ======================================================

        ctk.CTkButton(
            card,
            text="LOGIN",
            width=350,
            height=48,
            corner_radius=8,
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.login
        ).pack(
            padx=30
        )

        # ======================================================
        # FOOTER
        # ======================================================

        ctk.CTkLabel(
            card,
            text="Aztech Computer Store",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.GRAY
        ).pack(
            pady=(25, 2)
        )

        ctk.CTkLabel(
            card,
            text="Computer Parts Management System",
            font=ctk.CTkFont(
                size=10
            ),
            text_color=self.LIGHT_GRAY
        ).pack()

        # ======================================================
        # ENTER KEY
        # ======================================================

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus()

    # ==========================================================
    # SHOW / HIDE PASSWORD
    # ==========================================================

    def toggle_password(self):

        self.show_password = not self.show_password

        if self.show_password:

            self.password_entry.configure(
                show=""
            )

            self.show_button.configure(
                text="Hide"
            )

        else:

            self.password_entry.configure(
                show="•"
            )

            self.show_button.configure(
                text="Show"
            )

    # ==========================================================
    # LOGIN
    # ==========================================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # ======================================================
        # CHECK EMPTY FIELDS
        # ======================================================

        if username == "" or password == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter your username and password.",
                parent=self.root
            )

            return

        # ======================================================
        # TEMPORARY LOGIN
        #
        # Username: admin
        # Password: admin
        # ======================================================

        if username == "admin" and password == "admin":

            self.open_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.",
                parent=self.root
            )

            self.password_entry.delete(
                0,
                "end"
            )

            self.password_entry.focus()

    # ==========================================================
    # OPEN DASHBOARD
    # ==========================================================

    def open_dashboard(self):

        self.root.withdraw()

        dashboard = Dashboard(self.root)

        dashboard.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_dashboard(dashboard)
        )

    # ==========================================================
    # CLOSE DASHBOARD
    # ==========================================================

    def close_dashboard(self, dashboard):

        dashboard.root.destroy()

        self.root.deiconify()

        self.username_entry.delete(
            0,
            "end"
        )

        self.password_entry.delete(
            0,
            "end"
        )

        self.username_entry.focus()


# ==============================================================
# RUN PROGRAM
# ==============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    app = LoginWindow(root)

    root.mainloop()