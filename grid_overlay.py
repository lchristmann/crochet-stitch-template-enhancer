from PIL import Image, ImageDraw
import cv2
import numpy as np
import sys
import os

# -------------------------
# Input / Output
# -------------------------
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python grid_overlay.py <input_image> [output_image]")
    sys.exit(1)

input_file = sys.argv[1]

# If output not provided, create one automatically
if len(sys.argv) == 3:
    output_file = sys.argv[2]
else:
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join("/output", f"{base_name}.png")

# -------------------------
# Load image and preprocess
# -------------------------
img = cv2.imread(input_file)
if img is None:
    print(f"Failed to read {input_file}")
    sys.exit(1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# -------------------------
# Adaptive edge detection
# -------------------------
median_val = np.median(blurred)
lower = int(max(0, 0.7 * median_val))
upper = int(min(255, 1.3 * median_val))
edges = cv2.Canny(blurred, lower, upper)

# -------------------------
# Detect horizontal and vertical lines
# -------------------------
kernels_h = [cv2.getStructuringElement(cv2.MORPH_RECT, (k, 1)) for k in [25, 15, 10]]
kernels_v = [cv2.getStructuringElement(cv2.MORPH_RECT, (1, k)) for k in [25, 15, 10]]

def extract_lines(edges, kernels):
    lines = np.zeros_like(edges)
    for k in kernels:
        lines = cv2.bitwise_or(lines, cv2.morphologyEx(edges, cv2.MORPH_OPEN, k))
    return lines

h_lines = extract_lines(edges, kernels_h)
v_lines = extract_lines(edges, kernels_v)

# Slight 1px dilation to connect broken segments
h_lines = cv2.dilate(h_lines, np.ones((1, 2), np.uint8), iterations=1)
v_lines = cv2.dilate(v_lines, np.ones((2, 1), np.uint8), iterations=1)

# -------------------------
# Merge nearby positions to avoid duplicate lines
# -------------------------
def merge_positions(positions, max_gap=2):
    """Merge positions closer than max_gap into a single line (center)."""
    if len(positions) == 0:
        return []
    merged = []
    cluster = [positions[0]]
    for p in positions[1:]:
        if p - cluster[-1] <= max_gap:
            cluster.append(p)
        else:
            merged.append(int(np.mean(cluster)))
            cluster = [p]
    merged.append(int(np.mean(cluster)))
    return merged

hor_positions = merge_positions(np.where(np.sum(h_lines, axis=1) > 0)[0])
ver_positions = merge_positions(np.where(np.sum(v_lines, axis=0) > 0)[0])

# -------------------------
# Draw overlay
# -------------------------
pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
overlay = Image.new("RGBA", pil_img.size, (255, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

line_color = (0, 0, 255, 255)  # Blue

# Draw horizontal lines
for y in hor_positions:
    draw.line([(0, y), (pil_img.width, y)], fill=line_color, width=1)

# Draw vertical lines
for x in ver_positions:
    draw.line([(x, 0), (x, pil_img.height)], fill=line_color, width=1)

# Composite overlay on original image
result = Image.alpha_composite(pil_img.convert("RGBA"), overlay)

result.save(output_file)
print(f"Enhanced grid saved to {output_file}")
