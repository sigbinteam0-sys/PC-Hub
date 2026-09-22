import customtkinter as ctk

from products import Products
from categories import Categories
from pos import POS
from sales import Sales
from sales_summary import SalesSummary


class Dashboard:

    def __init__(self, parent, on_logout):

        self.parent = parent
        self.on_logout = on_logout

        # ==================================================
        # MAIN WINDOW
        # ==================================================

        self.window = ctk.CTkToplevel(parent)

        self.window.title("PC Hub - Dashboard")
        self.window.geometry("1200x750")

        self.window.minsize(
            1000,
            650
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.logout
        )

        # ==================================================
        # TOP NAVIGATION BAR
        # ==================================================

        self.navbar = ctk.CTkFrame(
            self.window,
            height=70,
            corner_radius=0,
            fg_color="white"
        )

        self.navbar.pack(
            side="top",
            fill="x"
        )

        self.navbar.pack_propagate(False)

        # ==================================================
        # PC HUB LOGO
        # ==================================================

        self.logo_label = ctk.CTkLabel(
            self.navbar,
            text="PC Hub",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color="#3B8ED0"
        )

        self.logo_label.pack(
            side="left",
            padx=(30, 30)
        )

        # ==================================================
        # DASHBOARD BUTTON
        # ==================================================

        self.dashboard_button = ctk.CTkButton(
            self.navbar,
            text="Dashboard",
            width=100,
            height=38,
            command=self.show_home
        )

        self.dashboard_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # PRODUCTS BUTTON
        # ==================================================

        self.products_button = ctk.CTkButton(
            self.navbar,
            text="Products",
            width=90,
            height=38,
            fg_color="transparent",
            text_color="black",
            hover_color="#E8E8E8",
            command=self.show_products
        )

        self.products_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # CATEGORIES BUTTON
        # ==================================================

        self.categories_button = ctk.CTkButton(
            self.navbar,
            text="Categories",
            width=100,
            height=38,
            fg_color="transparent",
            text_color="black",
            hover_color="#E8E8E8",
            command=self.show_categories
        )

        self.categories_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # NEW SALE BUTTON
        # ==================================================

        self.pos_button = ctk.CTkButton(
            self.navbar,
            text="New Sale",
            width=90,
            height=38,
            fg_color="transparent",
            text_color="black",
            hover_color="#E8E8E8",
            command=self.show_pos
        )

        self.pos_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # SALES HISTORY BUTTON
        # ==================================================

        self.sales_button = ctk.CTkButton(
            self.navbar,
            text="Sales History",
            width=110,
            height=38,
            fg_color="transparent",
            text_color="black",
            hover_color="#E8E8E8",
            command=self.show_sales
        )

        self.sales_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # REPORTS BUTTON
        # ==================================================

        self.reports_button = ctk.CTkButton(
            self.navbar,
            text="Reports",
            width=90,
            height=38,
            fg_color="transparent",
            text_color="black",
            hover_color="#E8E8E8",
            command=self.show_summary
        )

        self.reports_button.pack(
            side="left",
            padx=5
        )

        # ==================================================
        # LOGOUT
        # ==================================================

        self.logout_button = ctk.CTkButton(
            self.navbar,
            text="Logout",
            width=80,
            height=38,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.logout
        )

        self.logout_button.pack(
            side="right",
            padx=25
        )

        # ==================================================
        # CONTENT AREA
        # ==================================================

        self.content = ctk.CTkFrame(
            self.window,
            corner_radius=0,
            fg_color="#F5F6FA"
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # SHOW HOME
        # ==================================================

        self.show_home()

    # ==================================================
    # CLEAR CONTENT
    # ==================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ==================================================
    # DASHBOARD HOME
    # ==================================================

    def show_home(self):

        self.clear_content()

        # ==================================================
        # HEADER
        # ==================================================

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 10)
        )

        # LEFT HEADER

        header_left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        header_left.pack(
            side="left"
        )

        welcome_label = ctk.CTkLabel(
            header_left,
            text="Good Morning, Admin!",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        welcome_label.pack(
            anchor="w"
        )

        subtitle_label = ctk.CTkLabel(
            header_left,
            text="Here's what's happening in your store today.",
            text_color="#777777"
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        # ==================================================
        # NEW SALE BUTTON
        # ==================================================

        new_sale_button = ctk.CTkButton(
            header,
            text="+ New Sale",
            width=130,
            height=40,
            command=self.show_pos
        )

        new_sale_button.pack(
            side="right",
            pady=5
        )

        # ==================================================
        # SUMMARY CARDS
        # ==================================================

        cards = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            padx=35,
            pady=(15, 10)
        )

        # ==================================================
        # TOTAL SALES
        # ==================================================

        total_sales_card = ctk.CTkFrame(
            cards,
            height=115,
            fg_color="white"
        )

        total_sales_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        total_sales_title = ctk.CTkLabel(
            total_sales_card,
            text="Total Sales",
            text_color="#777777"
        )

        total_sales_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        total_sales_value = ctk.CTkLabel(
            total_sales_card,
            text="₱125,000.00",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        total_sales_value.pack(
            anchor="w",
            padx=20
        )

        total_sales_subtitle = ctk.CTkLabel(
            total_sales_card,
            text="This month",
            text_color="#777777"
        )

        total_sales_subtitle.pack(
            anchor="w",
            padx=20,
            pady=(3, 10)
        )

        # ==================================================
        # TOTAL PRODUCTS
        # ==================================================

        products_card = ctk.CTkFrame(
            cards,
            height=115,
            fg_color="white"
        )

        products_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        products_title = ctk.CTkLabel(
            products_card,
            text="Total Products",
            text_color="#777777"
        )

        products_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        products_value = ctk.CTkLabel(
            products_card,
            text="150",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        products_value.pack(
            anchor="w",
            padx=20
        )

        products_subtitle = ctk.CTkLabel(
            products_card,
            text="Items in inventory",
            text_color="#777777"
        )

        products_subtitle.pack(
            anchor="w",
            padx=20,
            pady=(3, 10)
        )

        # ==================================================
        # CATEGORIES
        # ==================================================

        categories_card = ctk.CTkFrame(
            cards,
            height=115,
            fg_color="white"
        )

        categories_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        categories_title = ctk.CTkLabel(
            categories_card,
            text="Categories",
            text_color="#777777"
        )

        categories_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        categories_value = ctk.CTkLabel(
            categories_card,
            text="12",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        categories_value.pack(
            anchor="w",
            padx=20
        )

        categories_subtitle = ctk.CTkLabel(
            categories_card,
            text="Product categories",
            text_color="#777777"
        )

        categories_subtitle.pack(
            anchor="w",
            padx=20,
            pady=(3, 10)
        )

        # ==================================================
        # LOW STOCK
        # ==================================================

        stock_card = ctk.CTkFrame(
            cards,
            height=115,
            fg_color="white"
        )

        stock_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        stock_title = ctk.CTkLabel(
            stock_card,
            text="Low Stock",
            text_color="#777777"
        )

        stock_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        stock_value = ctk.CTkLabel(
            stock_card,
            text="8",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        stock_value.pack(
            anchor="w",
            padx=20
        )

        stock_subtitle = ctk.CTkLabel(
            stock_card,
            text="Items need attention",
            text_color="#777777"
        )

        stock_subtitle.pack(
            anchor="w",
            padx=20,
            pady=(3, 10)
        )

        # ==================================================
        # LOWER CONTENT
        # ==================================================

        lower = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        lower.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(10, 30)
        )

        # ==================================================
        # SALES OVERVIEW
        # ==================================================

        sales_overview = ctk.CTkFrame(
            lower,
            fg_color="white"
        )

        sales_overview.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        overview_title = ctk.CTkLabel(
            sales_overview,
            text="Sales Overview",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        overview_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 3)
        )

        overview_subtitle = ctk.CTkLabel(
            sales_overview,
            text="Monthly sales performance",
            text_color="#777777"
        )

        overview_subtitle.pack(
            anchor="w",
            padx=20
        )

        # ==================================================
        # SALES CHART PLACEHOLDER
        # ==================================================

        chart = ctk.CTkFrame(
            sales_overview,
            fg_color="#EAF4FC"
        )

        chart.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        chart_title = ctk.CTkLabel(
            chart,
            text="Sales Chart",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color="#3B8ED0"
        )

        chart_title.pack(
            pady=(65, 5)
        )

        chart_amount = ctk.CTkLabel(
            chart,
            text="₱125,000",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color="#3B8ED0"
        )

        chart_amount.pack(
            pady=5
        )

        chart_message = ctk.CTkLabel(
            chart,
            text="Sales data will appear here",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color="#3B8ED0"
        )

        chart_message.pack(
            pady=5
        )

        # ==================================================
        # RECENT TRANSACTIONS
        # ==================================================

        transactions = ctk.CTkFrame(
            lower,
            fg_color="white"
        )

        transactions.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        transactions_title = ctk.CTkLabel(
            transactions,
            text="Recent Transactions",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        transactions_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
        )

        # ==================================================
        # TRANSACTION 1
        # ==================================================

        self.create_transaction(
            transactions,
            "Sale #001",
            "₱2,500.00"
        )

        # ==================================================
        # TRANSACTION 2
        # ==================================================

        self.create_transaction(
            transactions,
            "Sale #002",
            "₱5,200.00"
        )

        # ==================================================
        # TRANSACTION 3
        # ==================================================

        self.create_transaction(
            transactions,
            "Sale #003",
            "₱1,800.00"
        )

        # ==================================================
        # TRANSACTION 4
        # ==================================================

        self.create_transaction(
            transactions,
            "Sale #004",
            "₱3,750.00"
        )

    # ==================================================
    # CREATE TRANSACTION
    # ==================================================

    def create_transaction(
        self,
        parent,
        sale_id,
        amount
    ):

        transaction = ctk.CTkFrame(
            parent,
            height=50,
            fg_color="#F5F6FA"
        )

        transaction.pack(
            fill="x",
            padx=15,
            pady=6
        )

        transaction.pack_propagate(False)

        sale_label = ctk.CTkLabel(
            transaction,
            text=sale_id
        )

        sale_label.pack(
            side="left",
            padx=15
        )

        amount_label = ctk.CTkLabel(
            transaction,
            text=amount,
            font=ctk.CTkFont(
                weight="bold"
            ),
            text_color="#3B8ED0"
        )

        amount_label.pack(
            side="right",
            padx=15
        )

    # ==================================================
    # PRODUCTS
    # ==================================================

    def show_products(self):

        self.clear_content()

        products_page = Products(
            self.content
        )

        products_page.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # CATEGORIES
    # ==================================================

    def show_categories(self):

        self.clear_content()

        categories_page = Categories(
            self.content
        )

        categories_page.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # POS
    # ==================================================

    def show_pos(self):

        self.clear_content()

        pos_page = POS(
            self.content
        )

        pos_page.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # SALES HISTORY
    # ==================================================

    def show_sales(self):

        self.clear_content()

        sales_page = Sales(
            self.content
        )

        sales_page.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # REPORTS / SALES SUMMARY
    # ==================================================

    def show_summary(self):

        self.clear_content()

        summary_page = SalesSummary(
            self.content
        )

        summary_page.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # LOGOUT
    # ==================================================

    def logout(self):

        self.window.destroy()

        self.on_logout()