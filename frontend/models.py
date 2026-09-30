"""Domain data models and catalog for Aztech POS & Inventory."""
from datetime import datetime
from typing import List, Dict, Any, Optional


class Product:
    """Represents a store product with full dict compatibility."""

    def __init__(self, name: str, category: str, price: float, description: str = "", image: str = ""):
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.price = float(price)
        self.description = str(description).strip()
        self.image = str(image).strip()

    @property
    def formatted_price(self) -> str:
        return f"₱{self.price:,.2f}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "image": self.image
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        return cls(
            name=data.get("name", ""),
            category=data.get("category", ""),
            price=float(data.get("price", 0)),
            description=data.get("description", ""),
            image=data.get("image", "")
        )

    # Dict-like compatibility for legacy code
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        if key == "price":
            value = float(value)
        setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def copy(self) -> "Product":
        return Product(self.name, self.category, self.price, self.description, self.image)

    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.category!r}, {self.price})"


class CartItem:
    """Represents a product item in the shopping cart."""

    def __init__(self, product: Any, quantity: int = 1):
        if isinstance(product, dict):
            self.product = Product.from_dict(product)
        elif isinstance(product, Product):
            self.product = product
        else:
            raise TypeError(f"Invalid product type: {type(product)}")

        self.quantity = max(1, int(quantity))

    @property
    def price(self) -> float:
        return self.product.price

    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity

    @property
    def formatted_subtotal(self) -> str:
        return f"₱{self.subtotal:,.2f}"

    # Dict-like compatibility
    def __getitem__(self, key: str) -> Any:
        if key == "product":
            return self.product.to_dict()
        if key == "quantity":
            return self.quantity
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        if key == "quantity":
            self.quantity = max(1, int(value))
        else:
            raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product": self.product.to_dict(),
            "quantity": self.quantity
        }


class Cart:
    """Encapsulates shopping cart state and operations."""

    def __init__(self):
        self.items: List[CartItem] = []

    def add(self, product: Any, quantity: int = 1) -> CartItem:
        prod_obj = product if isinstance(product, Product) else Product.from_dict(product)
        for item in self.items:
            if item.product.name == prod_obj.name:
                item.quantity += quantity
                return item
        new_item = CartItem(prod_obj, quantity)
        self.items.append(new_item)
        return new_item

    def remove(self, index: int) -> Optional[CartItem]:
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def change_quantity(self, index: int, delta: int) -> bool:
        if 0 <= index < len(self.items):
            new_qty = self.items[index].quantity + delta
            if new_qty <= 0:
                self.items.pop(index)
            else:
                self.items[index].quantity = new_qty
            return True
        return False

    def clear(self) -> None:
        self.items.clear()

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.items)

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def formatted_total(self) -> str:
        return f"₱{self.total_amount:,.2f}"

    def to_legacy_list(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self.items]

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index: int) -> CartItem:
        return self.items[index]


class SaleRecord:
    """Encapsulates a completed checkout sale transaction."""

    def __init__(self, items: List[Any], total: float, cash: float, change: float,
                 date: Optional[datetime] = None, payment_method: str = "Cash"):
        self.date = date or datetime.now()
        self.total = float(total)
        self.cash = float(cash)
        self.change = float(change)
        self.payment_method = payment_method
        self.items: List[Dict[str, Any]] = []

        for item in items:
            if isinstance(item, CartItem):
                self.items.append({
                    "name": item.product.name,
                    "category": item.product.category,
                    "price": item.product.price,
                    "quantity": item.quantity,
                })
            elif isinstance(item, dict):
                prod = item.get("product", item)
                self.items.append({
                    "name": prod.get("name", "Unknown"),
                    "category": prod.get("category", "Other"),
                    "price": float(prod.get("price", 0)),
                    "quantity": int(item.get("quantity", 1)),
                })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "items": self.items,
            "total": self.total,
            "cash": self.cash,
            "change": self.change,
            "payment_method": self.payment_method
        }

    # Dict-like compatibility
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


