import customtkinter as ctk


class POS(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        # =========================
        # PRODUCT DATA
        # =========================

        self.products = {
            "Keyboard": 500.00,
            "Mouse": 350.00,
            "Monitor": 5500.00,
            "Video Card": 15000.00,
            "RAM": 2000.00
        }

        self.cart = []

        self.selected_product = None

        # =========================
        # TITLE
        # =========================

        self.title_label = ctk.CTkLabel(
            self,
            text="Point of Sale",
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
            text="Create a new sale"
        )

        self.description_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        # =========================
        # MAIN AREA
        # =========================

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        # =========================
        # LEFT SIDE - PRODUCTS
        # =========================

        self.product_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.product_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.product_title = ctk.CTkLabel(
            self.product_frame,
            text="Products",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.product_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # =========================
        # SEARCH
        # =========================

        self.search_frame = ctk.CTkFrame(
            self.product_frame,
            fg_color="transparent"
        )

        self.search_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
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
            padx=(0, 5)
        )

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=90,
            height=38,
            command=self.search_products
        )

        self.search_button.pack(
            side="right"
        )

        # =========================
        # PRODUCT LIST
        # =========================

        self.product_list = ctk.CTkScrollableFrame(
            self.product_frame
        )

        self.product_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # =========================
        # QUANTITY
        # =========================

        self.quantity_label = ctk.CTkLabel(
            self.product_frame,
            text="Quantity:"
        )

        self.quantity_label.pack(
            anchor="w",
            padx=15
        )

        self.quantity_entry = ctk.CTkEntry(
            self.product_frame,
            height=38,
            placeholder_text="Enter quantity"
        )

        self.quantity_entry.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        self.add_button = ctk.CTkButton(
            self.product_frame,
            text="Add to Cart",
            height=40,
            command=self.add_to_cart
        )

        self.add_button.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        # =========================
        # RIGHT SIDE - CART
        # =========================

        self.cart_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.cart_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.cart_title = ctk.CTkLabel(
            self.cart_frame,
            text="Cart",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.cart_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # =========================
        # CART LIST
        # =========================

        self.cart_list = ctk.CTkScrollableFrame(
            self.cart_frame
        )

        self.cart_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        # =========================
        # TOTAL
        # =========================

        self.total_label = ctk.CTkLabel(
            self.cart_frame,
            text="Total: ₱0.00",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.total_label.pack(
            anchor="e",
            padx=15,
            pady=10
        )

        # =========================
        # PAYMENT
        # =========================

        self.payment_entry = ctk.CTkEntry(
            self.cart_frame,
            height=38,
            placeholder_text="Payment Amount"
        )

        self.payment_entry.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # =========================
        # CHANGE
        # =========================

        self.change_label = ctk.CTkLabel(
            self.cart_frame,
            text="Change: ₱0.00"
        )

        self.change_label.pack(
            anchor="e",
            padx=15,
            pady=5
        )

        # =========================
        # CHECKOUT
        # =========================

        self.checkout_button = ctk.CTkButton(
            self.cart_frame,
            text="Checkout",
            height=40,
            command=self.checkout
        )

        self.checkout_button.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # =========================
        # CLEAR CART
        # =========================

        self.clear_button = ctk.CTkButton(
            self.cart_frame,
            text="Clear Cart",
            height=40,
            command=self.clear_cart
        )

        self.clear_button.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        # =========================
        # DISPLAY PRODUCTS
        # =========================

        self.display_products()

    # ==================================================
    # DISPLAY PRODUCTS
    # ==================================================

    def display_products(self, products=None):

        for widget in self.product_list.winfo_children():
            widget.destroy()

        if products is None:
            products = self.products

        if not products:

            label = ctk.CTkLabel(
                self.product_list,
                text="No products found."
            )

            label.pack(
                pady=20
            )

            return

        for product, price in products.items():

            row = ctk.CTkFrame(
                self.product_list
            )

            row.pack(
                fill="x",
                pady=3
            )

            product_button = ctk.CTkButton(
                row,
                text=f"{product}     ₱{price:,.2f}",
                anchor="w",
                command=lambda p=product:
                    self.select_product(p)
            )

            product_button.pack(
                fill="x",
                padx=5,
                pady=5
            )

    # ==================================================
    # SELECT PRODUCT
    # ==================================================

    def select_product(self, product):

        self.selected_product = product

        self.quantity_entry.delete(
            0,
            "end"
        )

        self.quantity_entry.insert(
            0,
            "1"
        )

    # ==================================================
    # SEARCH PRODUCTS
    # ==================================================

    def search_products(self):

        search = self.search_entry.get().strip().lower()

        if not search:

            self.display_products()

            return

        results = {
            product: price
            for product, price in self.products.items()
            if search in product.lower()
        }

        self.display_products(
            results
        )

    # ==================================================
    # ADD TO CART
    # ==================================================

    def add_to_cart(self):

        if self.selected_product is None:

            print("Please select a product.")

            return

        try:

            quantity = int(
                self.quantity_entry.get()
            )

        except ValueError:

            print(
                "Please enter a valid quantity."
            )

            return

        if quantity <= 0:

            print(
                "Quantity must be greater than 0."
            )

            return

        price = self.products[
            self.selected_product
        ]

        # Check if product already exists
        # in cart

        for item in self.cart:

            if item["product"] == self.selected_product:

                item["quantity"] += quantity

                self.display_cart()

                return

        # Add new item

        self.cart.append({
            "product": self.selected_product,
            "price": price,
            "quantity": quantity
        })

        self.display_cart()

    # ==================================================
    # DISPLAY CART
    # ==================================================

    def display_cart(self):

        for widget in self.cart_list.winfo_children():
            widget.destroy()

        if not self.cart:

            label = ctk.CTkLabel(
                self.cart_list,
                text="Cart is empty."
            )

            label.pack(
                pady=20
            )

            self.total_label.configure(
                text="Total: ₱0.00"
            )

            return

        total = 0

        for index, item in enumerate(self.cart):

            product = item["product"]
            price = item["price"]
            quantity = item["quantity"]

            subtotal = price * quantity

            total += subtotal

            row = ctk.CTkFrame(
                self.cart_list
            )

            row.pack(
                fill="x",
                pady=3
            )

            text = (
                f"{product}\n"
                f"₱{price:,.2f} x {quantity} = "
                f"₱{subtotal:,.2f}"
            )

            label = ctk.CTkLabel(
                row,
                text=text,
                anchor="w"
            )

            label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=8
            )

            remove_button = ctk.CTkButton(
                row,
                text="Remove",
                width=80,
                command=lambda i=index:
                    self.remove_from_cart(i)
            )

            remove_button.pack(
                side="right",
                padx=10,
                pady=5
            )

        self.total_label.configure(
            text=f"Total: ₱{total:,.2f}"
        )

    # ==================================================
    # REMOVE FROM CART
    # ==================================================

    def remove_from_cart(self, index):

        if index < 0 or index >= len(self.cart):
            return

        self.cart.pop(index)

        self.display_cart()

    # ==================================================
    # CLEAR CART
    # ==================================================

    def clear_cart(self):

        self.cart.clear()

        self.payment_entry.delete(
            0,
            "end"
        )

        self.change_label.configure(
            text="Change: ₱0.00"
        )

        self.display_cart()

    # ==================================================
    # GET TOTAL
    # ==================================================

    def get_total(self):

        total = 0

        for item in self.cart:

            total += (
                item["price"] *
                item["quantity"]
            )

        return total

    # ==================================================
    # CHECKOUT
    # ==================================================

    def checkout(self):

        if not self.cart:

            print("Cart is empty.")

            return

        try:

            payment = float(
                self.payment_entry.get()
            )

        except ValueError:

            print(
                "Please enter a valid payment amount."
            )

            return

        total = self.get_total()

        if payment < total:

            print(
                f"Insufficient payment. "
                f"Total is ₱{total:,.2f}"
            )

            return

        change = payment - total

        self.change_label.configure(
            text=f"Change: ₱{change:,.2f}"
        )

        print("Sale completed.")

        print(
            f"Total: ₱{total:,.2f}"
        )

        print(
            f"Payment: ₱{payment:,.2f}"
        )

        print(
            f"Change: ₱{change:,.2f}"
        )

        # Clear cart after successful checkout

        self.cart.clear()

        self.payment_entry.delete(
            0,
            "end"
        )

        self.display_cart()