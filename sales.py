import customtkinter as ctk


class Sales(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        # =========================
        # SAMPLE SALES DATA
        # =========================

        self.sales = [
            {
                "id": "SALE-001",
                "date": "2026-09-22",
                "items": "Keyboard, Mouse",
                "total": 850.00
            },
            {
                "id": "SALE-002",
                "date": "2026-09-22",
                "items": "Monitor",
                "total": 5500.00
            },
            {
                "id": "SALE-003",
                "date": "2026-09-21",
                "items": "RAM, Mouse",
                "total": 2350.00
            },
            {
                "id": "SALE-004",
                "date": "2026-09-20",
                "items": "Keyboard",
                "total": 500.00
            }
        ]

        self.selected_sale = None

        # =========================
        # TITLE
        # =========================

        self.title_label = ctk.CTkLabel(
            self,
            text="Sales History",
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
            text="View previous sales transactions"
        )

        self.description_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        # =========================
        # SEARCH AREA
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
            height=40,
            placeholder_text="Search Sale ID"
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
            height=40,
            command=self.search_sales
        )

        self.search_button.pack(
            side="right"
        )

        # =========================
        # SALES LIST
        # =========================

        self.sales_list = ctk.CTkScrollableFrame(
            self
        )

        self.sales_list.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        # =========================
        # BUTTON AREA
        # =========================

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        self.view_button = ctk.CTkButton(
            self.button_frame,
            text="View Details",
            height=40,
            command=self.view_details
        )

        self.view_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.refresh_button = ctk.CTkButton(
            self.button_frame,
            text="Refresh",
            height=40,
            command=self.refresh_sales
        )

        self.refresh_button.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        # =========================
        # DISPLAY SALES
        # =========================

        self.display_sales()

    # ==================================================
    # DISPLAY SALES
    # ==================================================

    def display_sales(self, sales=None):

        for widget in self.sales_list.winfo_children():
            widget.destroy()

        if sales is None:
            sales = self.sales

        if not sales:

            empty_label = ctk.CTkLabel(
                self.sales_list,
                text="No sales found."
            )

            empty_label.pack(
                pady=30
            )

            return

        for sale in sales:

            row = ctk.CTkFrame(
                self.sales_list
            )

            row.pack(
                fill="x",
                pady=4
            )

            # =========================
            # SALE INFORMATION
            # =========================

            info_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            info_frame.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=10
            )

            sale_id_label = ctk.CTkLabel(
                info_frame,
                text=sale["id"],
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            )

            sale_id_label.pack(
                anchor="w"
            )

            details_label = ctk.CTkLabel(
                info_frame,
                text=(
                    f"Date: {sale['date']}    "
                    f"Items: {sale['items']}"
                )
            )

            details_label.pack(
                anchor="w",
                pady=(3, 0)
            )

            # =========================
            # TOTAL
            # =========================

            total_label = ctk.CTkLabel(
                row,
                text=f"₱{sale['total']:,.2f}",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            )

            total_label.pack(
                side="right",
                padx=15
            )

            # =========================
            # SELECT BUTTON
            # =========================

            select_button = ctk.CTkButton(
                row,
                text="Select",
                width=80,
                command=lambda s=sale:
                    self.select_sale(s)
            )

            select_button.pack(
                side="right",
                padx=5
            )

    # ==================================================
    # SELECT SALE
    # ==================================================

    def select_sale(self, sale):

        self.selected_sale = sale

        print(
            f"Selected: {sale['id']}"
        )

    # ==================================================
    # SEARCH SALES
    # ==================================================

    def search_sales(self):

        search = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if not search:

            self.display_sales()

            return

        results = []

        for sale in self.sales:

            if search in sale["id"].lower():

                results.append(sale)

        self.display_sales(
            results
        )

    # ==================================================
    # VIEW DETAILS
    # ==================================================

    def view_details(self):

        if self.selected_sale is None:

            print(
                "Please select a sale first."
            )

            return

        sale = self.selected_sale

        details_window = ctk.CTkToplevel(
            self
        )

        details_window.title(
            f"Sale Details - {sale['id']}"
        )

        details_window.geometry(
            "450x400"
        )

        details_window.resizable(
            False,
            False
        )

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            details_window,
            text="Sale Details",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.pack(
            pady=(25, 20)
        )

        # =========================
        # SALE ID
        # =========================

        sale_id = ctk.CTkLabel(
            details_window,
            text=f"Sale ID: {sale['id']}"
        )

        sale_id.pack(
            anchor="w",
            padx=30,
            pady=5
        )

        # =========================
        # DATE
        # =========================

        date = ctk.CTkLabel(
            details_window,
            text=f"Date: {sale['date']}"
        )

        date.pack(
            anchor="w",
            padx=30,
            pady=5
        )

        # =========================
        # ITEMS
        # =========================

        items = ctk.CTkLabel(
            details_window,
            text=f"Items: {sale['items']}"
        )

        items.pack(
            anchor="w",
            padx=30,
            pady=5
        )

        # =========================
        # TOTAL
        # =========================

        total = ctk.CTkLabel(
            details_window,
            text=f"Total: ₱{sale['total']:,.2f}",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        total.pack(
            anchor="w",
            padx=30,
            pady=15
        )

        # =========================
        # CLOSE
        # =========================

        close_button = ctk.CTkButton(
            details_window,
            text="Close",
            command=details_window.destroy
        )

        close_button.pack(
            padx=30,
            pady=20,
            fill="x"
        )

    # ==================================================
    # REFRESH
    # ==================================================

    def refresh_sales(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.selected_sale = None

        self.display_sales()