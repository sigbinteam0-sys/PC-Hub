"""OOP Modal dialogs for Aztech POS & Inventory.

Includes:
- BaseModal: Helper class for centered, responsive CTkToplevel dialogs.
- ProductFormModal: Unified modal for Adding and Editing products.
- CartModal: Shopping cart dialog with quantity adjusters and checkout.
- PaymentModal: Checkout settlement dialog with change calculator.
"""
import os
import shutil
from typing import Optional, Callable, Dict, Any, List
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image

from frontend.theme import Theme
from frontend.models import Product, Cart, CartItem


class BaseModal(ctk.CTkToplevel):
    """Base class for centered, laptop-responsive modal dialogs."""

    def __init__(self, parent, title: str, width: int = 520, height: int = 680, min_w: int = 440, min_h: int = 420):
        super().__init__(parent)
        self.title(title)
        self.parent = parent

        # Screen dimension centering with responsive bounds
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        actual_w = min(width, max(min_w, screen_w - 40))
        actual_h = min(height, max(min_h, screen_h - 60))
        x = max(0, (screen_w - actual_w) // 2)
        y = max(0, (screen_h - actual_h) // 2)

        self.geometry(f"{actual_w}x{actual_h}+{x}+{y}")
        self.minsize(min_w, min_h)
        self.resizable(True, True)
        self.configure(fg_color=Theme.BG)

        # Modal attachment
        top = parent.winfo_toplevel() if hasattr(parent, "winfo_toplevel") else parent
        self.transient(top)
        try:
            self.grab_set()
        except Exception:
            pass


class ProductFormModal(BaseModal):
    """Unified modal for Adding and Editing products."""

    CATEGORIES = [
        "CPU", "GPU", "RAM", "Storage", "Motherboard",
        "PSU", "Case", "Laptop", "Monitor", "Accessories",
        "Printer", "CCTV", "Pisonet", "Other"
    ]

    def __init__(self, parent, mode: str = "add", product: Optional[Dict[str, Any]] = None,
                 on_save: Optional[Callable[[Dict[str, Any]], None]] = None,
                 get_image_path_fn: Optional[Callable[[str], Optional[str]]] = None):
        title = "Add Product" if mode == "add" else "Update Product"
        super().__init__(parent, title=title, width=520, height=680, min_w=460, min_h=460)

        self.mode = mode
        self.initial_product = product or {}
        self.on_save = on_save
        self.get_image_path_fn = get_image_path_fn
        self.selected_image_path = self.initial_product.get("image", "")

        self._build_ui()
        self._load_initial_data()

    def _build_ui(self):
        # 1. Docked buttons at bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=24, pady=(0, 16))

        save_text = "Add Product" if self.mode == "add" else "Update Product"
        ctk.CTkButton(
            btn_frame,
            text=save_text,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK,
            text_color=Theme.WHITE,
            height=42,
            corner_radius=8,
            font=Theme.font(12, "bold"),
            command=self._handle_save
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=Theme.DARK,
            height=40,
            corner_radius=8,
            font=Theme.font(12, "bold"),
            command=self.destroy
        ).pack(fill="x")

        # 2. Scrollable form area
        form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form_scroll.pack(fill="both", expand=True, padx=20, pady=(16, 8))

        # Title Card
        title_card = ctk.CTkFrame(form_scroll, fg_color=Theme.PRIMARY, corner_radius=10, height=54)
        title_card.pack(fill="x", pady=(0, 14))
        title_card.pack_propagate(False)

        header_title = "Add New Product" if self.mode == "add" else "Update Product Details"
        ctk.CTkLabel(
            title_card,
            text=header_title,
            font=Theme.font(17, "bold"),
            text_color=Theme.WHITE
        ).pack(expand=True)

        # Fields container
        container = ctk.CTkFrame(form_scroll, fg_color=Theme.CARD_BG, corner_radius=10,
                                 border_width=1, border_color=Theme.BORDER)
        container.pack(fill="x", pady=(0, 10))

        # Product Name
        self._add_field_label(container, "Product Name *", pady_top=14)
        self.name_entry = ctk.CTkEntry(container, height=40, placeholder_text="e.g. Intel Core i5 10th Gen",
                                       border_color=Theme.BORDER, font=Theme.font(12))
        self.name_entry.pack(fill="x", padx=16, pady=(0, 10))

        # Category
        self._add_field_label(container, "Category *")
        self.category_var = ctk.StringVar(value="CPU")
        self.category_menu = ctk.CTkOptionMenu(
            container,
            values=self.CATEGORIES,
            variable=self.category_var,
            height=40,
            fg_color=Theme.WHITE,
            button_color=Theme.PRIMARY,
            button_hover_color=Theme.PRIMARY_DARK,
            text_color=Theme.DARK,
            dropdown_text_color=Theme.DARK,
            font=Theme.font(12)
        )
        self.category_menu.pack(fill="x", padx=16, pady=(0, 10))

        # Price
        self._add_field_label(container, "Price (₱) *")
        self.price_entry = ctk.CTkEntry(container, height=40, placeholder_text="e.g. 8500",
                                        border_color=Theme.BORDER, font=Theme.font(12))
        self.price_entry.pack(fill="x", padx=16, pady=(0, 10))

        # Description
        self._add_field_label(container, "Description")
        self.desc_entry = ctk.CTkEntry(container, height=40, placeholder_text="e.g. High-performance processor",
                                       border_color=Theme.BORDER, font=Theme.font(12))
        self.desc_entry.pack(fill="x", padx=16, pady=(0, 10))

        # Image picker
        self._add_field_label(container, "Product Image")
        img_row = ctk.CTkFrame(container, fg_color="transparent")
        img_row.pack(fill="x", padx=16, pady=(0, 10))

        self.img_path_entry = ctk.CTkEntry(img_row, height=40, placeholder_text="Select image file...",
                                           border_color=Theme.BORDER, font=Theme.font(11))
        self.img_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            img_row,
            text="Browse...",
            width=96,
            height=40,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(11, "bold"),
            command=self._browse_image
        ).pack(side="right")

        # Image preview box
        self.preview_frame = ctk.CTkFrame(container, height=120, fg_color=Theme.IMAGE_GRAY, corner_radius=8)
        self.preview_frame.pack(fill="x", padx=16, pady=(0, 16))
        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="No image preview",
            font=Theme.font(11),
            text_color=Theme.GRAY
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

    def _add_field_label(self, parent, text: str, pady_top: int = 4):
        ctk.CTkLabel(
            parent,
            text=text,
            font=Theme.font(12, "bold"),
            text_color=Theme.DARK,
            anchor="w"
        ).pack(fill="x", padx=16, pady=(pady_top, 4))

    def _load_initial_data(self):
        if not self.initial_product:
            return

        self.name_entry.insert(0, str(self.initial_product.get("name", "")))
        cat = str(self.initial_product.get("category", "CPU"))
        if cat in self.CATEGORIES:
            self.category_var.set(cat)
        else:
            self.category_var.set("Other")

        price_val = self.initial_product.get("price", 0)
        self.price_entry.insert(0, str(int(price_val) if float(price_val).is_integer() else price_val))
        self.desc_entry.insert(0, str(self.initial_product.get("description", "")))

        img = self.initial_product.get("image", "")
        if img:
            self.img_path_entry.insert(0, str(img))
            self._update_preview(str(img))

    def _browse_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*")]
        chosen = filedialog.askopenfilename(parent=self, title="Select Product Image", filetypes=filetypes)
        if chosen:
            self.selected_image_path = chosen
            self.img_path_entry.delete(0, "end")
            self.img_path_entry.insert(0, chosen)
            self._update_preview(chosen)

    def _update_preview(self, img_path: str):
        resolved_path = None
        if self.get_image_path_fn:
            resolved_path = self.get_image_path_fn(img_path)
        elif os.path.exists(img_path):
            resolved_path = img_path

        if resolved_path and os.path.exists(resolved_path):
            try:
                pil_img = Image.open(resolved_path)
                pil_img.thumbnail((140, 95))
                ctk_img = ctk.CTkImage(light_image=pil_img, size=pil_img.size)
                self.preview_label.configure(image=ctk_img, text="")
                self.preview_label.image = ctk_img
                return
            except Exception:
                pass

        self.preview_label.configure(image=None, text="Image preview unavailable")

    def _handle_save(self):
        name = self.name_entry.get().strip()
        category = self.category_var.get().strip()
        price_str = self.price_entry.get().strip()
        description = self.desc_entry.get().strip()
        image_path = self.img_path_entry.get().strip()

        if not name:
            messagebox.showwarning("Missing Information", "Please enter a product name.", parent=self)
            self.name_entry.focus()
            return

        try:
            price = float(price_str.replace(",", "").replace("₱", ""))
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Invalid Price", "Please enter a valid positive price.", parent=self)
            self.price_entry.focus()
            return

        saved_data = {
            "name": name,
            "category": category,
            "price": price,
            "description": description,
            "image": image_path
        }

        if self.on_save:
            self.on_save(saved_data)

        self.destroy()


class CartModal(BaseModal):
    """Dedicated shopping cart modal dialog."""

    def __init__(self, parent, cart: Cart, on_checkout: Callable[[], None],
                 get_image_path_fn: Optional[Callable[[str], Optional[str]]] = None):
        super().__init__(parent, title="Shopping Cart", width=720, height=580, min_w=550, min_h=400)

        self.cart = cart
        self.on_checkout = on_checkout
        self.get_image_path_fn = get_image_path_fn

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # 1. Header (54px)
        header = ctk.CTkFrame(self, height=54, fg_color=Theme.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="SHOPPING CART",
            font=Theme.font(18, "bold"),
            text_color=Theme.WHITE
        ).pack(side="left", padx=20)

        self.item_count_label = ctk.CTkLabel(
            header,
            text=f"{self.cart.total_items} items",
            font=Theme.font(12),
            text_color=Theme.PRIMARY_LIGHT
        )
        self.item_count_label.pack(side="right", padx=20)

        # 2. Footer (68px)
        footer = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, height=68)
        footer.pack(side="bottom", fill="x", padx=16, pady=12)

        self.grand_total_label = ctk.CTkLabel(
            footer,
            text="Grand Total: ₱0.00",
            font=Theme.font(18, "bold"),
            text_color=Theme.DARK
        )
        self.grand_total_label.pack(side="left", padx=16)

        ctk.CTkButton(
            footer,
            text="Proceed to Checkout",
            width=175,
            height=42,
            corner_radius=8,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(12, "bold"),
            command=self._proceed_checkout
        ).pack(side="right", padx=12, pady=12)

        ctk.CTkButton(
            footer,
            text="Close",
            width=86,
            height=42,
            corner_radius=8,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=Theme.DARK,
            font=Theme.font(12, "bold"),
            command=self.destroy
        ).pack(side="right", padx=(0, 6), pady=12)

        # 3. Items scrollable list
        self.items_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.items_container.pack(fill="both", expand=True, padx=16, pady=(12, 0))

    def refresh(self):
        for w in self.items_container.winfo_children():
            w.destroy()

        if len(self.cart) == 0:
            ctk.CTkLabel(
                self.items_container,
                text="Your shopping cart is empty.",
                font=Theme.font(15, "bold"),
                text_color=Theme.GRAY
            ).pack(pady=60)
            self.grand_total_label.configure(text="Grand Total: ₱0.00")
            self.item_count_label.configure(text="0 items")
            return

        self.grand_total_label.configure(text=f"Grand Total: {self.cart.formatted_total}")
        self.item_count_label.configure(text=f"{self.cart.total_items} items")

        for idx, item in enumerate(self.cart.items):
            row = ctk.CTkFrame(self.items_container, fg_color=Theme.CARD_BG, corner_radius=8,
                               border_width=1, border_color=Theme.BORDER)
            row.pack(fill="x", pady=4)

            # Details
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=12, pady=8)

            ctk.CTkLabel(
                info,
                text=item.product.name,
                font=Theme.font(13, "bold"),
                text_color=Theme.DARK,
                anchor="w"
            ).pack(fill="x")

            ctk.CTkLabel(
                info,
                text=f"{item.product.formatted_price} each",
                font=Theme.font(11),
                text_color=Theme.GRAY,
                anchor="w"
            ).pack(fill="x")

            # Quantity controls
            qty_frame = ctk.CTkFrame(row, fg_color="transparent")
            qty_frame.pack(side="right", padx=12, pady=8)

            ctk.CTkButton(
                qty_frame,
                text="-",
                width=32,
                height=32,
                corner_radius=6,
                fg_color="#E5E7EB",
                hover_color="#D1D5DB",
                text_color=Theme.DARK,
                font=Theme.font(14, "bold"),
                command=lambda i=idx: self._change_qty(i, -1)
            ).pack(side="left", padx=2)

            ctk.CTkLabel(
                qty_frame,
                text=str(item.quantity),
                width=34,
                font=Theme.font(13, "bold"),
                text_color=Theme.DARK
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                qty_frame,
                text="+",
                width=32,
                height=32,
                corner_radius=6,
                fg_color="#E5E7EB",
                hover_color="#D1D5DB",
                text_color=Theme.DARK,
                font=Theme.font(14, "bold"),
                command=lambda i=idx: self._change_qty(i, 1)
            ).pack(side="left", padx=2)

            # Subtotal
            ctk.CTkLabel(
                qty_frame,
                text=item.formatted_subtotal,
                width=100,
                font=Theme.font(14, "bold"),
                text_color=Theme.PRIMARY,
                anchor="e"
            ).pack(side="left", padx=(10, 8))

            # Delete button
            ctk.CTkButton(
                qty_frame,
                text="✕",
                width=32,
                height=32,
                corner_radius=6,
                fg_color="#FEE2E2",
                hover_color="#FCA5A5",
                text_color=Theme.DANGER,
                font=Theme.font(12, "bold"),
                command=lambda i=idx: self._remove_item(i)
            ).pack(side="left")

    def _change_qty(self, index: int, delta: int):
        self.cart.change_quantity(index, delta)
        self.refresh()

    def _remove_item(self, index: int):
        self.cart.remove(index)
        self.refresh()

    def _proceed_checkout(self):
        if len(self.cart) == 0:
            messagebox.showinfo("Empty Cart", "Your cart is empty.", parent=self)
            return
        self.destroy()
        self.on_checkout()


