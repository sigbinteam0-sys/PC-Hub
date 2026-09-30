"""Sales management and analytics view for Aztech POS.

Provides full analytics, metric cards, and transaction history breakdown.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
import customtkinter as ctk

from frontend.theme import Theme


class SalesView(ctk.CTkFrame):
    """Encapsulates the Sales dashboard with metric cards and full transaction breakdown."""

    def __init__(self, parent, sales_data: Optional[List[Any]] = None):
        super().__init__(parent, fg_color=Theme.BG, corner_radius=0)
        self.parent = parent
        self.sales_data = sales_data if sales_data is not None else []

        # Pack immediately into parent
        self.pack(fill="both", expand=True)

        self._build_ui()
        self.refresh_sales()

    def _build_ui(self):
        # Main Outer Container
        main = ctk.CTkFrame(self, fg_color=Theme.BG, corner_radius=0)
        main.pack(fill="both", expand=True, padx=16, pady=16)

        # White Container Panel
        sales_container = ctk.CTkFrame(
            main,
            fg_color=Theme.CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=Theme.BORDER
        )
        sales_container.pack(fill="both", expand=True)

        # ======================================================
        # TOP SUMMARY METRICS (TODAY & THIS MONTH)
        # ======================================================
        summary_frame = ctk.CTkFrame(sales_container, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, pady=(20, 10))
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)

        # 1. Today Frame
        today_frame = ctk.CTkFrame(
            summary_frame,
            fg_color=Theme.WHITE,
            corner_radius=10,
            border_width=2,
            border_color=Theme.PRIMARY
        )
        today_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(
            today_frame,
            text="Sales for this day",
            font=Theme.font(18, "bold"),
            text_color=Theme.DARK
        ).pack(anchor="w", padx=20, pady=(16, 6))

        self.today_sales_amount_label = ctk.CTkLabel(
            today_frame,
            text="₱0.00",
            font=Theme.font(32, "bold"),
            text_color=Theme.PRIMARY
        )
        self.today_sales_amount_label.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            today_frame,
            text="Total sales today",
            font=Theme.font(12),
            text_color=Theme.GRAY
        ).pack(anchor="w", padx=20, pady=(2, 8))

        self.today_transactions_label = ctk.CTkLabel(
            today_frame,
            text="Transactions: 0",
            font=Theme.font(14, "bold"),
            text_color=Theme.DARK
        )
        self.today_transactions_label.pack(anchor="w", padx=20, pady=(0, 16))

        # 2. Month Frame
        month_frame = ctk.CTkFrame(
            summary_frame,
            fg_color=Theme.WHITE,
            corner_radius=10,
            border_width=2,
            border_color=Theme.PRIMARY
        )
        month_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(
            month_frame,
            text="Sales for this Month",
            font=Theme.font(18, "bold"),
            text_color=Theme.DARK
        ).pack(anchor="w", padx=20, pady=(16, 6))

        self.month_sales_amount_label = ctk.CTkLabel(
            month_frame,
            text="₱0.00",
            font=Theme.font(32, "bold"),
            text_color=Theme.PRIMARY
        )
        self.month_sales_amount_label.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            month_frame,
            text="Total sales this month",
            font=Theme.font(12),
            text_color=Theme.GRAY
        ).pack(anchor="w", padx=20, pady=(2, 8))

        self.month_transactions_label = ctk.CTkLabel(
            month_frame,
            text="Transactions: 0",
            font=Theme.font(14, "bold"),
            text_color=Theme.DARK
        )
        self.month_transactions_label.pack(anchor="w", padx=20, pady=(0, 16))

        # ======================================================
        # TRANSACTION HISTORY SECTION
        # ======================================================
        history_header = ctk.CTkFrame(
            sales_container,
            height=50,
            fg_color=Theme.PRIMARY,
            corner_radius=8
        )
        history_header.pack(fill="x", padx=20, pady=(10, 10))
        history_header.pack_propagate(False)

        ctk.CTkLabel(
            history_header,
            text="TRANSACTION HISTORY",
            font=Theme.font(15, "bold"),
            text_color=Theme.WHITE
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            history_header,
            text="Refresh",
            width=86,
            height=34,
            corner_radius=6,
            fg_color=Theme.PRIMARY_DARK,
            hover_color=Theme.PRIMARY_HOVER,
            font=Theme.font(11, "bold"),
            command=self.refresh_sales
        ).pack(side="right", padx=12)

        # Scrollable transaction area
        self.sales_history_frame = ctk.CTkScrollableFrame(
            sales_container,
            fg_color="transparent"
        )
        self.sales_history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    # ==========================================================
    # METRIC CALCULATIONS
    # ==========================================================

    def _get_sale_datetime(self, record: Any) -> datetime:
        d = record.get("date") if isinstance(record, dict) else getattr(record, "date", None)
        if isinstance(d, datetime):
            return d
        return datetime.now()

    def _get_sale_total(self, record: Any) -> float:
        try:
            val = record.get("total") if isinstance(record, dict) else getattr(record, "total", 0)
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    def get_today_total(self) -> float:
        today = datetime.now().date()
        return sum(self._get_sale_total(r) for r in self.sales_data if self._get_sale_datetime(r).date() == today)

    def get_today_transactions(self) -> int:
        today = datetime.now().date()
        return sum(1 for r in self.sales_data if self._get_sale_datetime(r).date() == today)

    def get_month_total(self) -> float:
        now = datetime.now()
        return sum(
            self._get_sale_total(r) for r in self.sales_data
            if self._get_sale_datetime(r).year == now.year and self._get_sale_datetime(r).month == now.month
        )

    def get_month_transactions(self) -> int:
        now = datetime.now()
        return sum(
            1 for r in self.sales_data
            if self._get_sale_datetime(r).year == now.year and self._get_sale_datetime(r).month == now.month
        )

    # ==========================================================
    # REFRESH & RENDER
    # ==========================================================

    def refresh_sales(self):
        today_total = self.get_today_total()
        today_tx = self.get_today_transactions()
        month_total = self.get_month_total()
        month_tx = self.get_month_transactions()

        if hasattr(self, "today_sales_amount_label") and self.today_sales_amount_label.winfo_exists():
            self.today_sales_amount_label.configure(text=f"₱{today_total:,.2f}")
        if hasattr(self, "today_transactions_label") and self.today_transactions_label.winfo_exists():
            self.today_transactions_label.configure(text=f"Transactions: {today_tx}")
        if hasattr(self, "month_sales_amount_label") and self.month_sales_amount_label.winfo_exists():
            self.month_sales_amount_label.configure(text=f"₱{month_total:,.2f}")
        if hasattr(self, "month_transactions_label") and self.month_transactions_label.winfo_exists():
            self.month_transactions_label.configure(text=f"Transactions: {month_tx}")

        if not hasattr(self, "sales_history_frame") or not self.sales_history_frame.winfo_exists():
            return

        for w in self.sales_history_frame.winfo_children():
            w.destroy()

        if not self.sales_data:
            ctk.CTkLabel(
                self.sales_history_frame,
                text="No transactions yet.",
                font=Theme.font(15, "bold"),
                text_color=Theme.GRAY
            ).pack(pady=50)
            return

        records = list(reversed(self.sales_data))
        for index, record in enumerate(records, start=1):
            tx_num = len(self.sales_data) - index + 1
            dt = self._get_sale_datetime(record)
            total = self._get_sale_total(record)
            cash = float(record.get("cash", total) if isinstance(record, dict) else getattr(record, "cash", total))
            change = float(record.get("change", 0) if isinstance(record, dict) else getattr(record, "change", 0))

            card = ctk.CTkFrame(
                self.sales_history_frame,
                fg_color=Theme.WHITE,
                corner_radius=10,
                border_width=1,
                border_color=Theme.BORDER
            )
            card.pack(fill="x", pady=6)

            # Transaction Header
            head = ctk.CTkFrame(card, fg_color="transparent")
            head.pack(fill="x", padx=16, pady=(12, 6))

            ctk.CTkLabel(
                head,
                text=f"Transaction #{tx_num}",
                font=Theme.font(14, "bold"),
                text_color=Theme.DARK
            ).pack(side="left")

            ctk.CTkLabel(
                head,
                text=dt.strftime("%B %d, %Y  •  %I:%M %p"),
                font=Theme.font(11),
                text_color=Theme.GRAY
            ).pack(side="right")

            # Items Frame (light gray box)
            items = record.get("items", []) if isinstance(record, dict) else getattr(record, "items", [])
            if items:
                items_box = ctk.CTkFrame(card, fg_color=Theme.BG, corner_radius=8)
                items_box.pack(fill="x", padx=16, pady=4)

                for item in items:
                    name = item.get("name", "Product")
                    qty = item.get("quantity", 1)
                    price = float(item.get("price", 0))
                    subtotal = price * qty

                    item_row = ctk.CTkFrame(items_box, fg_color="transparent")
                    item_row.pack(fill="x", padx=12, pady=5)

                    ctk.CTkLabel(
                        item_row,
                        text=f"{name}  x{qty}",
                        font=Theme.font(12, "bold"),
                        text_color=Theme.DARK,
                        anchor="w"
                    ).pack(side="left")

                    ctk.CTkLabel(
                        item_row,
                        text=f"₱{subtotal:,.2f}",
                        font=Theme.font(12),
                        text_color=Theme.DARK
                    ).pack(side="right")

            # Payment Info 3-Column Footer
            payment_info = ctk.CTkFrame(card, fg_color="transparent")
            payment_info.pack(fill="x", padx=16, pady=(6, 12))

            # Column 1: Total
            tot_col = ctk.CTkFrame(payment_info, fg_color="transparent")
            tot_col.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(tot_col, text="TOTAL", font=Theme.font(10, "bold"), text_color=Theme.GRAY, anchor="w").pack(anchor="w")
            ctk.CTkLabel(tot_col, text=f"₱{total:,.2f}", font=Theme.font(17, "bold"), text_color=Theme.PRIMARY, anchor="w").pack(anchor="w")

            # Column 2: Cash
            cash_col = ctk.CTkFrame(payment_info, fg_color="transparent")
            cash_col.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(cash_col, text="CASH", font=Theme.font(10, "bold"), text_color=Theme.GRAY, anchor="w").pack(anchor="w")
            ctk.CTkLabel(cash_col, text=f"₱{cash:,.2f}", font=Theme.font(17, "bold"), text_color=Theme.DARK, anchor="w").pack(anchor="w")

            # Column 3: Change
            chg_col = ctk.CTkFrame(payment_info, fg_color="transparent")
            chg_col.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(chg_col, text="CHANGE", font=Theme.font(10, "bold"), text_color=Theme.GRAY, anchor="w").pack(anchor="w")
            ctk.CTkLabel(chg_col, text=f"₱{change:,.2f}", font=Theme.font(17, "bold"), text_color=Theme.DARK, anchor="w").pack(anchor="w")


# Backward-compatible alias
Sales = SalesView