# brandnbloom/ai_tools/color_extractor.py
from io import BytesIO
from typing import List
from PIL import Image
import numpy as np

try:
    from sklearn.cluster import KMeans
except Exception:
    KMeans = None  # optional dependency; fallback below


def _rgb_to_hex(rgb):
    r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
    return f"#{r:02X}{g:02X}{b:02X}"


def extract_dominant_colors(img_bytes: bytes, num_colors: int = 5) -> List[str]:
    """
    Extract dominant colors from image bytes. Returns hex codes.
    Uses KMeans if available; otherwise returns a simple histogram-based palette.
    """
    image = Image.open(BytesIO(img_bytes)).convert("RGB")
    image = image.resize((200, 200))  # reasonable speed/quality tradeoff
    pixels = np.array(image).reshape(-1, 3)

    if KMeans is not None:
        kmeans = KMeans(n_clusters=num_colors, random_state=42)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_.astype(int)
        return [_rgb_to_hex(center) for center in centers]

    # fallback: pick top histogram colors
    pixels_tuple = [tuple(p) for p in pixels]
    unique, counts = np.unique(pixels, axis=0, return_counts=True)
    idx = np.argsort(counts)[-num_colors:][::-1]
    return [_rgb_to_hex(unique[i]) for i in idx]
