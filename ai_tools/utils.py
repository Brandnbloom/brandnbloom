# brandnbloom/ai_tools/utils.py
from typing import Dict, List
import numpy as np

def hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def palette_luminance(hex_palette: List[str]) -> float:
    """
    Return average luminance of palette (0-255 scale).
    Used for basic aesthetic heuristics.
    """
    vals = []
    for h in hex_palette:
        r, g, b = hex_to_rgb(h)
        lum = 0.2126*r + 0.7152*g + 0.0722*b
        vals.append(lum)
    return float(np.mean(vals) if vals else 0.0)
