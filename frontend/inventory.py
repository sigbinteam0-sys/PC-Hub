import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os
import shutil


class Inventory(ctk.CTkFrame):

    # ==========================================================
    # COLORS
    # ==========================================================

    BLUE = "#1769D1"
    DARK_BLUE = "#0F4FA8"
    LIGHT_BLUE = "#EAF3FF"

    WHITE = "#FFFFFF"
    BG = "#F4F7FB"

    DARK = "#172033"
    GRAY = "#667085"
    BORDER = "#D6E0ED"

    RED = "#D66D70"
    LIGHT_RED = "#FFF1F1"

    IMAGE_GRAY = "#E8EEF5"

    # ==========================================================
    # INIT
    # ==========================================================

    def __init__(self, parent, products, refresh_callback=None):

        super().__init__(
            parent,
            fg_color=self.BG,
            corner_radius=0
        )

        self.parent = parent
        self.products = products
        self.refresh_callback = refresh_callback

        self.selected_product = None

        # Search
        self.search_text = ""

        # This is a PAGE, not a separate window
        self.pack(
            fill="both",
            expand=True
        )

        self.create_inventory()

    # ==========================================================
    # IMAGE FOLDER
    # ==========================================================

    def get_images_folder(self):

        # inventory.py is inside the frontend folder
        frontend_folder = os.path.dirname(
            os.path.abspath(__file__)
        )

        images_folder = os.path.join(
            frontend_folder,
            "images"
        )

        # Automatically create images folder
        os.makedirs(
            images_folder,
            exist_ok=True
        )

        return images_folder

    # ==========================================================
    # SAVE PRODUCT IMAGE
    # ==========================================================

    def save_product_image(self, source_path, product_name):

        if not source_path:
            return ""

        try:

            images_folder = self.get_images_folder()

            # Get original extension
            extension = os.path.splitext(
                source_path
            )[1].lower()

            # Create safe filename from product name
            safe_name = "".join(
                character
                for character in product_name
                if character.isalnum()
                or character in (" ", "_", "-")
            ).strip()

            safe_name = safe_name.replace(
                " ",
                "_"
            )

            # If product name somehow becomes empty
            if not safe_name:
                safe_name = "product"

            destination = os.path.join(
                images_folder,
                safe_name + extension
            )

            # Prevent overwriting existing image
            counter = 1

            while os.path.exists(destination):

                destination = os.path.join(
                    images_folder,
                    f"{safe_name}_{counter}{extension}"
                )

                counter += 1

            # Copy image into frontend/images
            shutil.copy2(
                source_path,
                destination
            )

            return destination

        except Exception as error:

            messagebox.showerror(
                "Image Error",
                f"Unable to save product picture.\n\n{error}",
                parent=self.winfo_toplevel()
            )

            return ""

    # ==========================================================
    # DELETE PRODUCT IMAGE
    # ==========================================================

    def delete_product_image(self, image_path):

        if not image_path:
            return

        try:

            if os.path.exists(image_path):

                os.remove(
                    image_path
                )

        except Exception:
            pass

    # ==========================================================
    # INVENTORY UI
    # ==========================================================

    def create_inventory(self):

        # ======================================================
        # TITLE + SEARCH BAR
        # ======================================================

        top_frame = ctk.CTkFrame(
            self,
            fg_color=self.WHITE,
            corner_radius=10
        )

        top_frame.pack(
            fill="x",
            padx=10,
            pady=(10, 10)
        )

        # ======================================================
        # PRODUCT TITLE
        # ======================================================

        ctk.CTkLabel(
            top_frame,
            text="Inventory",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            side="left",
            padx=18,
            pady=10
        )

        # ======================================================
        # SEARCH AREA
        # ======================================================

        search_frame = ctk.CTkFrame(
            top_frame,
            fg_color="transparent"
        )

        search_frame.pack(
            side="right",
            padx=10,
            pady=8
        )

        # ======================================================
        # SEARCH BUTTON
        # ======================================================

        ctk.CTkButton(
            search_frame,
            text="🔍  Search",
            width=90,
            height=36,
            corner_radius=8,
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.on_search
        ).pack(
            side="left",
            padx=(0, 10)
        )

        # ======================================================
        # SEARCH ENTRY
        # ======================================================

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=350,
            height=36,
            corner_radius=8,
            placeholder_text="Search products..."
        )

        self.search_entry.pack(
            side="left"
        )

        # Press Enter to search
        self.search_entry.bind(
            "<Return>",
            self.on_search
        )

        # ======================================================
        # TABLE CONTAINER
        # ======================================================

        table_container = ctk.CTkFrame(
            self,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=1,
            border_color=self.BORDER
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = ctk.CTkFrame(
            table_container,
            fg_color=self.BLUE,
            corner_radius=8
        )

        header.pack(
            fill="x",
            padx=8,
            pady=8
        )

        column_weights = [
            3,
            2,
            2,
            1,
            1,
            1
        ]

        for column, weight in enumerate(
            column_weights
        ):

            header.grid_columnconfigure(
                column,
                weight=weight,
                uniform="inventory_columns"
            )

        headers = [
            "Name",
            "Category",
            "Price",
            "Quantity",
            "Delete",
            "Update"
        ]

        for column, text in enumerate(headers):

            ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                text_color=self.WHITE,
                anchor="center"
            ).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=5,
                pady=8
            )

        # ======================================================
        # SCROLLABLE TABLE
        # ======================================================

        self.table = ctk.CTkScrollableFrame(
            table_container,
            fg_color=self.WHITE,
            corner_radius=0
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8)
        )

        for column, weight in enumerate(
            column_weights
        ):

            self.table.grid_columnconfigure(
                column,
                weight=weight,
                uniform="inventory_columns"
            )

        # ======================================================
        # BOTTOM BAR
        # ======================================================

        bottom = ctk.CTkFrame(
            self,
            height=60,
            fg_color=self.BLUE,
            corner_radius=0
        )

        bottom.pack(
            fill="x",
            side="bottom"
        )

        bottom.pack_propagate(False)

        # ======================================================
        # ADD PRODUCT
        # ======================================================

        ctk.CTkButton(
            bottom,
            text="Add Product",
            width=120,
            height=38,
            corner_radius=8,
            fg_color=self.WHITE,
            hover_color=self.LIGHT_BLUE,
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.add_product
        ).pack(
            side="left",
            padx=15,
            pady=10
        )

        # ======================================================
        # LOAD TABLE
        # ======================================================

        self.refresh_table()

    # ==========================================================
    # SEARCH
    # ==========================================================

    def on_search(self, event=None):

        self.search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        self.refresh_table()

    # ==========================================================
    # GET FILTERED PRODUCTS
    # ==========================================================

    def get_filtered_products(self):

        if not self.search_text:
            return self.products

        filtered = []

        for product in self.products:

            name = str(
                product.get(
                    "name",
                    ""
                )
            ).lower()

            category = str(
                product.get(
                    "category",
                    ""
                )
            ).lower()

            if (
                self.search_text in name
                or self.search_text in category
            ):

                filtered.append(
                    product
                )

        return filtered

    # ==========================================================
    # REFRESH TABLE
    # ==========================================================

    def refresh_table(self):

        if not hasattr(
            self,
            "table"
        ):
            return

        for widget in self.table.winfo_children():

            widget.destroy()

        filtered_products = (
            self.get_filtered_products()
        )

        # ======================================================
        # NO PRODUCTS
        # ======================================================

        if not filtered_products:

            if self.search_text:

                text = (
                    f'No products found for '
                    f'"{self.search_text}".'
                )

            else:

                text = "No products in inventory."

            ctk.CTkLabel(
                self.table,
                text=text,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                ),
                text_color=self.GRAY
            ).grid(
                row=0,
                column=0,
                columnspan=6,
                pady=80
            )

            return

        # ======================================================
        # CREATE ROWS
        # ======================================================

        for display_index, product in enumerate(
            filtered_products
        ):

            if "quantity" not in product:

                product["quantity"] = 10

            if "image" not in product:

                product["image"] = ""

            try:

                original_index = (
                    self.products.index(product)
                )

            except ValueError:

                continue

            self.create_product_row(
                display_index,
                original_index,
                product
            )

    # ==========================================================
    # PRODUCT ROW
    # ==========================================================

    def create_product_row(
        self,
        display_index,
        original_index,
        product
    ):

        row = ctk.CTkFrame(
            self.table,
            fg_color=(
                self.WHITE
                if display_index % 2 == 0
                else "#F8FAFC"
            ),
            corner_radius=6
        )

        row.grid(
            row=display_index,
            column=0,
            columnspan=6,
            sticky="ew",
            pady=2
        )

        column_weights = [
            3,
            2,
            2,
            1,
            1,
            1
        ]

        for column, weight in enumerate(
            column_weights
        ):

            row.grid_columnconfigure(
                column,
                weight=weight,
                uniform="inventory_columns"
            )

        # ======================================================
        # NAME
        # ======================================================

        ctk.CTkLabel(
            row,
            text=product.get(
                "name",
                "Unnamed Product"
            ),
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.DARK,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        # ======================================================
        # CATEGORY
        # ======================================================

        ctk.CTkLabel(
            row,
            text=product.get(
                "category",
                "Other"
            ),
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.DARK,
            anchor="center"
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=8
        )

        # ======================================================
        # PRICE
        # ======================================================

        price = product.get(
            "price",
            0
        )

        try:

            price_value = float(
                price
            )

        except (
            ValueError,
            TypeError
        ):

            price_value = 0

        ctk.CTkLabel(
            row,
            text=f"₱{price_value:,.2f}",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.DARK,
            anchor="center"
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5,
            pady=8
        )

        # ======================================================
        # QUANTITY
        # ======================================================

        quantity = product.get(
            "quantity",
            10
        )

        ctk.CTkLabel(
            row,
            text=str(quantity),
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.DARK,
            anchor="center"
        ).grid(
            row=0,
            column=3,
            sticky="ew",
            padx=5,
            pady=8
        )

        # ======================================================
        # DELETE
        # ======================================================

        ctk.CTkButton(
            row,
            text="Delete",
            width=70,
            height=30,
            corner_radius=7,
            fg_color=self.RED,
            hover_color="#B94F53",
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            command=lambda i=original_index:
                self.delete_product(i)
        ).grid(
            row=0,
            column=4,
            padx=8,
            pady=5
        )

        # ======================================================
        # UPDATE
        # ======================================================

        ctk.CTkButton(
            row,
            text="Update",
            width=70,
            height=30,
            corner_radius=7,
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            command=lambda i=original_index:
                self.update_product(i)
        ).grid(
            row=0,
            column=5,
            padx=8,
            pady=5
        )

    # ==========================================================
    # ADD PRODUCT
    # ==========================================================

    def add_product(self):

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Add Product"
        )

        window.geometry(
            "520x760"
        )

        window.resizable(
            False,
            False
        )

        window.configure(
            fg_color=self.BG
        )

        window.transient(
            self.winfo_toplevel()
        )

        window.grab_set()

        # ======================================================
        # TITLE
        # ======================================================

        ctk.CTkLabel(
            window,
            text="ADD PRODUCT",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            pady=(25, 20)
        )

        # ======================================================
        # NAME
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Product Name:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        name_entry = ctk.CTkEntry(
            window,
            height=38
        )

        name_entry.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # CATEGORY
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Category:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        category_menu = ctk.CTkComboBox(
            window,
            height=38,
            values=[
                "CPU",
                "GPU",
                "RAM",
                "Storage",
                "Motherboard",
                "PSU",
                "Other"
            ]
        )

        category_menu.set(
            "CPU"
        )

        category_menu.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # PRICE
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Price:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        price_entry = ctk.CTkEntry(
            window,
            height=38
        )

        price_entry.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # QUANTITY
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Quantity:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        quantity_entry = ctk.CTkEntry(
            window,
            height=38
        )

        quantity_entry.insert(
            0,
            "10"
        )

        quantity_entry.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # PICTURE
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Product Picture:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        picture_frame = ctk.CTkFrame(
            window,
            height=110,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=1,
            border_color=self.BORDER
        )

        picture_frame.pack(
            fill="x",
            padx=32,
            pady=(6, 8)
        )

        picture_frame.pack_propagate(
            False
        )

        picture_label = ctk.CTkLabel(
            picture_frame,
            text="No picture selected",
            width=120,
            height=100,
            fg_color=self.IMAGE_GRAY,
            corner_radius=10,
            text_color=self.GRAY
        )

        picture_label.pack(
            expand=True
        )

        selected_picture = {
            "path": ""
        }

        # ======================================================
        # BROWSE PICTURE
        # ======================================================

        def browse_picture():

            path = filedialog.askopenfilename(
                parent=window,
                title="Select Product Picture",
                filetypes=[
                    (
                        "Image Files",
                        "*.png *.jpg *.jpeg *.webp"
                    )
                ]
            )

            if not path:
                return

            selected_picture["path"] = path

            try:

                image = Image.open(
                    path
                )

                image.thumbnail(
                    (120, 100)
                )

                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=image.size
                )

                picture_label.configure(
                    image=ctk_image,
                    text=""
                )

                picture_label.image = ctk_image

            except Exception as error:

                messagebox.showerror(
                    "Image Error",
                    f"Unable to load image.\n\n{error}",
                    parent=window
                )

        ctk.CTkButton(
            window,
            text="Browse Picture",
            width=150,
            height=36,
            corner_radius=8,
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            command=browse_picture
        ).pack(
            pady=(0, 18)
        )

        # ======================================================
        # BUTTON FRAME
        # ======================================================

        button_frame = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=32,
            pady=(0, 20)
        )

        # ======================================================
        # SAVE PRODUCT
        # ======================================================

        def save_product():

            name = name_entry.get().strip()
            category = category_menu.get().strip()
            price_text = price_entry.get().strip()
            quantity_text = quantity_entry.get().strip()

            if not name:

                messagebox.showwarning(
                    "Missing Product",
                    "Please enter the product name.",
                    parent=window
                )

                return

            try:

                price = float(
                    price_text
                    .replace(",", "")
                    .replace("₱", "")
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Price",
                    "Please enter a valid price.",
                    parent=window
                )

                return

            try:

                quantity = int(
                    quantity_text
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Quantity",
                    "Quantity must be a whole number.",
                    parent=window
                )

                return

            if price < 0 or quantity < 0:

                messagebox.showwarning(
                    "Invalid Value",
                    "Price and quantity cannot be negative.",
                    parent=window
                )

                return

            # ==================================================
            # SAVE IMAGE INTO frontend/images
            # ==================================================

            saved_image = self.save_product_image(
                selected_picture["path"],
                name
            )

            # ==================================================
            # CREATE PRODUCT
            # ==================================================

            new_product = {
                "name": name,
                "category": category,
                "description": "Computer Part",
                "price": price,
                "quantity": quantity,
                "image": saved_image
            }

            self.products.append(
                new_product
            )

            self.refresh_table()

            # Refresh Dashboard

            if self.refresh_callback:

                try:

                    self.refresh_callback()

                except Exception:

                    pass

            messagebox.showinfo(
                "Product Added",
                f"{name} has been added successfully.",
                parent=window
            )

            window.destroy()

        # ======================================================
        # ADD PRODUCT BUTTON
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="Add Product",
            height=40,
            corner_radius=8,
            fg_color=self.DARK_BLUE,
            hover_color=self.BLUE,
            command=save_product
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        # ======================================================
        # CANCEL BUTTON
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=40,
            corner_radius=8,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=self.DARK,
            command=window.destroy
        ).pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        name_entry.focus()

    # ==========================================================
    # UPDATE PRODUCT
    # ==========================================================

    def update_product(self, index):

        if index < 0 or index >= len(self.products):
            return

        product = self.products[index]

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Update Product"
        )

        window.geometry(
            "520x760"
        )

        window.resizable(
            False,
            False
        )

        window.configure(
            fg_color=self.BG
        )

        window.transient(
            self.winfo_toplevel()
        )

        window.grab_set()

        # ======================================================
        # TITLE
        # ======================================================

        ctk.CTkLabel(
            window,
            text="UPDATE PRODUCT",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            pady=(25, 20)
        )

        # ======================================================
        # NAME
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Product Name:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        name_entry = ctk.CTkEntry(
            window,
            height=38
        )

        name_entry.insert(
            0,
            product.get(
                "name",
                ""
            )
        )

        name_entry.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # CATEGORY
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Category:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        category_menu = ctk.CTkComboBox(
            window,
            height=38,
            values=[
                "CPU",
                "GPU",
                "RAM",
                "Storage",
                "Motherboard",
                "PSU",
                "Other"
            ]
        )

        category_menu.set(
            product.get(
                "category",
                "Other"
            )
        )

        category_menu.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # PRICE
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Price:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        price_entry = ctk.CTkEntry(
            window,
            height=38
        )

        price_entry.insert(
            0,
            str(
                product.get(
                    "price",
                    0
                )
            )
        )

        price_entry.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # QUANTITY
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Quantity:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        quantity_entry = ctk.CTkEntry(
            window,
            height=38
        )

        quantity_entry.insert(
            0,
            str(
                product.get(
                    "quantity",
                    10
                )
            )
        )

        quantity_entry.pack(
            fill="x",
            padx=32,
            pady=(6, 16)
        )

        # ======================================================
        # PICTURE
        # ======================================================

        ctk.CTkLabel(
            window,
            text="Product Picture:",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=32
        )

        picture_frame = ctk.CTkFrame(
            window,
            height=110,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=1,
            border_color=self.BORDER
        )

        picture_frame.pack(
            fill="x",
            padx=32,
            pady=(6, 8)
        )

        picture_frame.pack_propagate(
            False
        )

        picture_label = ctk.CTkLabel(
            picture_frame,
            text="No picture selected",
            width=120,
            height=100,
            fg_color=self.IMAGE_GRAY,
            corner_radius=10,
            text_color=self.GRAY
        )

        picture_label.pack(
            expand=True
        )

        selected_picture = {
            "path": product.get(
                "image",
                ""
            )
        }

        # ======================================================
        # SHOW EXISTING PICTURE
        # ======================================================

        existing_image = selected_picture["path"]

        if (
            existing_image
            and os.path.exists(existing_image)
        ):

            try:

                image = Image.open(
                    existing_image
                )

                image.thumbnail(
                    (120, 100)
                )

                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=image.size
                )

                picture_label.configure(
                    image=ctk_image,
                    text=""
                )

                picture_label.image = ctk_image

            except Exception:

                pass

        # ======================================================
        # BROWSE PICTURE
        # ======================================================

        def browse_picture():

            path = filedialog.askopenfilename(
                parent=window,
                title="Select Product Picture",
                filetypes=[
                    (
                        "Image Files",
                        "*.png *.jpg *.jpeg *.webp"
                    )
                ]
            )

            if not path:
                return

            selected_picture["path"] = path

            try:

                image = Image.open(
                    path
                )

                image.thumbnail(
                    (120, 100)
                )

                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=image.size
                )

                picture_label.configure(
                    image=ctk_image,
                    text=""
                )

                picture_label.image = ctk_image

            except Exception as error:

                messagebox.showerror(
                    "Image Error",
                    f"Unable to load image.\n\n{error}",
                    parent=window
                )

        ctk.CTkButton(
            window,
            text="Browse Picture",
            width=150,
            height=36,
            corner_radius=8,
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            command=browse_picture
        ).pack(
            pady=(0, 18)
        )

        # ======================================================
        # BUTTON FRAME
        # ======================================================

        button_frame = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=32,
            pady=(0, 20)
        )

        # ======================================================
        # SAVE UPDATE
        # ======================================================

        def save_update():

            name = name_entry.get().strip()
            category = category_menu.get().strip()
            price_text = price_entry.get().strip()
            quantity_text = quantity_entry.get().strip()

            if not name:

                messagebox.showwarning(
                    "Missing Product",
                    "Please enter the product name.",
                    parent=window
                )

                return

            try:

                price = float(
                    price_text
                    .replace(",", "")
                    .replace("₱", "")
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Price",
                    "Please enter a valid price.",
                    parent=window
                )

                return

            try:

                quantity = int(
                    quantity_text
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Quantity",
                    "Quantity must be a whole number.",
                    parent=window
                )

                return

            if price < 0 or quantity < 0:

                messagebox.showwarning(
                    "Invalid Value",
                    "Price and quantity cannot be negative.",
                    parent=window
                )

                return

            # ==================================================
            # HANDLE IMAGE UPDATE
            # ==================================================

            old_image = product.get(
                "image",
                ""
            )

            selected_image = selected_picture["path"]

            # If user selected a new picture
            if (
                selected_image
                and selected_image != old_image
            ):

                saved_image = self.save_product_image(
                    selected_image,
                    name
                )

                if saved_image:

                    # Delete old copied image
                    if (
                        old_image
                        and old_image != saved_image
                        and os.path.exists(old_image)
                    ):

                        try:

                            os.remove(
                                old_image
                            )

                        except Exception:

                            pass

                    selected_image = saved_image

                else:

                    # Keep old image if copying failed
                    selected_image = old_image

            # ==================================================
            # UPDATE PRODUCT
            # ==================================================

            product["name"] = name
            product["category"] = category
            product["price"] = price
            product["quantity"] = quantity
            product["image"] = selected_image

            self.refresh_table()

            # Refresh Dashboard

            if self.refresh_callback:

                try:

                    self.refresh_callback()

                except Exception:

                    pass

            messagebox.showinfo(
                "Product Updated",
                f"{name} has been updated successfully.",
                parent=window
            )

            window.destroy()

        # ======================================================
        # UPDATE BUTTON
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="Update Product",
            height=40,
            corner_radius=8,
            fg_color=self.DARK_BLUE,
            hover_color=self.BLUE,
            command=save_update
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        # ======================================================
        # CANCEL BUTTON
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=40,
            corner_radius=8,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=self.DARK,
            command=window.destroy
        ).pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        name_entry.focus()

    # ==========================================================
    # DELETE PRODUCT
    # ==========================================================

    def delete_product(self, index):

        if index < 0 or index >= len(self.products):
            return

        product = self.products[index]

        answer = messagebox.askyesno(
            "Delete Product",
            f"Are you sure you want to delete\n\n"
            f"{product.get('name', 'this product')}?",
            parent=self.winfo_toplevel()
        )

        if not answer:
            return

        # ======================================================
        # DELETE IMAGE FILE
        # ======================================================

        image_path = product.get(
            "image",
            ""
        )

        if image_path:

            try:

                if os.path.exists(image_path):

                    os.remove(
                        image_path
                    )

            except Exception:

                pass

        # ======================================================
        # DELETE PRODUCT
        # ======================================================

        self.products.pop(
            index
        )

        self.refresh_table()

        # Refresh Dashboard

        if self.refresh_callback:

            try:

                self.refresh_callback()

            except Exception:

                pass

    # ==========================================================
    # DELETE SELECTED
    # ==========================================================

    def delete_selected(self):

        messagebox.showinfo(
            "Delete Product",
            "Please use the Delete button beside the "
            "product you want to remove.",
            parent=self.winfo_toplevel()
        )