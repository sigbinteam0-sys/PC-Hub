"""Login window and authentication screen for Aztech POS."""
import customtkinter as ctk
from tkinter import messagebox

from frontend.theme import Theme
from frontend.dashboard import Dashboard


class BrandPanel(ctk.CTkFrame):
    """Left branding panel with computer store logo and information."""

    def __init__(self, parent, width: int = 460):
        super().__init__(parent, width=width, fg_color=Theme.PRIMARY, corner_radius=0)
        self.pack_propagate(False)

        # Top accent strip
        ctk.CTkFrame(self, height=10, fg_color=Theme.PRIMARY_DARK, corner_radius=0).pack(fill="x", side="top")

        # Centered Brand Content
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.48, anchor="center")

        # Monitor icon graphic
        icon_box = ctk.CTkFrame(center, width=130, height=105, fg_color=Theme.WHITE, corner_radius=14)
        icon_box.pack(pady=(0, 20))
        icon_box.pack_propagate(False)

        monitor = ctk.CTkFrame(icon_box, width=76, height=50, fg_color=Theme.PRIMARY, corner_radius=5)
        monitor.place(relx=0.5, rely=0.40, anchor="center")

        screen = ctk.CTkFrame(monitor, width=64, height=38, fg_color=Theme.WHITE, corner_radius=2)
        screen.place(relx=0.5, rely=0.5, anchor="center")

        # Display inner code-like lines
        ctk.CTkFrame(screen, width=32, height=4, fg_color=Theme.PRIMARY, corner_radius=2).place(relx=0.5, rely=0.36, anchor="center")
        ctk.CTkFrame(screen, width=44, height=4, fg_color=Theme.PRIMARY_DARK, corner_radius=2).place(relx=0.5, rely=0.58, anchor="center")

        # Stand & base
        ctk.CTkFrame(icon_box, width=12, height=14, fg_color=Theme.GRAY, corner_radius=0).place(relx=0.5, rely=0.74, anchor="center")
        ctk.CTkFrame(icon_box, width=42, height=6, fg_color=Theme.DARK, corner_radius=3).place(relx=0.5, rely=0.86, anchor="center")

        # Brand Text
        ctk.CTkLabel(
            center,
            text="AZTECH",
            font=Theme.font(34, "bold"),
            text_color=Theme.WHITE
        ).pack()

        ctk.CTkLabel(
            center,
            text="COMPUTER STORE",
            font=Theme.font(14, "bold"),
            text_color=Theme.PRIMARY_LIGHT
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            center,
            text="Point of Sale & Inventory System",
            font=Theme.font(12),
            text_color="#CADCF8"
        ).pack()

        # Version tag
        vbox = ctk.CTkFrame(center, fg_color=Theme.PRIMARY_DARK, corner_radius=12)
        vbox.pack(pady=(16, 0))
        ctk.CTkLabel(
            vbox,
            text="v1.0 • Enterprise Edition",
            font=Theme.font(11),
            text_color=Theme.WHITE
        ).pack(padx=14, pady=4)


class LoginWindow:
    """Authentication view controller for POS access."""

    # Backward-compatible color constants
    BLUE = Theme.PRIMARY
    DARK_BLUE = Theme.PRIMARY_DARK
    LIGHT_BLUE = Theme.PRIMARY_LIGHT
    WHITE = Theme.WHITE
    BG = Theme.BG
    DARK = Theme.DARK
    GRAY = Theme.GRAY
    BORDER = Theme.BORDER
    RED = Theme.DANGER

    def __init__(self, root):
        self.root = root
        self.root.title("Aztech Computer Store - POS & Inventory Login")
        self.root.resizable(True, True)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        app_w = min(960, screen_w - 40)
        app_h = min(620, screen_h - 60)
        x = max(0, (screen_w - app_w) // 2)
        y = max(0, (screen_h - app_h) // 2)

        self.root.geometry(f"{app_w}x{app_h}+{x}+{y}")
        self.root.minsize(860, 520)
        self.root.configure(fg_color=Theme.WHITE)

        self._show_password = False
        self._build_ui()

    def _build_ui(self):
        main = ctk.CTkFrame(self.root, fg_color=Theme.WHITE, corner_radius=0)
        main.pack(fill="both", expand=True)

        # Left branding panel
        BrandPanel(main, width=420).pack(side="left", fill="y")

        # Right login form panel
        right = ctk.CTkFrame(main, fg_color=Theme.WHITE, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)

        card = ctk.CTkFrame(right, width=380, fg_color=Theme.WHITE, corner_radius=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Titles
        ctk.CTkLabel(
            card,
            text="Sign In",
            font=Theme.font(28, "bold"),
            text_color=Theme.DARK,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            card,
            text="Welcome back! Please enter your admin credentials.",
            font=Theme.font(12),
            text_color=Theme.GRAY,
            anchor="w"
        ).pack(fill="x", pady=(4, 20))

        # Username Field
        ctk.CTkLabel(card, text="Username", font=Theme.font(12, "bold"), text_color=Theme.DARK, anchor="w").pack(fill="x")
        self.username_entry = ctk.CTkEntry(
            card, height=44, placeholder_text="Enter username (admin)",
            font=Theme.font(12), border_color=Theme.BORDER
        )
        self.username_entry.pack(fill="x", pady=(4, 14))

        # Password Field
        ctk.CTkLabel(card, text="Password", font=Theme.font(12, "bold"), text_color=Theme.DARK, anchor="w").pack(fill="x")

        pass_row = ctk.CTkFrame(card, fg_color="transparent")
        pass_row.pack(fill="x", pady=(4, 18))

        self.password_entry = ctk.CTkEntry(
            pass_row, height=44, placeholder_text="Enter password (admin)",
            show="•", font=Theme.font(12), border_color=Theme.BORDER
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.eye_btn = ctk.CTkButton(
            pass_row, text="👁", width=44, height=44, corner_radius=6,
            fg_color=Theme.BG, hover_color=Theme.BORDER, text_color=Theme.DARK,
            font=Theme.font(14), command=self.toggle_password
        )
        self.eye_btn.pack(side="right")

        # Submit button
        ctk.CTkButton(
            card, text="Sign In", height=44, corner_radius=8,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(13, "bold"), command=self.login
        ).pack(fill="x", pady=(6, 16))

        # Footer
        ctk.CTkLabel(
            card, text="Default Credentials: admin / admin",
            font=Theme.font(11), text_color=Theme.GRAY
        ).pack()

        # Keyboard Enter bindings
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        self.username_entry.focus()

    def toggle_password(self):
        self._show_password = not self._show_password
        if self._show_password:
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="🔒")
        else:
            self.password_entry.configure(show="•")
            self.eye_btn.configure(text="👁")

    def login(self):
        user = self.username_entry.get().strip()
        pw = self.password_entry.get().strip()

        if not user or not pw:
            messagebox.showwarning("Missing Info", "Please enter both username and password.", parent=self.root)
            return

        if user == "admin" and pw == "admin":
            self.open_dashboard()
        else:
            messagebox.showerror("Authentication Failed", "Invalid username or password.", parent=self.root)
            self.password_entry.delete(0, "end")
            self.password_entry.focus()

    def open_dashboard(self):
        self.root.withdraw()
        dash = Dashboard(self.root)
        dash.root.protocol("WM_DELETE_WINDOW", lambda: self.close_dashboard(dash))

    def close_dashboard(self, dash):
        dash.root.destroy()
        self.root.deiconify()
        self.password_entry.delete(0, "end")
        self.username_entry.focus()