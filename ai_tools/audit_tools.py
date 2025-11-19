"""
audit_tools.py
Utilities for brand screenshot analysis, tone detection, palette extraction,
and overall brand consistency auditing.
"""

from typing import List, Dict, Tuple
from PIL import Image
from io import BytesIO
import numpy as np
from sklearn.cluster import KMeans


# ---------------------------------------------------------
# 1. EXTRACT DOMINANT COLORS (Basic Color Clustering)
# ---------------------------------------------------------

def extract_palette(img_bytes: bytes, num_colors: int = 5) -> List[str]:
    """Extract dominant colors using k-means clustering."""
    try:
        image = Image.open(BytesIO(img_bytes)).convert("RGB")
        image = image.resize((150, 150))  # speed + good enough for palettes
        pixels = np.array(image).reshape(-1, 3)

        kmeans = KMeans(n_clusters=num_colors, random_state=42)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_.astype(int)

        hex_colors = [f"#{r:02X}{g:02X}{b:02X}" for r, g, b in centers]
        return hex_colors

    except Exception:
        # fallback palette
        return ["#8B5CF6", "#F6F5FB", "#A25A3C"]


# ---------------------------------------------------------
# 2. ESTIMATE TONE (Color Psychology Based)
# ---------------------------------------------------------

def estimate_tone(colors: List[str]) -> str:
    """
    Basic aesthetic tone estimation:
    Pastel → Calm,  
    High saturation → Energetic  
    Warm muted → Aesthetic / Cozy  
    """
    if not colors:
        return "Unknown"

    # Convert hex to RGB for simple luminance & saturation heuristics
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    rgbs = [hex_to_rgb(c) for c in colors]

    luminance = np.mean([0.2126*r + 0.7152*g + 0.0722*b for r, g, b in rgbs])
    saturation = np.mean([max(rgb) - min(rgb) for rgb in rgbs])

    if luminance > 200 and saturation < 40:
        return "Soft / Minimalist"
    if luminance > 150:
        return "Friendly / Clean"
    if saturation > 120:
        return "Energetic / Playful"
    if luminance < 70:
        return "Bold / High Contrast"
    return "Warm / Aesthetic"


# ---------------------------------------------------------
# 3. CHECK PALETTE CONSISTENCY
# ---------------------------------------------------------

def measure_brand_consistency(colors: List[str], brand_palette: List[str] = None) -> str:
    """
    Compare extracted palette with brand palette.
    """
    if not colors:
        return "Unknown"

    if not brand_palette:
        # Default aesthetic palette
        brand_palette = ["#A25A3C", "#F7F1EB", "#3C2F2F"]

    def distance(c1, c2):
        """Simple Euclidean distance between hex colors."""
        def hex_to_rgb(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        r1, g1, b1 = hex_to_rgb(c1)
        r2, g2, b2 = hex_to_rgb(c2)
        return ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)**0.5

    distances = []
    for c in colors:
        distances.append(min(distance(c, b) for b in brand_palette))

    avg_distance = np.mean(distances)

    if avg_distance < 35:
        return "Excellent"
    if avg_distance < 60:
        return "Good"
    if avg_distance < 100:
        return "Moderate"
    return "Poor"


# ---------------------------------------------------------
# 4. FULL SCREENSHOT ANALYSIS (Main Function)
# ---------------------------------------------------------

def analyze_screenshot_tone(img_bytes: bytes) -> Dict:
    """Run full brand & aesthetic tone analysis on screenshot."""
    palette = extract_palette(img_bytes, num_colors=5)
    tone = estimate_tone(palette)
    consistency = measure_brand_consistency(palette)

    return {
        "dominant_colors": palette,
        "tone": tone,
        "consistency": consistency
    }


# ---------------------------------------------------------
# 5. BASIC AUDIT REPORT (Optional)
# ---------------------------------------------------------

def generate_audit_report(img_bytes: bytes) -> Dict:
    """
    High-level summary for UI/brand audits.
    """
    result = analyze_screenshot_tone(img_bytes)

    summary = {
        "palette": result["dominant_colors"],
        "ui_tone": result["tone"],
        "brand_alignment": result["consistency"],
        "message": f"The design feels {result['tone'].lower()}, and brand consistency is {result['consistency']}."
    }

    return summary
