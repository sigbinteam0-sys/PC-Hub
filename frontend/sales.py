import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class Sales(ctk.CTkFrame):

    # ==========================================================
    # COLORS - PC HUB DESIGN
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

    # ==========================================================
    # INIT
    # ==========================================================

    def __init__(self, parent, sales_data=None):

        super().__init__(
            parent,
            fg_color=self.BG,
            corner_radius=0
        )

        self.parent = parent

        # If your dashboard already has sales data,
        # it can be passed here.
        self.sales_data = sales_data if sales_data is not None else []

        self.create_sales()

    # ==========================================================
    # SALES UI
    # ==========================================================

    def create_sales(self):

        # ======================================================
        # MAIN CONTAINER
        # ======================================================

        main = ctk.CTkFrame(
            self,
            fg_color=self.BG,
            corner_radius=0
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ======================================================
        # PAGE TITLE
        # ======================================================

        title_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        title_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            title_frame,
            text="Sales",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            side="left"
        )

        # ======================================================
        # MAIN SALES PANEL
        # ======================================================

        sales_panel = ctk.CTkFrame(
            main,
            fg_color=self.WHITE,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )

        sales_panel.pack(
            fill="both",
            expand=True
        )

        # ======================================================
        # SALES PANEL HEADER
        # ======================================================

        panel_header = ctk.CTkFrame(
            sales_panel,
            fg_color=self.BLUE,
            height=55,
            corner_radius=10
        )

        panel_header.pack(
            fill="x",
            padx=8,
            pady=8
        )

        panel_header.pack_propagate(False)

        ctk.CTkLabel(
            panel_header,
            text="Sales Overview",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=self.WHITE
        ).pack(
            side="left",
            padx=20
        )

        # ======================================================
        # TWO SALES SECTIONS
        # ======================================================

        sections = ctk.CTkFrame(
            sales_panel,
            fg_color="transparent"
        )

        sections.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        sections.grid_columnconfigure(
            0,
            weight=1
        )

        sections.grid_columnconfigure(
            1,
            weight=1
        )

        sections.grid_rowconfigure(
            0,
            weight=1
        )

        # ======================================================
        # SALES FOR THIS DAY
        # ======================================================

        today_frame = ctk.CTkFrame(
            sections,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=2,
            border_color=self.BLUE
        )

        today_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        ctk.CTkLabel(
            today_frame,
            text="Sales for this day",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        # ------------------------------------------------------
        # TODAY TOTAL
        # ------------------------------------------------------

        today_total = self.get_today_total()

        self.today_total_label = ctk.CTkLabel(
            today_frame,
            text=f"₱{today_total:,.2f}",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=self.BLUE
        )

        self.today_total_label.pack(
            anchor="w",
            padx=25
        )

        ctk.CTkLabel(
            today_frame,
            text="Total sales today",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.GRAY
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # TODAY TRANSACTIONS
        # ------------------------------------------------------

        today_transactions = self.get_today_transactions()

        self.today_transactions_label = ctk.CTkLabel(
            today_frame,
            text=f"Transactions: {today_transactions}",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=self.DARK
        )

        self.today_transactions_label.pack(
            anchor="w",
            padx=25
        )

        # ======================================================
        # SALES FOR THIS MONTH
        # ======================================================

        month_frame = ctk.CTkFrame(
            sections,
            fg_color=self.WHITE,
            corner_radius=10,
            border_width=2,
            border_color=self.BLUE
        )

        month_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        ctk.CTkLabel(
            month_frame,
            text="Sales for this Month",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=self.DARK
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        # ------------------------------------------------------
        # MONTH TOTAL
        # ------------------------------------------------------

        month_total = self.get_month_total()

        self.month_total_label = ctk.CTkLabel(
            month_frame,
            text=f"₱{month_total:,.2f}",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=self.BLUE
        )

        self.month_total_label.pack(
            anchor="w",
            padx=25
        )

        ctk.CTkLabel(
            month_frame,
            text="Total sales this month",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.GRAY
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # MONTH TRANSACTIONS
        # ------------------------------------------------------

        month_transactions = self.get_month_transactions()

        self.month_transactions_label = ctk.CTkLabel(
            month_frame,
            text=f"Transactions: {month_transactions}",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=self.DARK
        )

        self.month_transactions_label.pack(
            anchor="w",
            padx=25
        )

        # ======================================================
        # REFRESH BUTTON
        # ======================================================

        refresh_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        refresh_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        ctk.CTkButton(
            refresh_frame,
            text="Refresh",
            width=110,
            height=36,
            corner_radius=8,
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.refresh_sales
        ).pack(
            side="right"
        )

    # ==========================================================
    # GET TODAY TOTAL
    # ==========================================================

    def get_today_total(self):

        today = datetime.now().date()

        total = 0

        for sale in self.sales_data:

            sale_date = sale.get("date")

            if isinstance(sale_date, datetime):
                sale_date = sale_date.date()

            if sale_date == today:

                try:
                    total += float(
                        sale.get(
                            "total",
                            0
                        )
                    )

                except (
                    ValueError,
                    TypeError
                ):
                    pass

        return total

    # ==========================================================
    # GET MONTH TOTAL
    # ==========================================================

    def get_month_total(self):

        current_date = datetime.now()

        total = 0

        for sale in self.sales_data:

            sale_date = sale.get("date")

            if isinstance(
                sale_date,
                datetime
            ):

                if (
                    sale_date.year
                    == current_date.year
                    and
                    sale_date.month
                    == current_date.month
                ):

                    try:

                        total += float(
                            sale.get(
                                "total",
                                0
                            )
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        pass

        return total

    # ==========================================================
    # TODAY TRANSACTIONS
    # ==========================================================

    def get_today_transactions(self):

        today = datetime.now().date()

        count = 0

        for sale in self.sales_data:

            sale_date = sale.get("date")

            if isinstance(
                sale_date,
                datetime
            ):

                sale_date = sale_date.date()

            if sale_date == today:

                count += 1

        return count

    # ==========================================================
    # MONTH TRANSACTIONS
    # ==========================================================

    def get_month_transactions(self):

        current_date = datetime.now()

        count = 0

        for sale in self.sales_data:

            sale_date = sale.get("date")

            if isinstance(
                sale_date,
                datetime
            ):

                if (
                    sale_date.year
                    == current_date.year
                    and
                    sale_date.month
                    == current_date.month
                ):

                    count += 1

        return count

    # ==========================================================
    # REFRESH SALES
    # ==========================================================

    def refresh_sales(self):

        today_total = self.get_today_total()
        month_total = self.get_month_total()

        today_transactions = (
            self.get_today_transactions()
        )

        month_transactions = (
            self.get_month_transactions()
        )

        self.today_total_label.configure(
            text=f"₱{today_total:,.2f}"
        )

        self.month_total_label.configure(
            text=f"₱{month_total:,.2f}"
        )

        self.today_transactions_label.configure(
            text=f"Transactions: {today_transactions}"
        )

        self.month_transactions_label.configure(
            text=f"Transactions: {month_transactions}"
        )