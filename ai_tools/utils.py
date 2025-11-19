# brandnbloom/ai_tools/utils.py

from typing import Dict, List, Tuple
import numpy as np


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert HEX string to RGB tuple.
    Accepts formats like "#ffffff" or "ffffff".
    """
    if not hex_color:
        raise ValueError("hex_color cannot be empty")

    h = hex_color.lstrip("#")

    if len(h) != 6 or any(c not in "0123456789abcdefABCDEF" for c in h):
        raise ValueError(f"Invalid hex color: {hex_color}")

    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def palette_luminance(hex_palette: List[str]) -> float:
    """
    Compute the average luminance (0–255) of a palette.
    Based on the standard perceived brightness formula:
    L = 0.2126R + 0.7152G + 0.0722B

    Useful for determining whether a palette is dark/light,
    or for aesthetic scoring.
    """
    if not hex_palette:
        return 0.0

    luminances = []

    for hex_color in hex_palette:
        try:
            r, g, b = hex_to_rgb(hex_color)
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            luminances.append(lum)
        except ValueError:
            # skip invalid colors instead of crashing the entire function
            continue

    return float(np.mean(luminances) if luminances else 0.0)
