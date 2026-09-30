"""Inventory management view for Aztech POS & Inventory."""
import os
import shutil
from typing import List, Dict, Any, Optional, Callable
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from frontend.theme import Theme
from frontend.modals import ProductFormModal


class Inventory(ctk.CTkFrame):
    """Inventory table view with search, filter, Add/Edit/Delete capabilities."""

    def __init__(self, parent, products: List[Any], refresh_callback: Optional[Callable[[], None]] = None):
        super().__init__(parent, fg_color=Theme.BG, corner_radius=0)

        self.parent = parent
        self.products = products
        self.refresh_callback = refresh_callback

        self.search_text = ""
        self.checkbox_vars = {}
        self.select_all_var = ctk.BooleanVar(value=False)

        self.pack(fill="both", expand=True)
        self._build_ui()
        self.refresh_table()

    # ==========================================================
    # IMAGE UTILS
    # ==========================================================

    def get_images_folder(self) -> str:
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
        os.makedirs(folder, exist_ok=True)
        return folder

    def resolve_image_path(self, img_path: str) -> Optional[str]:
        if not img_path:
            return None
        if os.path.isabs(img_path) and os.path.exists(img_path):
            return img_path
        if os.path.exists(img_path):
            return os.path.abspath(img_path)

        # Check PC-Hub folder
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate = os.path.join(project_folder, img_path)
        if os.path.exists(candidate):
            return candidate

        # Check frontend/images
        cand2 = os.path.join(self.get_images_folder(), os.path.basename(img_path))
        if os.path.exists(cand2):
            return cand2

        return None

    def _persist_image_if_needed(self, source_path: str, product_name: str) -> str:
        if not source_path:
            return ""
        resolved = self.resolve_image_path(source_path)
        if resolved and os.path.exists(resolved):
            return source_path

        if os.path.exists(source_path):
            try:
                images_dir = self.get_images_folder()
                ext = os.path.splitext(source_path)[1]
                safe_name = "".join(c for c in product_name if c.isalnum() or c in ("-", "_")).lower()
                dest_filename = f"{safe_name}{ext}"
                dest_path = os.path.join(images_dir, dest_filename)
                shutil.copy2(source_path, dest_path)
                return os.path.join("frontend", "images", dest_filename)
            except Exception:
                return source_path
        return source_path

    # ==========================================================
    # UI CONSTRUCTION
    # ==========================================================

    def _build_ui(self):
        main = ctk.CTkFrame(self, fg_color=Theme.BG, corner_radius=0)
        main.pack(fill="both", expand=True, padx=16, pady=16)

        # 1. Docked Action Bar at bottom (62px)
        action_bar = ctk.CTkFrame(main, fg_color=Theme.CARD_BG, corner_radius=10,
                                  border_width=1, border_color=Theme.BORDER, height=62)
        action_bar.pack(side="bottom", fill="x", pady=(12, 0))
        action_bar.pack_propagate(False)

        ctk.CTkButton(
            action_bar,
            text="+ Add Product",
            width=150,
            height=42,
            corner_radius=8,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(12, "bold"),
            command=self.add_product
        ).pack(side="left", padx=16, pady=10)

        ctk.CTkButton(
            action_bar,
            text="Delete Selected",
            width=140,
            height=42,
            corner_radius=8,
            fg_color="#FEE2E2",
            hover_color="#FCA5A5",
            text_color=Theme.DANGER,
            font=Theme.font(12, "bold"),
            command=self.delete_selected
        ).pack(side="left", padx=6, pady=10)

        self.item_count_label = ctk.CTkLabel(
            action_bar,
            text=f"Total: {len(self.products)} products",
            font=Theme.font(12),
            text_color=Theme.GRAY
        )
        self.item_count_label.pack(side="right", padx=16)

        # 2. Top Header & Search
        top_bar = ctk.CTkFrame(main, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            top_bar,
            text="Inventory Management",
            font=Theme.font(22, "bold"),
            text_color=Theme.DARK
        ).pack(side="left")

        search_box = ctk.CTkFrame(top_bar, fg_color=Theme.CARD_BG, corner_radius=8,
                                  border_width=1, border_color=Theme.BORDER)
        search_box.pack(side="right")

        self.search_entry = ctk.CTkEntry(
            search_box,
            placeholder_text="Search inventory...",
            width=280,
            height=38,
            border_width=0,
            font=Theme.font(12)
        )
        self.search_entry.pack(side="left", padx=(10, 4), pady=2)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        ctk.CTkButton(
            search_box,
            text="Clear",
            width=54,
            height=32,
            corner_radius=6,
            fg_color="transparent",
            text_color=Theme.GRAY,
            hover_color=Theme.BG,
            font=Theme.font(11),
            command=self._clear_search
        ).pack(side="right", padx=4)

        # 3. Two-Column Inventory Container
        table_panel = ctk.CTkFrame(main, fg_color=Theme.CARD_BG, corner_radius=10,
                                   border_width=1, border_color=Theme.BORDER)
        table_panel.pack(fill="both", expand=True)

        # Sub-header toolbar (Select All + Live Item Count)
        toolbar = ctk.CTkFrame(table_panel, fg_color=Theme.PRIMARY_LIGHT, corner_radius=8, height=44)
        toolbar.pack(fill="x", padx=8, pady=8)
        toolbar.pack_propagate(False)

        ctk.CTkCheckBox(
            toolbar,
            text="Select All Products",
            variable=self.select_all_var,
            font=Theme.font(12, "bold"),
            text_color=Theme.DARK,
            command=self._toggle_select_all
        ).pack(side="left", padx=14)

        self.table_status_label = ctk.CTkLabel(
            toolbar,
            text=f"Total: {len(self.products)} products",
            font=Theme.font(12, "bold"),
            text_color=Theme.PRIMARY_DARK
        )
        self.table_status_label.pack(side="right", padx=14)

        # Two-Column Cards Scrollable Frame
        self.rows_container = ctk.CTkScrollableFrame(table_panel, fg_color="transparent")
        self.rows_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.rows_container.grid_columnconfigure(0, weight=1, uniform="inv_col")
        self.rows_container.grid_columnconfigure(1, weight=1, uniform="inv_col")

    # ==========================================================
    # DATA & TABLE OPERATIONS
    # ==========================================================

    def _get_filtered_products(self) -> List[tuple]:
        q = self.search_text.lower().strip()
        result = []
        for idx, p in enumerate(self.products):
            name = str(p.get("name", "")).lower()
            cat = str(p.get("category", "")).lower()
            desc = str(p.get("description", "")).lower()
            if not q or (q in name or q in cat or q in desc):
                result.append((idx, p))
        return result

    def refresh_table(self):
        for w in self.rows_container.winfo_children():
            w.destroy()

        self.checkbox_vars.clear()
        filtered = self._get_filtered_products()
        count_text = f"Showing {len(filtered)} of {len(self.products)} products"
        self.item_count_label.configure(text=count_text)
        if hasattr(self, "table_status_label"):
            self.table_status_label.configure(text=count_text)

        if not filtered:
            ctk.CTkLabel(
                self.rows_container,
                text="No products match your search.",
                font=Theme.font(15, "bold"),
                text_color=Theme.GRAY
            ).pack(pady=40)
            return

        for card_idx, (original_idx, product) in enumerate(filtered):
            self._create_card(card_idx, original_idx, product)

    def _create_card(self, card_idx: int, index: int, product: Any):
        row = card_idx // 2
        col = card_idx % 2

        card = ctk.CTkFrame(
            self.rows_container,
            fg_color=Theme.WHITE,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER,
            height=98
        )
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        card.pack_propagate(False)

        # Checkbox & Thumbnail on left
        card_left = ctk.CTkFrame(card, fg_color="transparent")
        card_left.pack(side="left", fill="y", padx=(10, 8), pady=8)

        var = ctk.BooleanVar(value=False)
        self.checkbox_vars[index] = var
        ctk.CTkCheckBox(card_left, text="", variable=var, width=22).pack(side="left", padx=(0, 6))

        thumb_frame = ctk.CTkFrame(card_left, width=54, height=54, fg_color=Theme.IMAGE_GRAY, corner_radius=8)
        thumb_frame.pack(side="left")
        thumb_frame.pack_propagate(False)

        img_lbl = ctk.CTkLabel(thumb_frame, text="📦", font=Theme.font(18))
        img_lbl.place(relx=0.5, rely=0.5, anchor="center")

        img_path = self.resolve_image_path(product.get("image", ""))
        if img_path and os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                pil_img.thumbnail((50, 50))
                ctk_img = ctk.CTkImage(light_image=pil_img, size=pil_img.size)
                img_lbl.configure(image=ctk_img, text="")
                img_lbl.image = ctk_img
            except Exception:
                pass

        # Action buttons on right
        card_right = ctk.CTkFrame(card, fg_color="transparent")
        card_right.pack(side="right", fill="y", padx=(6, 12), pady=8)

        btn_box = ctk.CTkFrame(card_right, fg_color="transparent")
        btn_box.pack(expand=True)

        ctk.CTkButton(
            btn_box,
            text="Edit",
            width=54,
            height=32,
            corner_radius=6,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK,
            font=Theme.font(11, "bold"),
            command=lambda idx=index: self.update_product(idx)
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_box,
            text="✕",
            width=32,
            height=32,
            corner_radius=6,
            fg_color="#FEE2E2",
            hover_color="#FCA5A5",
            text_color=Theme.DANGER,
            font=Theme.font(11, "bold"),
            command=lambda idx=index: self.delete_product(idx)
        ).pack(side="left")

        # Center product info
        card_center = ctk.CTkFrame(card, fg_color="transparent")
        card_center.pack(side="left", fill="both", expand=True, padx=4, pady=8)

        # Name
        name_str = str(product.get("name", ""))
        ctk.CTkLabel(
            card_center,
            text=name_str,
            font=Theme.font(13, "bold"),
            text_color=Theme.DARK,
            anchor="w"
        ).pack(fill="x", anchor="w")

        # Category Badge & Price Row
        meta_row = ctk.CTkFrame(card_center, fg_color="transparent")
        meta_row.pack(fill="x", anchor="w", pady=(3, 2))

        cat_badge = ctk.CTkFrame(meta_row, fg_color=Theme.PRIMARY_LIGHT, corner_radius=10, height=22)
        cat_badge.pack(side="left", padx=(0, 8))
        cat_badge.pack_propagate(False)

        ctk.CTkLabel(
            cat_badge,
            text=str(product.get("category", "")),
            font=Theme.font(10, "bold"),
            text_color=Theme.PRIMARY
        ).place(relx=0.5, rely=0.5, anchor="center")

        price_val = float(product.get("price", 0))
        ctk.CTkLabel(
            meta_row,
            text=f"₱{price_val:,.2f}",
            font=Theme.font(13, "bold"),
            text_color=Theme.PRIMARY_DARK,
            anchor="w"
        ).pack(side="left")

        # Description
        desc_str = str(product.get("description", ""))
        if len(desc_str) > 48:
            desc_str = desc_str[:45] + "..."
        ctk.CTkLabel(
            card_center,
            text=desc_str,
            font=Theme.font(11),
            text_color=Theme.GRAY,
            anchor="w"
        ).pack(fill="x", anchor="w")

    def _create_row(self, index: int, product: Any):
        """Backward-compatible alias for creating an inventory card."""
        self._create_card(len(self.checkbox_vars), index, product)

    # ==========================================================
    # HANDLERS
    # ==========================================================

    def _on_search(self, event=None):
        self.search_text = self.search_entry.get()
        self.refresh_table()

    def _clear_search(self):
        self.search_entry.delete(0, "end")
        self.search_text = ""
        self.refresh_table()

    def _toggle_select_all(self):
        val = self.select_all_var.get()
        for v in self.checkbox_vars.values():
            v.set(val)

    def add_product(self):
        ProductFormModal(
            self,
            mode="add",
            on_save=self._on_product_added,
            get_image_path_fn=self.resolve_image_path
        )

    def _on_product_added(self, prod_data: Dict[str, Any]):
        prod_data["image"] = self._persist_image_if_needed(prod_data.get("image", ""), prod_data["name"])
        self.products.append(prod_data)
        self.refresh_table()
        if self.refresh_callback:
            self.refresh_callback()
        messagebox.showinfo("Success", f"Product '{prod_data['name']}' added successfully!", parent=self)

    def update_product(self, index: int):
        if 0 <= index < len(self.products):
            ProductFormModal(
                self,
                mode="edit",
                product=self.products[index],
                on_save=lambda p: self._on_product_updated(index, p),
                get_image_path_fn=self.resolve_image_path
            )

    def _on_product_updated(self, index: int, prod_data: Dict[str, Any]):
        prod_data["image"] = self._persist_image_if_needed(prod_data.get("image", ""), prod_data["name"])
        self.products[index] = prod_data
        self.refresh_table()
        if self.refresh_callback:
            self.refresh_callback()
        messagebox.showinfo("Success", f"Product '{prod_data['name']}' updated successfully!", parent=self)

    def delete_product(self, index: int):
        if 0 <= index < len(self.products):
            name = self.products[index].get("name", "this product")
            confirmed = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete '{name}'?",
                parent=self
            )
            if confirmed:
                self.products.pop(index)
                self.refresh_table()
                if self.refresh_callback:
                    self.refresh_callback()

    def delete_selected(self):
        selected_indices = [idx for idx, var in self.checkbox_vars.items() if var.get()]
        if not selected_indices:
            messagebox.showinfo("None Selected", "No products selected for deletion.", parent=self)
            return

        confirmed = messagebox.askyesno(
            "Confirm Bulk Deletion",
            f"Are you sure you want to delete {len(selected_indices)} selected products?",
            parent=self
        )
        if confirmed:
            for idx in sorted(selected_indices, reverse=True):
                if 0 <= idx < len(self.products):
                    self.products.pop(idx)

            self.select_all_var.set(False)
            self.refresh_table()
            if self.refresh_callback:
                self.refresh_callback()
            messagebox.showinfo("Deleted", f"Deleted {len(selected_indices)} products.", parent=self)