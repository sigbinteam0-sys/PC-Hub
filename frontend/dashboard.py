import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
import os

from frontend.inventory import Inventory


class Dashboard:

    # ==========================================================
    # COLORS
    # ==========================================================

    TEAL = "#1769D1"
    DARK_TEAL = "#0F4FA8"
    LIGHT_TEAL = "#EAF3FF"

    WHITE = "#FFFFFF"
    BG = "#F4F7FB"

    DARK = "#172033"
    GRAY = "#667085"
    BORDER = "#D6E0ED"

    RED = "#D66D70"

    IMAGE_GRAY = "#E8EEF5"

    # ==========================================================
    # INIT
    # ==========================================================

    def __init__(self, parent):

        self.parent = parent

        self.root = ctk.CTkToplevel(parent)
        self.root.title("Aztech Computer Store - POS")
        self.root.state("zoomed")
        self.root.configure(fg_color=self.BG)

        # ======================================================
        # CART
        # ======================================================

        self.cart = []
        self.cart_window = None

        # ======================================================
        # SALES RECORDS
        # ======================================================

        self.sales_records = []

        # ======================================================
        # PRODUCTS
        # ======================================================

        self.products = [

            # ==================================================
            # CPU
            # ==================================================

            {
                "name": "Intel Core i3",
                "category": "CPU",
                "description": "Desktop Processor",
                "price": 5200,
                "image": ""
            },
            {
                "name": "Intel Core i5",
                "category": "CPU",
                "description": "Computer Processor",
                "price": 8500,
                "image": ""
            },
            {
                "name": "Intel Core i7",
                "category": "CPU",
                "description": "High Performance Processor",
                "price": 14500,
                "image": ""
            },
            {
                "name": "Intel Core i9",
                "category": "CPU",
                "description": "Enthusiast Processor",
                "price": 28500,
                "image": ""
            },
            {
                "name": "AMD Ryzen 3",
                "category": "CPU",
                "description": "Desktop Processor",
                "price": 4800,
                "image": ""
            },
            {
                "name": "AMD Ryzen 5",
                "category": "CPU",
                "description": "Computer Processor",
                "price": 7500,
                "image": ""
            },
            {
                "name": "AMD Ryzen 7",
                "category": "CPU",
                "description": "High Performance Processor",
                "price": 13800,
                "image": ""
            },
            {
                "name": "AMD Ryzen 9",
                "category": "CPU",
                "description": "Enthusiast Processor",
                "price": 26500,
                "image": ""
            },

            # ==================================================
            # GPU
            # ==================================================

            {
                "name": "ASUS RTX 4060",
                "category": "GPU",
                "description": "Graphics Card",
                "price": 18500,
                "image": ""
            },
            {
                "name": "MSI RTX 4060",
                "category": "GPU",
                "description": "Graphics Card",
                "price": 19000,
                "image": ""
            },
            {
                "name": "Gigabyte RTX 4060",
                "category": "GPU",
                "description": "Graphics Card",
                "price": 18800,
                "image": ""
            },
            {
                "name": "MSI RTX 3060",
                "category": "GPU",
                "description": "Graphics Card",
                "price": 15500,
                "image": ""
            },
            {
                "name": "ASUS RTX 3050",
                "category": "GPU",
                "description": "Graphics Card",
                "price": 13500,
                "image": ""
            },
            {
                "name": "Gigabyte GTX 1660",
                "category": "GPU",
                "description": "Graphics Card",
                "price": 10500,
                "image": ""
            },

            # ==================================================
            # RAM
            # ==================================================

            {
                "name": "8GB DDR4 RAM",
                "category": "RAM",
                "description": "Desktop Memory",
                "price": 1800,
                "image": ""
            },
            {
                "name": "16GB DDR4 RAM",
                "category": "RAM",
                "description": "Desktop Memory",
                "price": 3200,
                "image": ""
            },
            {
                "name": "32GB DDR4 RAM",
                "category": "RAM",
                "description": "High Capacity Memory",
                "price": 5800,
                "image": ""
            },
            {
                "name": "8GB DDR5 RAM",
                "category": "RAM",
                "description": "DDR5 Desktop Memory",
                "price": 2500,
                "image": ""
            },
            {
                "name": "16GB DDR5 RAM",
                "category": "RAM",
                "description": "DDR5 Desktop Memory",
                "price": 4200,
                "image": ""
            },
            {
                "name": "32GB DDR5 RAM",
                "category": "RAM",
                "description": "High Performance DDR5",
                "price": 7500,
                "image": ""
            },

            # ==================================================
            # STORAGE
            # ==================================================

            {
                "name": "500GB SSD",
                "category": "Storage",
                "description": "Solid State Drive",
                "price": 2500,
                "image": ""
            },
            {
                "name": "1TB SSD",
                "category": "Storage",
                "description": "Solid State Drive",
                "price": 4200,
                "image": ""
            },
            {
                "name": "2TB SSD",
                "category": "Storage",
                "description": "High Capacity SSD",
                "price": 7200,
                "image": ""
            },
            {
                "name": "1TB HDD",
                "category": "Storage",
                "description": "Hard Disk Drive",
                "price": 2800,
                "image": ""
            },
            {
                "name": "2TB HDD",
                "category": "Storage",
                "description": "Hard Disk Drive",
                "price": 3900,
                "image": ""
            },

            # ==================================================
            # MOTHERBOARD
            # ==================================================

            {
                "name": "ASUS B550",
                "category": "Motherboard",
                "description": "AMD Motherboard",
                "price": 6500,
                "image": ""
            },
            {
                "name": "MSI B550",
                "category": "Motherboard",
                "description": "AMD Motherboard",
                "price": 6200,
                "image": ""
            },
            {
                "name": "ASRock B660",
                "category": "Motherboard",
                "description": "Intel Motherboard",
                "price": 6800,
                "image": ""
            },
            {
                "name": "Gigabyte B650",
                "category": "Motherboard",
                "description": "AMD AM5 Motherboard",
                "price": 8500,
                "image": ""
            },
            {
                "name": "ASUS H610",
                "category": "Motherboard",
                "description": "Intel Motherboard",
                "price": 4800,
                "image": ""
            },

            # ==================================================
            # PSU
            # ==================================================

            {
                "name": "550W Power Supply",
                "category": "PSU",
                "description": "Computer Power Supply",
                "price": 2800,
                "image": ""
            },
            {
                "name": "650W Power Supply",
                "category": "PSU",
                "description": "Computer Power Supply",
                "price": 3500,
                "image": ""
            },
            {
                "name": "750W Power Supply",
                "category": "PSU",
                "description": "Gaming Power Supply",
                "price": 4500,
                "image": ""
            },
            {
                "name": "850W Power Supply",
                "category": "PSU",
                "description": "High Performance PSU",
                "price": 5800,
                "image": ""
            },

            # ==================================================
            # OTHER
            # ==================================================

            {
                "name": "PC Case",
                "category": "Other",
                "description": "Computer Case",
                "price": 3000,
                "image": ""
            },
            {
                "name": "Gaming PC Case",
                "category": "Other",
                "description": "RGB Gaming Case",
                "price": 4500,
                "image": ""
            },
            {
                "name": "CPU Cooler",
                "category": "Other",
                "description": "Processor Cooler",
                "price": 1800,
                "image": ""
            },
            {
                "name": "120mm Case Fan",
                "category": "Other",
                "description": "Cooling Fan",
                "price": 450,
                "image": ""
            },

            # ==================================================
            # LAPTOP
            # ==================================================

            {
                "name": "ASUS Laptop",
                "category": "Other",
                "description": "Laptop Computer",
                "price": 28000,
                "image": ""
            },
            {
                "name": "Acer Laptop",
                "category": "Other",
                "description": "Laptop Computer",
                "price": 26000,
                "image": ""
            },
            {
                "name": "Lenovo Laptop",
                "category": "Other",
                "description": "Laptop Computer",
                "price": 27500,
                "image": ""
            },

            # ==================================================
            # MONITOR
            # ==================================================

            {
                "name": "22-inch Monitor",
                "category": "Other",
                "description": "Full HD Monitor",
                "price": 5200,
                "image": ""
            },
            {
                "name": "24-inch Monitor",
                "category": "Other",
                "description": "Full HD Computer Monitor",
                "price": 6500,
                "image": ""
            },
            {
                "name": "27-inch Gaming Monitor",
                "category": "Other",
                "description": "Gaming Monitor",
                "price": 9500,
                "image": ""
            },

            # ==================================================
            # ACCESSORIES
            # ==================================================

            {
                "name": "Gaming Keyboard",
                "category": "Other",
                "description": "USB Gaming Keyboard",
                "price": 1200,
                "image": ""
            },
            {
                "name": "Gaming Mouse",
                "category": "Other",
                "description": "USB Gaming Mouse",
                "price": 650,
                "image": ""
            },
            {
                "name": "Gaming Headset",
                "category": "Other",
                "description": "Computer Headset",
                "price": 1500,
                "image": ""
            },
            {
                "name": "Webcam",
                "category": "Other",
                "description": "USB Webcam",
                "price": 1800,
                "image": ""
            },
            {
                "name": "USB Hub",
                "category": "Other",
                "description": "USB Expansion Hub",
                "price": 650,
                "image": ""
            },

            # ==================================================
            # PRINTER
            # ==================================================

            {
                "name": "Epson Printer",
                "category": "Other",
                "description": "Ink Tank Printer",
                "price": 8500,
                "image": ""
            },
            {
                "name": "Canon Printer",
                "category": "Other",
                "description": "Ink Tank Printer",
                "price": 7800,
                "image": ""
            },
            {
                "name": "HP Printer",
                "category": "Other",
                "description": "All-in-One Printer",
                "price": 7200,
                "image": ""
            },

            # ==================================================
            # CCTV
            # ==================================================

            {
                "name": "CCTV Camera",
                "category": "Other",
                "description": "Security Camera",
                "price": 1800,
                "image": ""
            },
            {
                "name": "CCTV 4-Camera Set",
                "category": "Other",
                "description": "Complete CCTV Package",
                "price": 12500,
                "image": ""
            },
            {
                "name": "CCTV 8-Camera Set",
                "category": "Other",
                "description": "Complete CCTV Package",
                "price": 19500,
                "image": ""
            },

            # ==================================================
            # PISONET
            # ==================================================

            {
                "name": "Pisonet PC",
                "category": "Other",
                "description": "Pisonet Computer Set",
                "price": 18500,
                "image": ""
            },
            {
                "name": "Pisonet Cabinet",
                "category": "Other",
                "description": "Pisonet Computer Cabinet",
                "price": 3500,
                "image": ""
            },
            {
                "name": "Pisonet Timer",
                "category": "Other",
                "description": "Pisonet Timer System",
                "price": 1200,
                "image": ""
            }
        ]

        self.filtered_products = self.products.copy()

        self.product_page = 0
        self.products_per_page = 8

        # ======================================================
        # SALES PAGE VARIABLES
        # ======================================================

        self.today_sales_amount_label = None
        self.today_transactions_label = None

        self.month_sales_amount_label = None
        self.month_transactions_label = None

        self.sales_history_frame = None

        self.create_dashboard()

    # ==========================================================
    # IMAGE PATH
    # ==========================================================

    def get_product_image_path(self, image_path):

        if not image_path:
            return None

        # ------------------------------------------------------
        # 1. If image path is already absolute and exists
        # ------------------------------------------------------

        if os.path.isabs(image_path):

            if os.path.exists(image_path):
                return image_path

        # ------------------------------------------------------
        # 2. Try path exactly as provided
        # ------------------------------------------------------

        if os.path.exists(image_path):
            return os.path.abspath(image_path)

        # ------------------------------------------------------
        # 3. Project folder
        # ------------------------------------------------------

        project_folder = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        project_path = os.path.join(
            project_folder,
            image_path
        )

        if os.path.exists(project_path):
            return project_path

        # ------------------------------------------------------
        # 4. frontend/images
        # ------------------------------------------------------

        filename = os.path.basename(
            image_path
        )

        frontend_images = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "images",
            filename
        )

        if os.path.exists(frontend_images):
            return frontend_images

        return None

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def create_dashboard(self):

        content = ctk.CTkFrame(
            self.root,
            fg_color=self.BG,
            corner_radius=0
        )

        content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ======================================================
        # WELCOME BANNER
        # ======================================================

        welcome = ctk.CTkFrame(
            content,
            fg_color=self.TEAL,
            corner_radius=15
        )

        welcome.pack(
            fill="x",
            pady=(0, 10)
        )

        welcome_left = ctk.CTkFrame(
            welcome,
            fg_color="transparent"
        )

        welcome_left.pack(
            side="left",
            fill="x",
            expand=True,
            padx=22,
            pady=15
        )

        ctk.CTkLabel(
            welcome_left,
            text="🖥",
            font=ctk.CTkFont(size=28),
            text_color=self.WHITE
        ).pack(
            side="left",
            padx=(0, 14)
        )

        welcome_text = ctk.CTkFrame(
            welcome_left,
            fg_color="transparent"
        )

        welcome_text.pack(
            side="left"
        )

        ctk.CTkLabel(
            welcome_text,
            text="Welcome back, Admin! 👋",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color=self.WHITE,
            anchor="w"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            welcome_text,
            text="Choose a product or search for computer parts.",
            font=ctk.CTkFont(size=12),
            text_color=self.LIGHT_TEAL,
            anchor="w"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # ======================================================
        # PROFILE
        # ======================================================

        profile = ctk.CTkFrame(
            welcome,
            fg_color="transparent"
        )

        profile.pack(
            side="right",
            padx=18
        )

        avatar = ctk.CTkFrame(
            profile,
            width=40,
            height=40,
            fg_color=self.WHITE,
            corner_radius=20
        )

        avatar.pack(
            side="left",
            padx=(0, 8)
        )

        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="A",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=self.TEAL
        ).pack(
            expand=True
        )

        ctk.CTkLabel(
            profile,
            text="Admin",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            profile,
            text="Log out",
            width=75,
            height=32,
            corner_radius=8,
            fg_color="#FFF1F1",
            hover_color="#FFE0E0",
            text_color=self.RED,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.logout
        ).pack(
            side="left"
        )

        # ======================================================
        # NAVIGATION
        # ======================================================

        navigation = ctk.CTkFrame(
            content,
            fg_color=self.TEAL,
            corner_radius=10,
            height=42
        )

        navigation.pack(
            fill="x",
            pady=(0, 10)
        )

        navigation.pack_propagate(False)

        nav_inner = ctk.CTkFrame(
            navigation,
            fg_color="transparent"
        )

        nav_inner.pack(
            expand=True
        )

        self.products_nav = ctk.CTkButton(
            nav_inner,
            text="Products",
            width=105,
            height=30,
            corner_radius=15,
            fg_color=self.DARK_TEAL,
            hover_color=self.DARK_TEAL,
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.show_products
        )

        self.products_nav.pack(
            side="left",
            padx=3,
            pady=6
        )

        self.inventory_nav = ctk.CTkButton(
            nav_inner,
            text="Inventory",
            width=105,
            height=30,
            corner_radius=15,
            fg_color=self.WHITE,
            hover_color=self.LIGHT_TEAL,
            text_color=self.DARK,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.open_inventory
        )

        self.inventory_nav.pack(
            side="left",
            padx=3,
            pady=6
        )

        self.sales_nav = ctk.CTkButton(
            nav_inner,
            text="Sales",
            width=105,
            height=30,
            corner_radius=15,
            fg_color=self.WHITE,
            hover_color=self.LIGHT_TEAL,
            text_color=self.DARK,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.open_sales
        )

        self.sales_nav.pack(
            side="left",
            padx=3,
            pady=6
        )

        # ======================================================
        # DYNAMIC PAGE AREA
        # ======================================================

        self.page_frame = ctk.CTkFrame(
            content,
            fg_color=self.BG,
            corner_radius=0
        )

        self.page_frame.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )

        self.show_products_page()

        # ======================================================
        # CART BAR
        # ======================================================

        self.cart_frame = ctk.CTkFrame(
            content,
            height=55,
            fg_color=self.TEAL,
            corner_radius=10
        )

        self.cart_frame.pack(
            fill="x"
        )

        self.cart_frame.pack_propagate(False)

        self.total_label = ctk.CTkLabel(
            self.cart_frame,
            text="Cart Total: ₱0.00",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=self.WHITE
        )

        self.total_label.pack(
            side="left",
            padx=18
        )

        ctk.CTkButton(
            self.cart_frame,
            text="View Cart →",
            width=110,
            height=36,
            corner_radius=8,
            fg_color=self.WHITE,
            hover_color="#E5E5E5",
            text_color=self.TEAL,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.open_cart
        ).pack(
            side="right",
            padx=10
        )

    # ==========================================================
    # SHOW PRODUCTS PAGE
    # ==========================================================

    def show_products_page(self):

        for widget in self.page_frame.winfo_children():
            widget.destroy()

        # ======================================================
        # SEARCH
        # ======================================================

        search_frame = ctk.CTkFrame(
            self.page_frame,
            fg_color=self.WHITE,
            corner_radius=10,
            height=58
        )

        search_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        search_frame.pack_propagate(False)

        ctk.CTkLabel(
            search_frame,
            text="Product",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            side="left",
            padx=(18, 15)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=40,
            width=350,
            placeholder_text="🔍  Search products...",
            border_width=1,
            border_color=self.BORDER,
            fg_color=self.WHITE,
            font=ctk.CTkFont(size=13)
        )

        self.search_entry.pack(
            side="right",
            padx=(5, 7),
            pady=9
        )

        ctk.CTkButton(
            search_frame,
            text="🔍  Search",
            width=90,
            height=36,
            corner_radius=8,
            fg_color=self.TEAL,
            hover_color=self.DARK_TEAL,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.search_products
        ).pack(
            side="right",
            padx=(5, 7)
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_products()
        )

        # ======================================================
        # CATEGORIES
        # ======================================================

        category_frame = ctk.CTkFrame(
            self.page_frame,
            fg_color=self.TEAL,
            corner_radius=10
        )

        category_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        categories = [
            "All",
            "CPU",
            "GPU",
            "RAM",
            "Storage",
            "Motherboard",
            "PSU",
            "Other"
        ]

        self.category_buttons = {}

        for category in categories:

            button = ctk.CTkButton(
                category_frame,
                text=category,
                height=34,
                corner_radius=7,
                fg_color=(
                    self.DARK_TEAL
                    if category == "All"
                    else self.WHITE
                ),
                hover_color=self.LIGHT_TEAL,
                text_color=(
                    self.WHITE
                    if category == "All"
                    else self.DARK
                ),
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                command=lambda c=category:
                    self.filter_category(c)
            )

            button.pack(
                side="left",
                fill="x",
                expand=True,
                padx=3,
                pady=6
            )

            self.category_buttons[category] = button

        # ======================================================
        # PRODUCTS SECTION
        # ======================================================

        product_section = ctk.CTkFrame(
            self.page_frame,
            fg_color=self.TEAL,
            corner_radius=15
        )

        product_section.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            product_section,
            text="PRODUCTS",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack(
            pady=(8, 3)
        )

        product_navigation = ctk.CTkFrame(
            product_section,
            fg_color="transparent"
        )

        product_navigation.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8)
        )

        self.left_product_button = ctk.CTkButton(
            product_navigation,
            text="‹",
            width=42,
            height=55,
            corner_radius=10,
            fg_color=self.WHITE,
            hover_color=self.LIGHT_TEAL,
            text_color=self.TEAL,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            command=self.previous_product_page
        )

        self.left_product_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.product_area = ctk.CTkFrame(
            product_navigation,
            fg_color="transparent"
        )

        self.product_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        for column in range(4):

            self.product_area.grid_columnconfigure(
                column,
                weight=1,
                uniform="product"
            )

        for row in range(2):

            self.product_area.grid_rowconfigure(
                row,
                weight=1,
                uniform="product"
            )

        self.right_product_button = ctk.CTkButton(
            product_navigation,
            text="›",
            width=42,
            height=55,
            corner_radius=10,
            fg_color=self.WHITE,
            hover_color=self.LIGHT_TEAL,
            text_color=self.TEAL,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            command=self.next_product_page
        )

        self.right_product_button.pack(
            side="right",
            padx=(8, 0)
        )

        self.create_product_cards()

    # ==========================================================
    # PRODUCT CARDS
    # ==========================================================

    def create_product_cards(self):

        for widget in self.product_area.winfo_children():
            widget.destroy()

        total_products = len(self.filtered_products)

        if total_products == 0:

            ctk.CTkLabel(
                self.product_area,
                text="No products found.",
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                ),
                text_color=self.WHITE
            ).grid(
                row=0,
                column=0,
                columnspan=4,
                pady=50
            )

            self.left_product_button.configure(
                state="disabled"
            )

            self.right_product_button.configure(
                state="disabled"
            )

            return

        start = self.product_page * self.products_per_page
        end = start + self.products_per_page

        visible_products = self.filtered_products[start:end]

        for index, product in enumerate(visible_products):

            row = index // 4
            column = index % 4

            card = ctk.CTkFrame(
                self.product_area,
                fg_color=self.WHITE,
                corner_radius=15,
                border_width=1,
                border_color=self.BORDER
            )

            card.grid(
                row=row,
                column=column,
                padx=6,
                pady=6,
                sticky="nsew"
            )

            card.grid_propagate(False)

            # ==================================================
            # IMAGE
            # ==================================================

            image_frame = ctk.CTkFrame(
                card,
                height=125,
                fg_color=self.IMAGE_GRAY,
                corner_radius=10
            )

            image_frame.pack(
                fill="x",
                padx=10,
                pady=(10, 8)
            )

            image_frame.pack_propagate(False)

            image_path = (
                product.get("image")
                or product.get("image_path")
                or product.get("picture")
                or product.get("picture_path")
            )

            # --------------------------------------------------
            # FIX IMAGE PATH
            # --------------------------------------------------

            image_path = self.get_product_image_path(
                image_path
            )

            product_image = None

            if image_path:

                try:

                    original_image = Image.open(
                        image_path
                    )

                    original_image.load()

                    product_image = ctk.CTkImage(
                        light_image=original_image,
                        dark_image=original_image,
                        size=(180, 105)
                    )

                    print(
                        f"Product image loaded: {image_path}"
                    )

                except Exception as error:

                    print(
                        f"Could not load image: {image_path}"
                    )

                    print(
                        f"Image error: {error}"
                    )

                    product_image = None

            if product_image is not None:

                image_label = ctk.CTkLabel(
                    image_frame,
                    text="",
                    image=product_image
                )

                image_label.pack(
                    expand=True
                )

                image_label.image = product_image

            else:

                ctk.CTkLabel(
                    image_frame,
                    text="PRODUCT IMAGE",
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    ),
                    text_color="#8996A8"
                ).pack(
                    expand=True
                )

            # ==================================================
            # PRODUCT INFORMATION
            # ==================================================

            info = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            info.pack(
                fill="both",
                expand=True,
                padx=12
            )

            ctk.CTkLabel(
                info,
                text=product["name"],
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                text_color=self.DARK,
                anchor="w"
            ).pack(
                fill="x",
                pady=(2, 0)
            )

            ctk.CTkLabel(
                info,
                text=product["category"],
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                text_color=self.TEAL,
                anchor="w"
            ).pack(
                fill="x",
                pady=(4, 0)
            )

            ctk.CTkLabel(
                info,
                text=product["description"],
                font=ctk.CTkFont(
                    size=10
                ),
                text_color=self.GRAY,
                anchor="w"
            ).pack(
                fill="x",
                pady=(4, 0)
            )

            # ==================================================
            # PRICE + BUTTONS
            # ==================================================

            bottom = ctk.CTkFrame(
                info,
                fg_color="transparent"
            )

            bottom.pack(
                fill="x",
                side="bottom",
                pady=(8, 10)
            )

            ctk.CTkLabel(
                bottom,
                text=f"₱{product['price']:,.2f}",
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                text_color=self.DARK
            ).pack(
                side="left"
            )

            button_frame = ctk.CTkFrame(
                bottom,
                fg_color="transparent"
            )

            button_frame.pack(
                side="right"
            )

            ctk.CTkButton(
                button_frame,
                text="Buy Now",
                width=75,
                height=30,
                corner_radius=7,
                fg_color=self.DARK_TEAL,
                hover_color=self.TEAL,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                command=lambda p=product:
                    self.buy_now(p)
            ).pack(
                side="left",
                padx=(0, 5)
            )

            ctk.CTkButton(
                button_frame,
                text="Add to Cart",
                width=85,
                height=30,
                corner_radius=7,
                fg_color=self.TEAL,
                hover_color=self.DARK_TEAL,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                command=lambda p=product:
                    self.add_to_cart(p)
            ).pack(
                side="left"
            )

        # ======================================================
        # PAGE BUTTONS
        # ======================================================

        total_pages = (
            total_products
            + self.products_per_page
            - 1
        ) // self.products_per_page

        if self.product_page <= 0:

            self.left_product_button.configure(
                state="disabled"
            )

        else:

            self.left_product_button.configure(
                state="normal"
            )

        if self.product_page >= total_pages - 1:

            self.right_product_button.configure(
                state="disabled"
            )

        else:

            self.right_product_button.configure(
                state="normal"
            )

    # ==========================================================
    # NEXT PAGE
    # ==========================================================

    def next_product_page(self):

        total_pages = (
            len(self.filtered_products)
            + self.products_per_page
            - 1
        ) // self.products_per_page

        if self.product_page < total_pages - 1:

            self.product_page += 1

            self.create_product_cards()

    # ==========================================================
    # PREVIOUS PAGE
    # ==========================================================

    def previous_product_page(self):

        if self.product_page > 0:

            self.product_page -= 1

            self.create_product_cards()

    # ==========================================================
    # ADD TO CART
    # ==========================================================

    def add_to_cart(self, product):

        for item in self.cart:

            if item["product"]["name"] == product["name"]:

                item["quantity"] += 1

                self.update_cart_total()

                return

        self.cart.append({
            "product": product,
            "quantity": 1
        })

        self.update_cart_total()

    # ==========================================================
    # BUY NOW
    # ==========================================================

    def buy_now(self, product):

        self.open_payment(
            cart_items=[
                {
                    "product": product,
                    "quantity": 1
                }
            ],
            clear_cart_after_payment=False
        )

    # ==========================================================
    # UPDATE CART TOTAL
    # ==========================================================

    def update_cart_total(self):

        total = sum(
            item["product"]["price"] * item["quantity"]
            for item in self.cart
        )

        self.total_label.configure(
            text=f"Cart Total: ₱{total:,.2f}"
        )

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_products(self):

        keyword = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if keyword == "":

            self.filtered_products = (
                self.products.copy()
            )

        else:

            self.filtered_products = [
                product
                for product in self.products
                if (
                    keyword in product["name"].lower()
                    or keyword in product["category"].lower()
                    or keyword in product["description"].lower()
                )
            ]

        self.product_page = 0

        self.create_product_cards()

    # ==========================================================
    # CATEGORY FILTER
    # ==========================================================

    def filter_category(self, category):

        if category == "All":

            self.filtered_products = (
                self.products.copy()
            )

        else:

            self.filtered_products = [
                product
                for product in self.products
                if product["category"] == category
            ]

        self.product_page = 0

        for name, button in self.category_buttons.items():

            if name == category:

                button.configure(
                    fg_color=self.DARK_TEAL,
                    text_color=self.WHITE
                )

            else:

                button.configure(
                    fg_color=self.WHITE,
                    text_color=self.DARK
                )

        self.create_product_cards()

    # ==========================================================
    # PRODUCTS
    # ==========================================================

    def show_products(self):

        if hasattr(self, "cart_frame"):

            self.cart_frame.pack(
                fill="x"
            )

        self.filtered_products = (
            self.products.copy()
        )

        self.product_page = 0

        self.products_nav.configure(
            fg_color=self.DARK_TEAL,
            text_color=self.WHITE
        )

        self.inventory_nav.configure(
            fg_color=self.WHITE,
            text_color=self.DARK
        )

        self.sales_nav.configure(
            fg_color=self.WHITE,
            text_color=self.DARK
        )

        self.show_products_page()

    # ==========================================================
    # REFRESH PRODUCTS
    # ==========================================================

    def refresh_products(self):

        self.filtered_products = (
            self.products.copy()
        )

        self.product_page = 0

        self.show_products_page()

    # ==========================================================
    # INVENTORY
    # ==========================================================

    def open_inventory(self):

        if hasattr(self, "cart_frame"):

            self.cart_frame.pack_forget()

        for widget in self.page_frame.winfo_children():
            widget.destroy()

        self.products_nav.configure(
            fg_color=self.WHITE,
            text_color=self.DARK
        )

        self.inventory_nav.configure(
            fg_color=self.DARK_TEAL,
            text_color=self.WHITE
        )

        self.sales_nav.configure(
            fg_color=self.WHITE,
            text_color=self.DARK
        )

        Inventory(
            self.page_frame,
            self.products
        )

    # ==========================================================
    # SALES
    # ==========================================================

    def open_sales(self):

        if hasattr(self, "cart_frame"):

            self.cart_frame.pack_forget()

        for widget in self.page_frame.winfo_children():
            widget.destroy()

        self.products_nav.configure(
            fg_color=self.WHITE,
            text_color=self.DARK
        )

        self.inventory_nav.configure(
            fg_color=self.WHITE,
            text_color=self.DARK
        )

        self.sales_nav.configure(
            fg_color=self.DARK_TEAL,
            text_color=self.WHITE
        )

        sales_frame = ctk.CTkFrame(
            self.page_frame,
            fg_color=self.BG,
            corner_radius=0
        )

        sales_frame.pack(
            fill="both",
            expand=True
        )

        sales_container = ctk.CTkFrame(
            sales_frame,
            fg_color=self.WHITE,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )

        sales_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        summary_frame = ctk.CTkFrame(
            sales_container,
            fg_color="transparent"
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        summary_frame.grid_columnconfigure(
            0,
            weight=1
        )

        summary_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # ======================================================
        # TODAY
        # ======================================================

        today_frame = ctk.CTkFrame(
            summary_frame,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=2,
            border_color=self.TEAL
        )

        today_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        ctk.CTkLabel(
            today_frame,
            text="Sales for this day",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        self.today_sales_amount_label = ctk.CTkLabel(
            today_frame,
            text="₱0.00",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            ),
            text_color=self.TEAL
        )

        self.today_sales_amount_label.pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            today_frame,
            text="Total sales today",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.GRAY
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        self.today_transactions_label = ctk.CTkLabel(
            today_frame,
            text="Transactions: 0",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.DARK
        )

        self.today_transactions_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ======================================================
        # MONTH
        # ======================================================

        month_frame = ctk.CTkFrame(
            summary_frame,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=2,
            border_color=self.TEAL
        )

        month_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        ctk.CTkLabel(
            month_frame,
            text="Sales for this Month",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        self.month_sales_amount_label = ctk.CTkLabel(
            month_frame,
            text="₱0.00",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            ),
            text_color=self.TEAL
        )

        self.month_sales_amount_label.pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            month_frame,
            text="Total sales this month",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.GRAY
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        self.month_transactions_label = ctk.CTkLabel(
            month_frame,
            text="Transactions: 0",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.DARK
        )

        self.month_transactions_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ======================================================
        # HISTORY HEADER
        # ======================================================

        history_header = ctk.CTkFrame(
            sales_container,
            fg_color="transparent"
        )

        history_header.pack(
            fill="x",
            padx=20,
            pady=(8, 5)
        )

        ctk.CTkLabel(
            history_header,
            text="Transaction History",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            history_header,
            text="Refresh",
            width=85,
            height=30,
            corner_radius=7,
            fg_color=self.TEAL,
            hover_color=self.DARK_TEAL,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            command=self.refresh_sales_page
        ).pack(
            side="right"
        )

        # ======================================================
        # HISTORY
        # ======================================================

        self.sales_history_frame = ctk.CTkScrollableFrame(
            sales_container,
            fg_color=self.BG,
            corner_radius=8
        )

        self.sales_history_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.refresh_sales_page()

    # ==========================================================
    # REFRESH SALES PAGE
    # ==========================================================

    def refresh_sales_page(self):

        now = datetime.now()

        today = now.date()
        current_year = now.year
        current_month = now.month

        today_records = [
            record
            for record in self.sales_records
            if record["date"].date() == today
        ]

        today_total = sum(
            record["total"]
            for record in today_records
        )

        today_transactions = len(
            today_records
        )

        month_records = [
            record
            for record in self.sales_records
            if (
                record["date"].year == current_year
                and record["date"].month == current_month
            )
        ]

        month_total = sum(
            record["total"]
            for record in month_records
        )

        month_transactions = len(
            month_records
        )

        if (
            self.today_sales_amount_label is not None
            and self.today_sales_amount_label.winfo_exists()
        ):

            self.today_sales_amount_label.configure(
                text=f"₱{today_total:,.2f}"
            )

        if (
            self.today_transactions_label is not None
            and self.today_transactions_label.winfo_exists()
        ):

            self.today_transactions_label.configure(
                text=f"Transactions: {today_transactions}"
            )

        if (
            self.month_sales_amount_label is not None
            and self.month_sales_amount_label.winfo_exists()
        ):

            self.month_sales_amount_label.configure(
                text=f"₱{month_total:,.2f}"
            )

        if (
            self.month_transactions_label is not None
            and self.month_transactions_label.winfo_exists()
        ):

            self.month_transactions_label.configure(
                text=f"Transactions: {month_transactions}"
            )

        if self.sales_history_frame is None:
            return

        if not self.sales_history_frame.winfo_exists():
            return

        for widget in self.sales_history_frame.winfo_children():
            widget.destroy()

        if len(self.sales_records) == 0:

            ctk.CTkLabel(
                self.sales_history_frame,
                text="No transactions yet.",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                ),
                text_color=self.GRAY
            ).pack(
                pady=50
            )

            return

        records = list(
            reversed(self.sales_records)
        )

        for index, record in enumerate(
            records,
            start=1
        ):

            transaction_frame = ctk.CTkFrame(
                self.sales_history_frame,
                fg_color=self.WHITE,
                corner_radius=10,
                border_width=1,
                border_color=self.BORDER
            )

            transaction_frame.pack(
                fill="x",
                pady=5
            )

            header = ctk.CTkFrame(
                transaction_frame,
                fg_color="transparent"
            )

            header.pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            transaction_number = (
                len(self.sales_records)
                - index
                + 1
            )

            ctk.CTkLabel(
                header,
                text=f"Transaction #{transaction_number}",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.DARK
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                header,
                text=record["date"].strftime(
                    "%B %d, %Y  •  %I:%M %p"
                ),
                font=ctk.CTkFont(
                    size=10
                ),
                text_color=self.GRAY
            ).pack(
                side="right"
            )

            items_frame = ctk.CTkFrame(
                transaction_frame,
                fg_color=self.BG,
                corner_radius=8
            )

            items_frame.pack(
                fill="x",
                padx=15,
                pady=5
            )

            for item in record["items"]:

                item_name = item["name"]
                quantity = item["quantity"]
                price = item["price"]

                subtotal = price * quantity

                item_row = ctk.CTkFrame(
                    items_frame,
                    fg_color="transparent"
                )

                item_row.pack(
                    fill="x",
                    padx=10,
                    pady=4
                )

                ctk.CTkLabel(
                    item_row,
                    text=f"{item_name}  x{quantity}",
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    ),
                    text_color=self.DARK,
                    anchor="w"
                ).pack(
                    side="left"
                )

                ctk.CTkLabel(
                    item_row,
                    text=f"₱{subtotal:,.2f}",
                    font=ctk.CTkFont(
                        size=11
                    ),
                    text_color=self.DARK
                ).pack(
                    side="right"
                )

            payment_info = ctk.CTkFrame(
                transaction_frame,
                fg_color="transparent"
            )

            payment_info.pack(
                fill="x",
                padx=15,
                pady=(5, 12)
            )

            total_frame = ctk.CTkFrame(
                payment_info,
                fg_color="transparent"
            )

            total_frame.pack(
                side="left",
                expand=True,
                fill="x"
            )

            ctk.CTkLabel(
                total_frame,
                text="TOTAL",
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                ),
                text_color=self.GRAY
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                total_frame,
                text=f"₱{record['total']:,.2f}",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                ),
                text_color=self.TEAL
            ).pack(
                anchor="w"
            )

            cash_frame = ctk.CTkFrame(
                payment_info,
                fg_color="transparent"
            )

            cash_frame.pack(
                side="left",
                expand=True,
                fill="x"
            )

            ctk.CTkLabel(
                cash_frame,
                text="CASH RECEIVED",
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                ),
                text_color=self.GRAY
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                cash_frame,
                text=f"₱{record['cash']:,.2f}",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.DARK
            ).pack(
                anchor="w"
            )

            change_frame = ctk.CTkFrame(
                payment_info,
                fg_color="transparent"
            )

            change_frame.pack(
                side="right",
                expand=True,
                fill="x"
            )

            ctk.CTkLabel(
                change_frame,
                text="CHANGE",
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                ),
                text_color=self.GRAY
            ).pack(
                anchor="e"
            )

            ctk.CTkLabel(
                change_frame,
                text=f"₱{record['change']:,.2f}",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.TEAL
            ).pack(
                anchor="e"
            )

    # ==========================================================
    # RECORD SALE
    # ==========================================================

    def record_sale(
        self,
        cart_items,
        total,
        cash,
        change
    ):

        sale_record = {
            "date": datetime.now(),
            "items": [],
            "total": total,
            "cash": cash,
            "change": change
        }

        for item in cart_items:

            product = item["product"]

            sale_record["items"].append({
                "name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "quantity": item["quantity"]
            })

        self.sales_records.append(
            sale_record
        )

        self.refresh_sales_page()

    # ==========================================================
    # CART
    # ==========================================================

    def open_cart(self):

        if not self.cart:

            messagebox.showinfo(
                "Shopping Cart",
                "Your cart is currently empty."
            )

            return

        if (
            self.cart_window is not None
            and self.cart_window.winfo_exists()
        ):

            self.cart_window.destroy()

        self.cart_window = ctk.CTkToplevel(
            self.root
        )

        self.cart_window.title(
            "Shopping Cart"
        )

        self.cart_window.geometry(
            "720x600"
        )

        self.cart_window.resizable(
            False,
            False
        )

        self.cart_window.configure(
            fg_color=self.BG
        )

        self.cart_window.transient(
            self.root
        )

        self.cart_window.grab_set()

        header = ctk.CTkFrame(
            self.cart_window,
            height=70,
            fg_color=self.TEAL,
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        ctk.CTkLabel(
            header,
            text="SHOPPING CART",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack(
            side="left",
            padx=25
        )

        ctk.CTkLabel(
            header,
            text="Edit your order before payment",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.LIGHT_TEAL
        ).pack(
            side="right",
            padx=25
        )

        self.cart_items_frame = ctk.CTkScrollableFrame(
            self.cart_window,
            fg_color="transparent"
        )

        self.cart_items_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        footer = ctk.CTkFrame(
            self.cart_window,
            fg_color=self.WHITE,
            corner_radius=10
        )

        footer.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.cart_grand_total_label = ctk.CTkLabel(
            footer,
            text="Grand Total: ₱0.00",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=self.DARK
        )

        self.cart_grand_total_label.pack(
            side="left",
            padx=18,
            pady=15
        )

        ctk.CTkButton(
            footer,
            text="Proceed to Pay",
            width=145,
            height=40,
            corner_radius=8,
            fg_color=self.DARK_TEAL,
            hover_color=self.TEAL,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.proceed_to_pay
        ).pack(
            side="right",
            padx=(5, 10),
            pady=10
        )

        ctk.CTkButton(
            footer,
            text="Close",
            width=85,
            height=40,
            corner_radius=8,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=self.DARK,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.cart_window.destroy
        ).pack(
            side="right",
            pady=10
        )

        self.refresh_cart_window()

    # ==========================================================
    # REFRESH CART
    # ==========================================================

    def refresh_cart_window(self):

        if (
            self.cart_window is None
            or not self.cart_window.winfo_exists()
        ):
            return

        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        if not self.cart:

            ctk.CTkLabel(
                self.cart_items_frame,
                text="Your cart is empty.",
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                ),
                text_color=self.GRAY
            ).pack(
                pady=80
            )

            self.cart_grand_total_label.configure(
                text="Grand Total: ₱0.00"
            )

            return

        total = 0

        for index, item in enumerate(
            self.cart
        ):

            product = item["product"]
            quantity = item["quantity"]

            subtotal = (
                product["price"]
                * quantity
            )

            total += subtotal

            row = ctk.CTkFrame(
                self.cart_items_frame,
                fg_color=self.WHITE,
                corner_radius=10,
                border_width=1,
                border_color=self.BORDER
            )

            row.pack(
                fill="x",
                pady=5
            )

            details = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            details.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=12
            )

            ctk.CTkLabel(
                details,
                text=product["name"],
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.DARK,
                anchor="w"
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                details,
                text=f"₱{product['price']:,.2f} each",
                font=ctk.CTkFont(
                    size=10
                ),
                text_color=self.GRAY,
                anchor="w"
            ).pack(
                anchor="w",
                pady=(2, 0)
            )

            quantity_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            quantity_frame.pack(
                side="left",
                padx=10
            )

            ctk.CTkButton(
                quantity_frame,
                text="−",
                width=32,
                height=30,
                corner_radius=7,
                fg_color="#E5E7EB",
                hover_color="#D1D5DB",
                text_color=self.DARK,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                command=lambda i=index:
                    self.change_cart_quantity(
                        i,
                        -1
                    )
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                quantity_frame,
                text=str(quantity),
                width=35,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                text_color=self.DARK
            ).pack(
                side="left"
            )

            ctk.CTkButton(
                quantity_frame,
                text="+",
                width=32,
                height=30,
                corner_radius=7,
                fg_color=self.TEAL,
                hover_color=self.DARK_TEAL,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                command=lambda i=index:
                    self.change_cart_quantity(
                        i,
                        1
                    )
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row,
                text=f"₱{subtotal:,.2f}",
                width=105,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                text_color=self.DARK
            ).pack(
                side="left",
                padx=5
            )

            ctk.CTkButton(
                row,
                text="Remove",
                width=65,
                height=30,
                corner_radius=7,
                fg_color="#FFF1F1",
                hover_color="#FFE0E0",
                text_color=self.RED,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                ),
                command=lambda i=index:
                    self.remove_from_cart(i)
            ).pack(
                side="right",
                padx=12
            )

        self.cart_grand_total_label.configure(
            text=f"Grand Total: ₱{total:,.2f}"
        )

    # ==========================================================
    # CHANGE QUANTITY
    # ==========================================================

    def change_cart_quantity(
        self,
        index,
        amount
    ):

        if index < 0 or index >= len(self.cart):
            return

        self.cart[index]["quantity"] += amount

        if self.cart[index]["quantity"] <= 0:

            self.cart.pop(index)

        self.update_cart_total()
        self.refresh_cart_window()

    # ==========================================================
    # REMOVE
    # ==========================================================

    def remove_from_cart(self, index):

        if 0 <= index < len(self.cart):

            self.cart.pop(index)

            self.update_cart_total()
            self.refresh_cart_window()

    # ==========================================================
    # PROCEED TO PAY
    # ==========================================================

    def proceed_to_pay(self):

        if not self.cart:
            return

        self.open_payment(
            cart_items=self.cart.copy(),
            clear_cart_after_payment=True
        )

    # ==========================================================
    # PAYMENT
    # ==========================================================

    def open_payment(
        self,
        cart_items,
        clear_cart_after_payment=False
    ):

        total = sum(
            item["product"]["price"]
            * item["quantity"]
            for item in cart_items
        )

        payment = ctk.CTkToplevel(
            self.root
        )

        payment.title(
            "Payment"
        )

        payment.geometry(
            "480x560"
        )

        payment.resizable(
            False,
            False
        )

        payment.configure(
            fg_color=self.BG
        )

        payment.transient(
            self.root
        )

        payment.grab_set()

        header = ctk.CTkFrame(
            payment,
            height=75,
            fg_color=self.TEAL,
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        ctk.CTkLabel(
            header,
            text="PAYMENT",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack(
            expand=True
        )

        summary = ctk.CTkFrame(
            payment,
            fg_color=self.WHITE,
            corner_radius=10
        )

        summary.pack(
            fill="x",
            padx=25,
            pady=20
        )

        for item in cart_items:

            product = item["product"]
            quantity = item["quantity"]

            subtotal = (
                product["price"]
                * quantity
            )

            ctk.CTkLabel(
                summary,
                text=(
                    f"{product['name']}  "
                    f"x{quantity}    "
                    f"₱{subtotal:,.2f}"
                ),
                font=ctk.CTkFont(
                    size=11
                ),
                text_color=self.DARK,
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=4
            )

        ctk.CTkLabel(
            summary,
            text=f"TOTAL DUE: ₱{total:,.2f}",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 15)
        )

        ctk.CTkLabel(
            payment,
            text="Cash Received",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=25
        )

        cash_entry = ctk.CTkEntry(
            payment,
            height=42,
            placeholder_text="Enter customer's cash",
            font=ctk.CTkFont(
                size=13
            )
        )

        cash_entry.pack(
            fill="x",
            padx=25,
            pady=(6, 15)
        )

        change_label = ctk.CTkLabel(
            payment,
            text="Change: ₱0.00",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color=self.TEAL
        )

        change_label.pack(
            pady=(0, 18)
        )

        def calculate_change(event=None):

            value = cash_entry.get().strip()

            if value == "":

                change_label.configure(
                    text="Change: ₱0.00",
                    text_color=self.TEAL
                )

                return

            try:

                cash = float(
                    value
                    .replace(",", "")
                    .replace("₱", "")
                )

                if cash < total:

                    change_label.configure(
                        text=(
                            f"Insufficient: "
                            f"₱{total - cash:,.2f} "
                            f"more needed"
                        ),
                        text_color=self.RED
                    )

                else:

                    change = cash - total

                    change_label.configure(
                        text=f"Change: ₱{change:,.2f}",
                        text_color=self.TEAL
                    )

            except ValueError:

                change_label.configure(
                    text="Enter a valid cash amount.",
                    text_color=self.RED
                )

        cash_entry.bind(
            "<KeyRelease>",
            calculate_change
        )

        def confirm_payment():

            value = cash_entry.get().strip()

            try:

                cash = float(
                    value
                    .replace(",", "")
                    .replace("₱", "")
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Cash",
                    "Please enter the amount of cash received.",
                    parent=payment
                )

                cash_entry.focus()

                return

            if cash < total:

                messagebox.showwarning(
                    "Insufficient Cash",
                    f"Customer gave ₱{cash:,.2f}.\n\n"
                    f"Total due is ₱{total:,.2f}.\n"
                    f"Need ₱{total - cash:,.2f} more.",
                    parent=payment
                )

                return

            change = cash - total

            answer = messagebox.askyesno(
                "Confirm Payment",
                f"Total Due: ₱{total:,.2f}\n"
                f"Cash Received: ₱{cash:,.2f}\n"
                f"Change: ₱{change:,.2f}\n\n"
                f"Confirm payment?",
                parent=payment
            )

            if not answer:
                return

            self.record_sale(
                cart_items=cart_items,
                total=total,
                cash=cash,
                change=change
            )

            if clear_cart_after_payment:

                self.cart.clear()

                self.update_cart_total()

                if (
                    self.cart_window is not None
                    and self.cart_window.winfo_exists()
                ):

                    self.cart_window.destroy()

                    self.cart_window = None

            messagebox.showinfo(
                "Payment Successful",
                f"Payment completed successfully!\n\n"
                f"Total: ₱{total:,.2f}\n"
                f"Cash: ₱{cash:,.2f}\n"
                f"Change: ₱{change:,.2f}",
                parent=payment
            )

            payment.destroy()

        ctk.CTkButton(
            payment,
            text="CONFIRM PAYMENT",
            height=42,
            corner_radius=8,
            fg_color=self.DARK_TEAL,
            hover_color=self.TEAL,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=confirm_payment
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 8)
        )

        ctk.CTkButton(
            payment,
            text="Cancel",
            height=38,
            corner_radius=8,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=self.DARK,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=payment.destroy
        ).pack(
            fill="x",
            padx=25
        )

        cash_entry.focus()

    # ==========================================================
    # LOGOUT
    # ==========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if answer:

            self.root.destroy()

            self.parent.deiconify()