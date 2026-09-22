import customtkinter as ctk


class SalesSummary(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        # =========================
        # SAMPLE DATA
        # =========================

        self.total_sales = 0.00
        self.transactions = 0
        self.items_sold = 0

        # =========================
        # TITLE
        # =========================

        self.title_label = ctk.CTkLabel(
            self,
            text="Sales Summary",
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
            text="View your sales statistics"
        )

        self.description_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 25)
        )

        # =========================
        # SUMMARY CARDS
        # =========================

        self.cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.cards_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        # =========================
        # TOTAL SALES CARD
        # =========================

        self.total_card = ctk.CTkFrame(
            self.cards_frame,
            height=130
        )

        self.total_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.total_title = ctk.CTkLabel(
            self.total_card,
            text="Total Sales"
        )

        self.total_title.pack(
            pady=(20, 5)
        )

        self.total_sales_label = ctk.CTkLabel(
            self.total_card,
            text="₱0.00",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.total_sales_label.pack()

        # =========================
        # TRANSACTIONS CARD
        # =========================

        self.transactions_card = ctk.CTkFrame(
            self.cards_frame,
            height=130
        )

        self.transactions_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.transactions_title = ctk.CTkLabel(
            self.transactions_card,
            text="Transactions"
        )

        self.transactions_title.pack(
            pady=(20, 5)
        )

        self.transactions_label = ctk.CTkLabel(
            self.transactions_card,
            text="0",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.transactions_label.pack()

        # =========================
        # ITEMS SOLD CARD
        # =========================

        self.items_card = ctk.CTkFrame(
            self.cards_frame,
            height=130
        )

        self.items_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.items_title = ctk.CTkLabel(
            self.items_card,
            text="Items Sold"
        )

        self.items_title.pack(
            pady=(20, 5)
        )

        self.items_sold_label = ctk.CTkLabel(
            self.items_card,
            text="0",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.items_sold_label.pack()

        # =========================
        # SALES INFORMATION
        # =========================

        self.info_frame = ctk.CTkFrame(
            self
        )

        self.info_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        self.info_title = ctk.CTkLabel(
            self.info_frame,
            text="Sales Overview",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.info_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        self.info_text = ctk.CTkLabel(
            self.info_frame,
            text=(
                "Total revenue generated from sales.\n"
                "Number of completed transactions.\n"
                "Total number of products sold."
            ),
            justify="left"
        )

        self.info_text.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # =========================
        # REFRESH BUTTON
        # =========================

        self.refresh_button = ctk.CTkButton(
            self,
            text="Refresh",
            height=40,
            command=self.refresh
        )

        self.refresh_button.pack(
            padx=30,
            pady=(0, 25),
            fill="x"
        )

    # ==================================================
    # REFRESH
    # ==================================================

    def refresh(self):

        self.total_sales_label.configure(
            text=f"₱{self.total_sales:,.2f}"
        )

        self.transactions_label.configure(
            text=str(self.transactions)
        )

        self.items_sold_label.configure(
            text=str(self.items_sold)
        )