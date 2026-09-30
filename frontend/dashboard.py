"""Main POS Dashboard for Aztech POS & Inventory."""
import os
import math
from typing import List, Dict, Any, Optional
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from frontend.theme import Theme
from frontend.models import Cart, CartItem, SaleRecord, get_default_products
from frontend.modals import CartModal, PaymentModal
from frontend.inventory import Inventory
from frontend.sales import SalesView


class ProductCard(ctk.CTkFrame):
    """Reusable card component for displaying a product in the POS grid."""

    def __init__(self, parent, product: Any, on_buy_now, on_add_to_cart, image_path: Optional[str] = None):
        super().__init__(
            parent,
            fg_color=Theme.CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=Theme.BORDER
        )
        self.product = product
        self.on_buy_now = on_buy_now
        self.on_add_to_cart = on_add_to_cart
        self.image_path = image_path

        self._build_ui()

    def _build_ui(self):
        # 1. Bottom action dock (Price + Action buttons)
        bottom_dock = ctk.CTkFrame(self, fg_color="transparent")
        bottom_dock.pack(side="bottom", fill="x", padx=12, pady=(4, 12))

        price_val = float(self.product.get("price", 0))
        price_row = ctk.CTkFrame(bottom_dock, fg_color="transparent")
        price_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            price_row,
            text=f"₱{price_val:,.2f}",
            font=Theme.font(18, "bold"),
            text_color=Theme.PRIMARY,
            anchor="w"
        ).pack(side="left")

        btn_row = ctk.CTkFrame(bottom_dock, fg_color="transparent")
        btn_row.pack(fill="x")

        ctk.CTkButton(
            btn_row,
            text="Buy Now",
            height=40,
            corner_radius=8,
            fg_color=Theme.PRIMARY_DARK,
            hover_color=Theme.PRIMARY,
            font=Theme.font(12, "bold"),
            command=lambda: self.on_buy_now(self.product)
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text="Add to Cart",
            height=40,
            corner_radius=8,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER,
            font=Theme.font(12, "bold"),
            command=lambda: self.on_add_to_cart(self.product)
        ).pack(side="left", fill="x", expand=True, padx=(4, 0))

        # 2. Top Image Area (Enlarged 140px container, 200x130 thumbnail)
        img_container = ctk.CTkFrame(self, height=140, fg_color=Theme.IMAGE_GRAY, corner_radius=8)
        img_container.pack(fill="x", padx=12, pady=(12, 8))
        img_container.pack_propagate(False)

        img_label = ctk.CTkLabel(img_container, text="🖥", font=Theme.font(30))
        img_label.place(relx=0.5, rely=0.5, anchor="center")

        if self.image_path and os.path.exists(self.image_path):
            try:
                pil_img = Image.open(self.image_path)
                pil_img.thumbnail((200, 130))
                ctk_img = ctk.CTkImage(light_image=pil_img, size=pil_img.size)
                img_label.configure(image=ctk_img, text="")
                img_label.image = ctk_img
            except Exception:
                pass

        # 3. Product Info
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=12, pady=(0, 4))

        # Category Tag
        cat_badge = ctk.CTkFrame(info_frame, fg_color=Theme.PRIMARY_LIGHT, corner_radius=12, height=24)
        cat_badge.pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(
            cat_badge,
            text=str(self.product.get("category", "")),
            font=Theme.font(11, "bold"),
            text_color=Theme.PRIMARY
        ).pack(padx=10, pady=2)

        # Name
        name_str = str(self.product.get("name", ""))
        ctk.CTkLabel(
            info_frame,
            text=name_str,
            font=Theme.font(15, "bold"),
            text_color=Theme.DARK,
            anchor="w",
            wraplength=270
        ).pack(fill="x", anchor="w")

        # Description
        desc_str = str(self.product.get("description", ""))
        if len(desc_str) > 45:
            desc_str = desc_str[:42] + "..."
        ctk.CTkLabel(
            info_frame,
            text=desc_str,
            font=Theme.font(12),
            text_color=Theme.GRAY,
            anchor="w",
            wraplength=270
        ).pack(fill="x", anchor="w", pady=(2, 0))


