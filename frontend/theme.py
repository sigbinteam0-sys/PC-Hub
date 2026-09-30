"""Theme and styling constants for Aztech POS & Inventory.

Optimized for high visibility, legible admin typography, and crisp contrast.
"""
import customtkinter as ctk


class Theme:
    # Primary Brand Colors (Aztech Blue)
    PRIMARY = "#1769D1"
    PRIMARY_DARK = "#0F4FA8"
    PRIMARY_LIGHT = "#EAF3FF"
    PRIMARY_HOVER = "#1357B2"

    # Neutrals & High-Contrast Backgrounds
    BG = "#F1F5F9"
    WHITE = "#FFFFFF"
    CARD_BG = "#FFFFFF"
    DARK = "#0F172A"       # Slate 900 for high-clarity text
    GRAY = "#475569"       # Slate 600 for sharp secondary text
    GRAY_LIGHT = "#94A3B8"
    BORDER = "#CBD5E1"     # Clean card border
    IMAGE_GRAY = "#E2E8F0"

    # Status Colors
    SUCCESS = "#16A34A"
    SUCCESS_LIGHT = "#DCFCE7"
    DANGER = "#DC2626"
    DANGER_DARK = "#B91C1C"
    WARNING = "#D97706"

    # Backward-compatible aliases
    TEAL = PRIMARY
    DARK_TEAL = PRIMARY_DARK
    LIGHT_TEAL = PRIMARY_LIGHT
    BLUE = PRIMARY
    DARK_BLUE = PRIMARY_DARK
    LIGHT_BLUE = PRIMARY_LIGHT
    RED = DANGER

    @staticmethod
    def font(size=13, weight="normal"):
        return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)
