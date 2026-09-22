import customtkinter as ctk


class Products(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        # =========================
        # PRODUCT DATA
        # =========================

        self.products = [
            "Keyboard",
            "Mouse",
            "Monitor",
            "Video Card",
            "RAM"
        ]

        self.archived_products = []

        # =========================
        # TITLE
        # =========================

        self.title_label = ctk.CTkLabel(
            self,
            text="Products",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        self.title_label.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        self.description_label = ctk.CTkLabel(
            self,
            text="Product Management"
        )

        self.description_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        # =========================
        # SEARCH
        # =========================

        self.search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.search_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search product",
            height=38
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            height=38,
            command=self.search_product
        )

        self.search_button.pack(
            side="right"
        )

        # =========================
        # PRODUCT LIST
        # =========================

        self.product_list = ctk.CTkScrollableFrame(
            self,
            label_text="Products"
        )

        self.product_list.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        # =========================
        # ACTION BUTTONS
        # =========================

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 30)
        )

        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add Product",
            command=self.add_product
        )

        self.add_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        self.edit_button = ctk.CTkButton(
            self.button_frame,
            text="Edit Product",
            command=self.edit_product
        )

        self.edit_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.archive_button = ctk.CTkButton(
            self.button_frame,
            text="Archive",
            command=self.archive_product
        )

        self.archive_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.archived_button = ctk.CTkButton(
            self.button_frame,
            text="Archived",
            command=self.show_archived
        )

        self.archived_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0)
        )

        # =========================
        # DISPLAY
        # =========================

        self.display_products()

    # ==================================================
    # CLEAR LIST
    # ==================================================

    def clear_list(self):
        for widget in self.product_list.winfo_children():
            widget.destroy()

    # ==================================================
    # DISPLAY ACTIVE PRODUCTS
    # ==================================================

    def display_products(self, products=None):

        self.clear_list()

        if products is None:
            products = self.products

        if not products:

            empty_label = ctk.CTkLabel(
                self.product_list,
                text="No products found."
            )

            empty_label.pack(
                pady=20
            )

            return

        for product in products:

            row = ctk.CTkFrame(
                self.product_list
            )

            row.pack(
                fill="x",
                pady=3
            )

            product_label = ctk.CTkLabel(
                row,
                text=product,
                anchor="w"
            )

            product_label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=8
            )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_product(self):

        search = self.search_entry.get().strip().lower()

        if not search:
            self.display_products()
            return

        results = [
            product
            for product in self.products
            if search in product.lower()
        ]

        self.display_products(results)

    # ==================================================
    # ADD PRODUCT
    # ==================================================

    def add_product(self):

        dialog = ctk.CTkInputDialog(
            text="Enter product name:",
            title="Add Product"
        )

        product = dialog.get_input()

        if not product:
            return

        product = product.strip()

        if not product:
            return

        if product in self.products:

            print("Product already exists.")
            return

        if product in self.archived_products:

            print(
                "Product is archived. "
                "Restore it instead."
            )

            return

        self.products.append(product)

        self.display_products()

        print(
            f"{product} added successfully."
        )

    # ==================================================
    # EDIT PRODUCT
    # ==================================================

    def edit_product(self):

        dialog = ctk.CTkInputDialog(
            text="Enter current product name:",
            title="Edit Product"
        )

        old_product = dialog.get_input()

        if not old_product:
            return

        old_product = old_product.strip()

        if old_product not in self.products:

            print("Product not found.")
            return

        dialog = ctk.CTkInputDialog(
            text="Enter new product name:",
            title="Edit Product"
        )

        new_product = dialog.get_input()

        if not new_product:
            return

        new_product = new_product.strip()

        if not new_product:
            return

        if new_product in self.products:

            print("Product name already exists.")
            return

        index = self.products.index(
            old_product
        )

        self.products[index] = new_product

        self.display_products()

        print(
            f"{old_product} changed to "
            f"{new_product}."
        )

    # ==================================================
    # ARCHIVE PRODUCT
    # ==================================================

    def archive_product(self):

        dialog = ctk.CTkInputDialog(
            text="Enter product name to archive:",
            title="Archive Product"
        )

        product = dialog.get_input()

        if not product:
            return

        product = product.strip()

        if product not in self.products:

            print("Product not found.")
            return

        confirm = ctk.CTkInputDialog(
            text=f"Type YES to archive {product}:",
            title="Confirm Archive"
        )

        answer = confirm.get_input()

        if not answer:
            return

        if answer.strip().upper() != "YES":

            print("Archive cancelled.")
            return

        self.products.remove(product)

        self.archived_products.append(product)

        self.display_products()

        print(
            f"{product} has been archived."
        )

    # ==================================================
    # SHOW ARCHIVED
    # ==================================================

    def show_archived(self):

        self.clear_list()

        if not self.archived_products:

            empty_label = ctk.CTkLabel(
                self.product_list,
                text="No archived products."
            )

            empty_label.pack(
                pady=20
            )

            return

        for product in self.archived_products:

            row = ctk.CTkFrame(
                self.product_list
            )

            row.pack(
                fill="x",
                pady=3
            )

            product_label = ctk.CTkLabel(
                row,
                text=product,
                anchor="w"
            )

            product_label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=8
            )

            restore_button = ctk.CTkButton(
                row,
                text="Restore",
                width=100,
                command=lambda p=product: self.restore_product(p)
            )

            restore_button.pack(
                side="right",
                padx=10,
                pady=5
            )

    # ==================================================
    # RESTORE PRODUCT
    # ==================================================

    def restore_product(self, product):

        if product not in self.archived_products:
            return

        self.archived_products.remove(product)

        self.products.append(product)

        self.display_products()

        print(
            f"{product} has been restored."
        )