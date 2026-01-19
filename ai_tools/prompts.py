# ai_tools/color_extractor.py

from typing import List, Tuple
from PIL import Image
import numpy as np
from collections import Counter

def extract_dominant_colors(image_path: str, n_colors: int = 5) -> List[Tuple[int, int, int]]:
    """
    Returns the top n_colors dominant colors in an image.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((100, 100))  # speed optimization
        pixels = np.array(img).reshape(-1, 3)
        counts = Counter(map(tuple, pixels))
        dominant_colors = [color for color, _ in counts.most_common(n_colors)]
        return dominant_colors
    except Exception:
        return []