class Dashboard:
    """Main POS Application Window and Navigation Controller."""

    # Backward-compatibility color constants
    TEAL = Theme.PRIMARY
    DARK_TEAL = Theme.PRIMARY_DARK
    LIGHT_TEAL = Theme.PRIMARY_LIGHT
    WHITE = Theme.WHITE
    BG = Theme.BG
    DARK = Theme.DARK
    GRAY = Theme.GRAY
    BORDER = Theme.BORDER
    RED = Theme.DANGER
    IMAGE_GRAY = Theme.IMAGE_GRAY

    def __init__(self, parent):
        self.parent = parent

        self.root = ctk.CTkToplevel(parent)
        self.root.title("Aztech Computer Store - POS")
        self.root.state("zoomed")
        self.root.minsize(1024, 600)
        self.root.configure(fg_color=Theme.BG)

        # Domain State
        self.cart = Cart()
        self.cart_window = None
        self.sales_records: List[Dict[str, Any]] = []
        self.sales_view: Optional[SalesView] = None
        self.today_sales_amount_label = None
        self.today_transactions_label = None
        self.month_sales_amount_label = None
        self.month_transactions_label = None
        self.sales_history_frame = None

        # Product Catalog
        self.products: List[Dict[str, Any]] = get_default_products()
        self.filtered_products = self.products.copy()

        self.current_category = "All"
        self.active_nav = "products"

        self._build_ui()
        self.show_products_page()

    # ==========================================================
    # IMAGE RESOLUTION
    # ==========================================================

    def get_product_image_path(self, image_path: Optional[str]) -> Optional[str]:
        if not image_path:
            return None
        if os.path.isabs(image_path) and os.path.exists(image_path):
            return image_path
        if os.path.exists(image_path):
            return os.path.abspath(image_path)

        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate = os.path.join(project_folder, image_path)
        if os.path.exists(candidate):
            return candidate

        frontend_images = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            os.path.basename(image_path)
        )
        if os.path.exists(frontend_images):
            return frontend_images

        return None

    # ==========================================================
    # UI SHELL
    # ==========================================================

    def _build_ui(self):
        content = ctk.CTkFrame(self.root, fg_color=Theme.BG, corner_radius=0)
        content.pack(fill="both", expand=True, padx=8, pady=8)

        # 1. Unified Header Bar (matching layout specification)
        header_bar = ctk.CTkFrame(content, fg_color=Theme.PRIMARY, corner_radius=14, height=64)
        header_bar.pack(fill="x", pady=(0, 8))
        header_bar.pack_propagate(False)

        # Left: Welcome Text
        w_left = ctk.CTkFrame(header_bar, fg_color="transparent")
        w_left.pack(side="left", fill="y", padx=20)

        ctk.CTkLabel(
            w_left,
            text="Welcome Back, ADMIN!",
            font=Theme.font(16, "bold"),
            text_color=Theme.WHITE,
            anchor="w"
        ).pack(side="left", pady=18)

        # Right: Logout Pill Button
        ctk.CTkButton(
            header_bar,
            text="Logout",
            width=100,
            height=36,
            corner_radius=18,
            fg_color="#E05656",
            hover_color="#C94545",
            text_color=Theme.WHITE,
            font=Theme.font(12, "bold"),
            command=self.logout
        ).pack(side="right", padx=20, pady=14)

        # Center: Darker Blue Pill Container for Navigation Tabs
        center_pill = ctk.CTkFrame(
            header_bar,
            fg_color=Theme.PRIMARY_DARK,
            corner_radius=18,
            height=46
        )
        center_pill.place(relx=0.5, rely=0.5, anchor="center")

        tabs_box = ctk.CTkFrame(center_pill, fg_color="transparent")
        tabs_box.pack(padx=6, pady=5)

        self.products_nav = ctk.CTkButton(
            tabs_box,
            text="PRODUCTS",
            width=115,
            height=34,
            corner_radius=14,
            font=Theme.font(12, "bold"),
            command=self.show_products_page
        )
        self.products_nav.pack(side="left", padx=4)

        self.inventory_nav = ctk.CTkButton(
            tabs_box,
            text="INVENTORY",
            width=115,
            height=34,
            corner_radius=14,
            font=Theme.font(12, "bold"),
            command=self.open_inventory
        )
        self.inventory_nav.pack(side="left", padx=4)

        self.sales_nav = ctk.CTkButton(
            tabs_box,
            text="SALES",
            width=110,
            height=34,
            corner_radius=14,
            font=Theme.font(12, "bold"),
            command=self.open_sales
        )
        self.sales_nav.pack(side="left", padx=4)

        # 2. Docked Cart Frame (always packed at bottom before page_frame)
        self.cart_frame = ctk.CTkFrame(content, fg_color=Theme.CARD_BG, corner_radius=10,
                                       border_width=1, border_color=Theme.BORDER, height=62)
        self.cart_frame.pack(side="bottom", fill="x", pady=(6, 0))
        self.cart_frame.pack_propagate(False)

        c_info = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        c_info.pack(side="left", padx=18, fill="y")

        self.cart_summary_label = ctk.CTkLabel(
            c_info, text="🛒 Cart: 0 items • Total: ₱0.00",
            font=Theme.font(14, "bold"), text_color=Theme.DARK
        )
        self.cart_summary_label.pack(side="left", pady=16)

        c_btns = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        c_btns.pack(side="right", padx=14, fill="y")

        ctk.CTkButton(
            c_btns, text="View Cart", width=105, height=38, corner_radius=6,
            fg_color=Theme.WHITE, hover_color=Theme.PRIMARY_LIGHT, text_color=Theme.PRIMARY,
            border_width=1, border_color=Theme.BORDER, font=Theme.font(11, "bold"),
            command=self.open_cart
        ).pack(side="left", padx=4, pady=12)

        ctk.CTkButton(
            c_btns, text="Pay Now", width=105, height=38, corner_radius=6,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(11, "bold"), command=self.proceed_to_pay
        ).pack(side="left", padx=4, pady=12)

        # 3. Main Page Container
        self.page_frame = ctk.CTkFrame(content, fg_color=Theme.BG, corner_radius=0)
        self.page_frame.pack(fill="both", expand=True)

    def _set_active_nav(self, nav_name: str):
        self.active_nav = nav_name
        for name, btn in [("products", self.products_nav),
                          ("inventory", self.inventory_nav),
                          ("sales", self.sales_nav)]:
            active = (name == nav_name)
            btn.configure(
                fg_color=Theme.WHITE if active else "#CBD5E1",
                text_color=Theme.PRIMARY_DARK if active else Theme.DARK,
                hover_color=Theme.WHITE if active else "#E2E8F0"
            )

    # ==========================================================
    # POS PRODUCTS VIEW
    # ==========================================================

    def show_products_page(self):
        self._set_active_nav("products")
        if hasattr(self, "cart_frame"):
            self.cart_frame.pack(side="bottom", fill="x", pady=(6, 0))

        for w in self.page_frame.winfo_children():
            w.destroy()

        # Top Controls: Search + Categories
        top_ctrl = ctk.CTkFrame(self.page_frame, fg_color=Theme.CARD_BG, corner_radius=10,
                                border_width=1, border_color=Theme.BORDER)
        top_ctrl.pack(fill="x", pady=(0, 6))

        # Search Row
        s_row = ctk.CTkFrame(top_ctrl, fg_color="transparent")
        s_row.pack(fill="x", padx=14, pady=(10, 8))

        self.search_entry = ctk.CTkEntry(
            s_row, placeholder_text="Search parts by name...",
            height=42, font=Theme.font(12), border_color=Theme.BORDER
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_products())

        ctk.CTkButton(
            s_row, text="Search", width=90, height=42, corner_radius=8,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(12, "bold"), command=self.search_products
        ).pack(side="right")

        # Category Buttons Row + Products Counter
        cat_row = ctk.CTkFrame(top_ctrl, fg_color="transparent")
        cat_row.pack(fill="x", padx=14, pady=(0, 10))

        categories = ["All", "CPU", "GPU", "RAM", "Storage", "Motherboard", "PSU", "Other"]
        self.cat_buttons = {}

        cat_btns_box = ctk.CTkFrame(cat_row, fg_color="transparent")
        cat_btns_box.pack(side="left")

        for cat in categories:
            btn = ctk.CTkButton(
                cat_btns_box, text=cat, height=32, corner_radius=16,
                font=Theme.font(11, "bold"),
                command=lambda c=cat: self.filter_category(c)
            )
            btn.pack(side="left", padx=3)
            self.cat_buttons[cat] = btn

        self.product_count_label = ctk.CTkLabel(
            cat_row, text=f"{len(self.filtered_products)} products",
            font=Theme.font(12, "bold"), text_color=Theme.GRAY
        )
        self.product_count_label.pack(side="right", padx=6)

        self._update_cat_button_styles()

        # Product Cards Scrollable Grid (3 items per row)
        self.product_area = ctk.CTkScrollableFrame(self.page_frame, fg_color="transparent")
        self.product_area.pack(fill="both", expand=True)

        for col in range(3):
            self.product_area.grid_columnconfigure(col, weight=1, uniform="card")

        self.create_product_cards()

    def _update_cat_button_styles(self):
        for cat, btn in self.cat_buttons.items():
            active = (cat == self.current_category)
            btn.configure(
                fg_color=Theme.PRIMARY if active else Theme.WHITE,
                text_color=Theme.WHITE if active else Theme.DARK,
                border_width=0 if active else 1,
                border_color=Theme.BORDER,
                hover_color=Theme.PRIMARY_DARK if active else Theme.PRIMARY_LIGHT
            )

    def filter_category(self, category: str):
        self.current_category = category
        self._update_cat_button_styles()
        self._apply_filters()

    def search_products(self):
        self._apply_filters()

    def _apply_filters(self):
        query = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""
        results = []

        for p in self.products:
            p_name = str(p.get("name", "")).lower()
            p_cat = str(p.get("category", "")).lower()
            p_desc = str(p.get("description", "")).lower()

            matches_cat = (self.current_category == "All") or (p_cat == self.current_category.lower())
            matches_query = not query or (query in p_name or query in p_cat or query in p_desc)

            if matches_cat and matches_query:
                results.append(p)

        self.filtered_products = results
        self.create_product_cards()

    def create_product_cards(self):
        for w in self.product_area.winfo_children():
            w.destroy()

        if hasattr(self, "product_count_label"):
            self.product_count_label.configure(text=f"{len(self.filtered_products)} products")

        if not self.filtered_products:
            ctk.CTkLabel(
                self.product_area, text="No products found.",
                font=Theme.font(16, "bold"), text_color=Theme.GRAY
            ).pack(pady=60)
            return

        # Render all products in a 3-column scrollable grid
        for idx, prod in enumerate(self.filtered_products):
            row = idx // 3
            col = idx % 3
            img_path = self.get_product_image_path(prod.get("image"))

            card = ProductCard(
                self.product_area,
                product=prod,
                on_buy_now=self.buy_now,
                on_add_to_cart=self.add_to_cart,
                image_path=img_path
            )
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    # ==========================================================
    # CART & CHECKOUT OPERATIONS
    # ==========================================================

    def add_to_cart(self, product: Any):
        self.cart.add(product)
        self.update_cart_total()

    def buy_now(self, product: Any):
        PaymentModal(
            self.root,
            items=[{"product": product, "quantity": 1}],
            total=float(product.get("price", 0)),
            on_success=self.record_sale
        )

    def update_cart_total(self):
        self.cart_summary_label.configure(
            text=f"🛒 Cart: {self.cart.total_items} items • Total: {self.cart.formatted_total}"
        )

    def open_cart(self):
        if len(self.cart) == 0:
            messagebox.showinfo("Empty Cart", "Your cart is currently empty.", parent=self.root)
            return

        if self.cart_window and self.cart_window.winfo_exists():
            self.cart_window.destroy()

        self.cart_window = CartModal(
            self.root,
            cart=self.cart,
            on_checkout=self.proceed_to_pay,
            get_image_path_fn=self.get_product_image_path
        )

    def proceed_to_pay(self):
        if len(self.cart) == 0:
            messagebox.showinfo("Empty Cart", "Your cart is empty.", parent=self.root)
            return

        if self.cart_window and self.cart_window.winfo_exists():
            self.cart_window.destroy()
            self.cart_window = None

        PaymentModal(
            self.root,
            items=self.cart.to_legacy_list(),
            total=self.cart.total_amount,
            on_success=self._on_cart_payment_success
        )

    def _on_cart_payment_success(self, items, total, cash, change, method):
        self.record_sale(items, total, cash, change, method)
        self.cart.clear()
        self.update_cart_total()

    def record_sale(self, cart_items, total, cash, change, payment_method="Cash"):
        sale_record = {
            "date": datetime.now(),
            "items": [],
            "total": float(total),
            "cash": float(cash),
            "change": float(change),
            "payment_method": payment_method
        }
        for item in cart_items:
            prod = item.get("product", item)
            qty = int(item.get("quantity", 1))
            name = prod.get("name", "Unknown") if isinstance(prod, dict) else str(prod)
            cat = prod.get("category", "Other") if isinstance(prod, dict) else "Other"
            price = float(prod.get("price", 0)) if isinstance(prod, dict) else float(total)
            sale_record["items"].append({
                "name": name,
                "category": cat,
                "price": price,
                "quantity": qty
            })
        self.sales_records.append(sale_record)
        self.refresh_sales_page()

    def refresh_sales_page(self):
        if hasattr(self, "sales_view") and self.sales_view and self.sales_view.winfo_exists():
            self.sales_view.refresh_sales()

    # ==========================================================
    # NAVIGATION HANDLERS
    # ==========================================================

    def open_inventory(self):
        self._set_active_nav("inventory")
        if hasattr(self, "cart_frame"):
            self.cart_frame.pack_forget()

        for w in self.page_frame.winfo_children():
            w.destroy()

        Inventory(self.page_frame, self.products, refresh_callback=self.refresh_products)

    def open_sales(self):
        self._set_active_nav("sales")
        if hasattr(self, "cart_frame"):
            self.cart_frame.pack_forget()

        for w in self.page_frame.winfo_children():
            w.destroy()

        self.sales_view = SalesView(self.page_frame, self.sales_records)
        self.today_sales_amount_label = self.sales_view.today_sales_amount_label
        self.today_transactions_label = self.sales_view.today_transactions_label
        self.month_sales_amount_label = self.sales_view.month_sales_amount_label
        self.month_transactions_label = self.sales_view.month_transactions_label
        self.sales_history_frame = self.sales_view.sales_history_frame

    def refresh_products(self):
        self.filtered_products = self.products.copy()
        if self.active_nav == "products":
            self.create_product_cards()

    def logout(self):
        confirmed = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?", parent=self.root)
        if confirmed:
            self.root.destroy()
            self.parent.deiconify()