# Master product catalog data tuples: (name, category, price, description, image_path)
_CATALOG_DATA = [
    ("Intel Core I3 10Gen", "CPU", 5200, "Desktop Processor", "Images/I3_10Gen.jpg"),
    ("Intel Core I5 10Gen", "CPU", 8500, "Computer Processor", "Images/I5_10Gen.jpg"),
    ("Intel Core I7 13Gen", "CPU", 17500, "High Performance Processor", "Images/I7_13Gen.jpg"),
    ("Intel Core I9 12Gen", "CPU", 28500, "Enthusiast Processor", "Images/I9_12Gen.jpg"),
    ("AMD Ryzen 3 3200g", "CPU", 4800, "Desktop Processor", "Images/r3_3200g.webp"),
    ("AMD Ryzen 5 5600", "CPU", 7500, "Computer Processor", "Images/r5_5600.webp"),
    ("AMD Ryzen 7 8000", "CPU", 13800, "High Performance Processor", "Images/r7_8000.webp"),
    ("AMD Ryzen 9 9000", "CPU", 26500, "Enthusiast Processor", "Images/r9_9000.jpg"),
    ("ASUS RTX 4060", "GPU", 18500, "Graphics Card", "Images/asus_4060.webp"),
    ("MSI RTX 4060", "GPU", 19000, "Graphics Card", "Images/msi_4060.png"),
    ("Gigabyte RTX 4060", "GPU", 18800, "Graphics Card", "Images/gigabyte_4060.jpg"),
    ("MSI RTX 3060ti", "GPU", 18500, "Graphics Card", "Images/msi_3060.webp"),
    ("ASUS RTX 3050", "GPU", 13500, "Graphics Card", "Images/asus_3050.jpg"),
    ("Gigabyte GTX 1660 Super", "GPU", 10500, "Graphics Card", "Images/gigabyte_1660.jpg"),
    ("8GB DDR4 RAM 3200Mhz", "RAM", 3800, "Desktop Memory", "Images/ddr4_8gb.jpg"),
    ("16GB DDR4 RAM 3200Mhz", "RAM", 7500, "Desktop Memory", "Images/ddr4_16gb.jpg"),
    ("32GB DDR4 RAM 3200Mhz", "RAM", 14000, "High Capacity Memory", "Images/ddr4_32gb.webp"),
    ("8GB DDR5 RAM 6000Mhz", "RAM", 9500, "DDR5 Desktop Memory", "Images/ddr5_8gb.jpg"),
    ("16GB DDR5 RAM 6000Mhz", "RAM", 17500, "DDR5 Desktop Memory", "Images/ddr5_16gb.jpg"),
    ("32GB DDR5 RAM", "RAM", 35000, "High Performance DDR5", "Images/ddr5_32gb.jpg"),
    ("500GB SSD", "Storage", 2500, "Solid State Drive", "Images/ssd_500gb.png"),
    ("1TB SSD", "Storage", 4200, "Solid State Drive", "Images/ssd_1tb.png"),
    ("2TB SSD", "Storage", 7200, "High Capacity SSD", "Images/ssd_2tb.webp"),
    ("1TB HDD", "Storage", 1800, "Hard Disk Drive", "Images/hdd_500gb.jpg"),
    ("2TB HDD", "Storage", 3900, "Hard Disk Drive", "Images/hdd_2tb.jpg"),
    ("ASUS B550-F", "Motherboard", 6500, "AMD Motherboard", "Images/asusmobo_b550-f.jpg"),
    ("MSI B550", "Motherboard", 6200, "AMD Motherboard", "Images/msimobo_b550.png"),
    ("ASRock B660-Pro", "Motherboard", 6800, "Intel Motherboard", "Images/asrockmobo_b660m_pro.jpg"),
    ("Gigabyte B650 EANGLE AX", "Motherboard", 8500, "AMD AM5 Motherboard", "Images/gigamobo_b650-eangle.png"),
    ("ASUS H610", "Motherboard", 4800, "Intel Motherboard", "Images/asusmobo_h610m.png"),
    ("550W Power Supply", "PSU", 2800, "Computer Power Supply", "Images/psutuf_550w.png"),
    ("650W Power Supply", "PSU", 3500, "Computer Power Supply", "Images/psu_g650.webp"),
    ("750W Power Supply", "PSU", 4500, "Gaming Power Supply", "Images/psu_750w.webp"),
    ("850W Power Supply", "PSU", 5800, "High Performance PSU", "Images/psu_850w.jpg"),
    ("PC Case", "Other", 3000, "Computer Case", "Images/normalcase.webp"),
    ("Gaming PC Case", "Other", 4500, "RGB Gaming Case", "Images/rgbcase.jpg"),
    ("CPU Cooler", "Other", 1800, "Processor Cooler", "Images/rbgcoolercase.jpg"),
    ("120mm Case Fan", "Other", 450, "Cooling Fan", "Images/coolingfan.jpg"),
    ("ASUS Laptop", "Other", 28000, "Laptop Computer", "Images/asuslaptop.jpg"),
    ("Acer Laptop", "Other", 26000, "Laptop Computer", "Images/acerlaptop.jpg"),
    ("Huawei Laptop", "Other", 27500, "Laptop Computer", "Images/huaweilaptop.png"),
    ("22-inch Monitor", "Other", 5200, "Full HD Monitor", "Images/22ich.jpg"),
    ("24-inch Monitor", "Other", 6500, "Full HD Computer Monitor", "Images/24inch.png"),
    ("27-inch Gaming Monitor", "Other", 9500, "Gaming Monitor", "Images/27inch.jpg"),
    ("Gaming Keyboard", "Other", 1200, "USB Gaming Keyboard", "Images/keyboard.png"),
    ("Gaming Mouse", "Other", 650, "USB Gaming Mouse", "Images/mouse.png"),
    ("Gaming Headset", "Other", 1500, "Computer Headset", "Images/headset.webp"),
    ("Webcam", "Other", 1800, "USB Webcam", "Images/webcam.jpg"),
    ("USB Hub", "Other", 650, "USB Expansion Hub", "Images/usbhub.png"),
    ("Epson Printer", "Other", 8500, "Ink Tank Printer", "Images/epsonprinter.jpg"),
    ("Canon Printer", "Other", 7800, "Ink Tank Printer", "Images/canonprinter.webp"),
    ("HP Printer", "Other", 7200, "All-in-One Printer", "Images/hpprinter.png"),
    ("CCTV Camera", "Other", 1800, "Security Camera", "Images/cctv1.jpg"),
    ("CCTV 4-Camera Set", "Other", 12500, "Complete CCTV Package", "Images/cctv4.jpg"),
    ("CCTV 8-Camera Set", "Other", 19500, "Complete CCTV Package", "Images/cctv8.webp"),
    ("Pisonet PC", "Other", 18500, "Pisonet Computer Set", "Images/pisonet.jpg"),
    ("Pisonet Cabinet", "Other", 3500, "Pisonet Computer Cabinet", "Images/cabinet.jpg"),
    ("Pisonet Timer", "Other", 1200, "Pisonet Timer System", "Images/timer.jpg"),
]


def get_default_products() -> List[Dict[str, Any]]:
    """Returns the default product catalog as a list of dictionaries for full compatibility."""
    return [
        {
            "name": name,
            "category": cat,
            "price": price,
            "description": desc,
            "image": img
        }
        for name, cat, price, desc, img in _CATALOG_DATA
    ]
