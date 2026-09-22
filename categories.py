import customtkinter as ctk


class Categories(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        # =========================
        # CATEGORY DATA
        # =========================

        self.categories = [
            "Accessories",
            "Components",
            "Monitors",
            "Peripherals"
        ]

        self.archived_categories = []

        # =========================
        # TITLE
        # =========================

        self.title_label = ctk.CTkLabel(
            self,
            text="Categories",
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
            text="Category Management"
        )

        self.description_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        # =========================
        # SEARCH
        # =========================
        def show_categories(self):
            self.clear_content()

            categories_page = Categories(
                self.content
            )

            categories_page.pack(
                fill="both",
                expand=True
            )

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
            placeholder_text="Search category",
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
            command=self.search_category
        )

        self.search_button.pack(
            side="right"
        )

        # =========================
        # CATEGORY LIST
        # =========================

        self.category_list = ctk.CTkScrollableFrame(
            self,
            label_text="Categories"
        )

        self.category_list.pack(
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

        # Add
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add Category",
            command=self.add_category
        )

        self.add_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        # Edit
        self.edit_button = ctk.CTkButton(
            self.button_frame,
            text="Edit Category",
            command=self.edit_category
        )

        self.edit_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        # Archive
        self.archive_button = ctk.CTkButton(
            self.button_frame,
            text="Archive",
            command=self.archive_category
        )

        self.archive_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        # Archived
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

        self.display_categories()

    # ==================================================
    # CLEAR LIST
    # ==================================================

    def clear_list(self):

        for widget in self.category_list.winfo_children():
            widget.destroy()

    # ==================================================
    # DISPLAY ACTIVE CATEGORIES
    # ==================================================

    def display_categories(self, categories=None):

        self.clear_list()

        if categories is None:
            categories = self.categories

        if not categories:

            empty_label = ctk.CTkLabel(
                self.category_list,
                text="No categories found."
            )

            empty_label.pack(
                pady=20
            )

            return

        for category in categories:

            row = ctk.CTkFrame(
                self.category_list
            )

            row.pack(
                fill="x",
                pady=3
            )

            category_label = ctk.CTkLabel(
                row,
                text=category,
                anchor="w"
            )

            category_label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=8
            )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_category(self):

        search = self.search_entry.get().strip().lower()

        if not search:
            self.display_categories()
            return

        results = [
            category
            for category in self.categories
            if search in category.lower()
        ]

        self.display_categories(results)

    # ==================================================
    # ADD CATEGORY
    # ==================================================

    def add_category(self):

        dialog = ctk.CTkInputDialog(
            text="Enter category name:",
            title="Add Category"
        )

        category = dialog.get_input()

        if not category:
            return

        category = category.strip()

        if not category:
            return

        if category in self.categories:

            print("Category already exists.")
            return

        if category in self.archived_categories:

            print(
                "Category is archived. "
                "Restore it instead."
            )

            return

        self.categories.append(category)

        self.display_categories()

        print(
            f"{category} added successfully."
        )

    # ==================================================
    # EDIT CATEGORY
    # ==================================================

    def edit_category(self):

        dialog = ctk.CTkInputDialog(
            text="Enter current category name:",
            title="Edit Category"
        )

        old_category = dialog.get_input()

        if not old_category:
            return

        old_category = old_category.strip()

        if old_category not in self.categories:

            print("Category not found.")
            return

        dialog = ctk.CTkInputDialog(
            text="Enter new category name:",
            title="Edit Category"
        )

        new_category = dialog.get_input()

        if not new_category:
            return

        new_category = new_category.strip()

        if not new_category:
            return

        if new_category in self.categories:

            print(
                "Category name already exists."
            )

            return

        index = self.categories.index(
            old_category
        )

        self.categories[index] = new_category

        self.display_categories()

        print(
            f"{old_category} changed to "
            f"{new_category}."
        )

    # ==================================================
    # ARCHIVE CATEGORY
    # ==================================================

    def archive_category(self):

        dialog = ctk.CTkInputDialog(
            text="Enter category name to archive:",
            title="Archive Category"
        )

        category = dialog.get_input()

        if not category:
            return

        category = category.strip()

        if category not in self.categories:

            print("Category not found.")
            return

        confirm = ctk.CTkInputDialog(
            text=f"Type YES to archive {category}:",
            title="Confirm Archive"
        )

        answer = confirm.get_input()

        if not answer:
            return

        if answer.strip().upper() != "YES":

            print("Archive cancelled.")
            return

        self.categories.remove(category)

        self.archived_categories.append(category)

        self.display_categories()

        print(
            f"{category} has been archived."
        )

    # ==================================================
    # SHOW ARCHIVED
    # ==================================================

    def show_archived(self):

        self.clear_list()

        if not self.archived_categories:

            empty_label = ctk.CTkLabel(
                self.category_list,
                text="No archived categories."
            )

            empty_label.pack(
                pady=20
            )

            return

        for category in self.archived_categories:

            row = ctk.CTkFrame(
                self.category_list
            )

            row.pack(
                fill="x",
                pady=3
            )

            category_label = ctk.CTkLabel(
                row,
                text=category,
                anchor="w"
            )

            category_label.pack(
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
                command=lambda c=category:
                    self.restore_category(c)
            )

            restore_button.pack(
                side="right",
                padx=10,
                pady=5
            )

    # ==================================================
    # RESTORE CATEGORY
    # ==================================================

    def restore_category(self, category):

        if category not in self.archived_categories:
            return

        self.archived_categories.remove(category)

        self.categories.append(category)

        self.display_categories()

        print(
            f"{category} has been restored."
        )