class PaymentModal(BaseModal):
    """Payment settlement dialog with change calculator."""

    def __init__(self, parent, items: List[Any], total: float,
                 on_success: Callable[[List[Any], float, float, float, str], None]):
        super().__init__(parent, title="Payment", width=480, height=520, min_w=420, min_h=400)

        self.items = items
        self.total = float(total)
        self.on_success = on_success
        self.payment_method_var = ctk.StringVar(value="Cash")

        self._build_ui()

    def _build_ui(self):
        # 1. Header (52px)
        header = ctk.CTkFrame(self, height=52, fg_color=Theme.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="PAYMENT & CHECKOUT",
            font=Theme.font(17, "bold"),
            text_color=Theme.WHITE
        ).pack(expand=True)

        # 2. Docked Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 14))

        ctk.CTkButton(
            btn_frame,
            text="CONFIRM PAYMENT",
            height=44,
            corner_radius=8,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(13, "bold"),
            command=self._confirm_payment
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            height=40,
            corner_radius=8,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color=Theme.DARK,
            font=Theme.font(12, "bold"),
            command=self.destroy
        ).pack(fill="x")

        # 3. Scrollable Content
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=(10, 6))

        # Order Summary Box
        summary = ctk.CTkFrame(scroll, fg_color=Theme.CARD_BG, corner_radius=10,
                               border_width=1, border_color=Theme.BORDER)
        summary.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            summary,
            text="Order Summary",
            font=Theme.font(13, "bold"),
            text_color=Theme.DARK
        ).pack(anchor="w", padx=14, pady=(10, 6))

        for itm in self.items:
            prod_name = itm["product"]["name"] if isinstance(itm, dict) else itm.product.name
            prod_price = itm["product"]["price"] if isinstance(itm, dict) else itm.product.price
            qty = itm["quantity"] if isinstance(itm, dict) else itm.quantity
            subtotal = prod_price * qty

            row_lbl = ctk.CTkFrame(summary, fg_color="transparent")
            row_lbl.pack(fill="x", padx=14, pady=3)

            ctk.CTkLabel(row_lbl, text=f"{prod_name} × {qty}", font=Theme.font(11),
                         text_color=Theme.DARK, anchor="w").pack(side="left")
            ctk.CTkLabel(row_lbl, text=f"₱{subtotal:,.2f}", font=Theme.font(11, "bold"),
                         text_color=Theme.DARK, anchor="e").pack(side="right")

        # Total Due
        total_frame = ctk.CTkFrame(summary, fg_color=Theme.PRIMARY_LIGHT, corner_radius=6)
        total_frame.pack(fill="x", padx=14, pady=10)

        ctk.CTkLabel(
            total_frame,
            text="TOTAL DUE",
            font=Theme.font(13, "bold"),
            text_color=Theme.PRIMARY_DARK
        ).pack(side="left", padx=12, pady=10)

        ctk.CTkLabel(
            total_frame,
            text=f"₱{self.total:,.2f}",
            font=Theme.font(20, "bold"),
            text_color=Theme.PRIMARY
        ).pack(side="right", padx=12, pady=10)

        # Cash Received
        ctk.CTkLabel(
            scroll,
            text="Amount Received *",
            font=Theme.font(12, "bold"),
            text_color=Theme.DARK
        ).pack(anchor="w", padx=4, pady=(4, 4))

        self.cash_entry = ctk.CTkEntry(
            scroll,
            height=44,
            placeholder_text="Enter cash given by customer...",
            font=Theme.font(14, "bold"),
            border_color=Theme.BORDER
        )
        self.cash_entry.pack(fill="x", pady=(0, 8))
        self.cash_entry.bind("<KeyRelease>", self._calculate_change)

        # Quick cash buttons
        quick_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        quick_frame.pack(fill="x", pady=(0, 10))

        quick_amounts = [self.total, 500, 1000, 2000]
        for amt in quick_amounts:
            label = "Exact" if amt == self.total else f"₱{int(amt)}"
            ctk.CTkButton(
                quick_frame,
                text=label,
                width=72,
                height=32,
                corner_radius=6,
                fg_color=Theme.WHITE,
                hover_color=Theme.PRIMARY_LIGHT,
                text_color=Theme.PRIMARY,
                border_width=1,
                border_color=Theme.BORDER,
                font=Theme.font(11, "bold"),
                command=lambda a=amt: self._set_quick_cash(a)
            ).pack(side="left", padx=3)

        # Change display
        self.change_label = ctk.CTkLabel(
            scroll,
            text="Change: ₱0.00",
            font=Theme.font(20, "bold"),
            text_color=Theme.PRIMARY
        )
        self.change_label.pack(pady=(4, 10))

        self.cash_entry.focus()

    def _set_quick_cash(self, amount: float):
        self.cash_entry.delete(0, "end")
        self.cash_entry.insert(0, str(int(amount) if float(amount).is_integer() else amount))
        self._calculate_change()

    def _calculate_change(self, event=None):
        val = self.cash_entry.get().strip().replace(",", "").replace("₱", "")
        if not val:
            self.change_label.configure(text="Change: ₱0.00", text_color=Theme.PRIMARY)
            return

        try:
            cash = float(val)
            if cash < self.total:
                shortage = self.total - cash
                self.change_label.configure(
                    text=f"Insufficient: ₱{shortage:,.2f} more needed",
                    text_color=Theme.DANGER
                )
            else:
                change = cash - self.total
                self.change_label.configure(
                    text=f"Change: ₱{change:,.2f}",
                    text_color=Theme.SUCCESS
                )
        except ValueError:
            self.change_label.configure(text="Please enter a valid amount", text_color=Theme.DANGER)

    def _confirm_payment(self):
        val = self.cash_entry.get().strip().replace(",", "").replace("₱", "")
        try:
            cash = float(val)
        except ValueError:
            messagebox.showwarning("Invalid Amount", "Please enter the cash received.", parent=self)
            self.cash_entry.focus()
            return

        if cash < self.total:
            shortage = self.total - cash
            messagebox.showwarning(
                "Insufficient Cash",
                f"Total due is ₱{self.total:,.2f}.\nReceived ₱{cash:,.2f}.\n₱{shortage:,.2f} more needed.",
                parent=self
            )
            return

        change = cash - self.total
        confirmed = messagebox.askyesno(
            "Confirm Checkout",
            f"Total Due: ₱{self.total:,.2f}\nCash Received: ₱{cash:,.2f}\nChange: ₱{change:,.2f}\n\nComplete transaction?",
            parent=self
        )

        if not confirmed:
            return

        method = self.payment_method_var.get()
        if self.on_success:
            self.on_success(self.items, self.total, cash, change, method)

        messagebox.showinfo(
            "Payment Successful",
            f"Transaction completed!\n\nTotal: ₱{self.total:,.2f}\nCash: ₱{cash:,.2f}\nChange: ₱{change:,.2f}",
            parent=self
        )
        self.destroy()
