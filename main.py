from frontend.login import LoginWindow
import customtkinter as ctk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

app = LoginWindow(root)

root.mainloop()