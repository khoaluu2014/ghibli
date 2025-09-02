import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import colorsys
import os

# pass in the img that we want
# TODO make it a prompt instead of hardcoded
PATH = "./img/thewindrises/"
all_pixels = []
# convert the image to RGB to ensure consistency
for filename in os.listdir(PATH):
    if filename.lower().endswith("jpg"):
        img_path = os.path.join(PATH, filename)
        try:
            img = Image.open(img_path).convert("RGB")
            # scale the image down for effciency
            img.thumbnail((100, 100))
            # flatten array of img from 3D (width, height, 3) to 2D (width * height, 3)
            pixels = np.array(img).reshape(-1, 3)
            print(f"Processed {filename}.")
            all_pixels.append(pixels)
        except Exception as e:
            print(f"Error: {e}")
# number of dominant colors we want to extract
pixels = []
if all_pixels:
    pixels = np.concatenate(all_pixels, axis=0)

N_COLORS = 12
RANDOM_STATE = 42

# Use K Means clustering on the image
kmeans = KMeans(n_clusters=N_COLORS, random_state=RANDOM_STATE, n_init="auto")
kmeans_result = kmeans.fit(pixels)
clusters = kmeans_result.cluster_centers_
dominant_colors_in_rgb = clusters.astype(int)


def adjust_color_tone(color_in_rgb, light_factor=1.0, saturate_factor=1.0):
    """Adjusts the lightness and saturation of an RGB color.

    Args:
        color_in_rgb (list): The original color as an RGB triplet, e.g., [216, 156, 124].
        light_factor (float, optional): Multiplier for lightness.
            A value > 1.0 makes it lighter, < 1.0 makes it darker. Defaults to 1.0.
        saturate_factor (float, optional): Multiplier for saturation.
            A value > 1.0 is more saturated, < 1.0 is less. Defaults to 1.0.

    Returns:
        list: The new, adjusted color as an RGB triplet.
    """
    r, g, b = color_in_rgb
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l *= light_factor
    s *= saturate_factor
    l = max(0, min(1.0, l))
    s = max(0, min(1.0, s))
    r_new, g_new, b_new = colorsys.hls_to_rgb(h, l, s)
    return [int(r_new * 255), int(g_new * 255), int(b_new * 255)]


lighter_palette = []
darker_pallete = []
for color_in_rgb in dominant_colors_in_rgb:
    lighter_color = adjust_color_tone(color_in_rgb=color_in_rgb, light_factor=1.2)
    darker_color = adjust_color_tone(color_in_rgb=color_in_rgb, light_factor=0.8)
    r_light, g_light, b_light = lighter_color
    r_dark, g_dark, b_dark = darker_color
    lighter_palette.append(f"#{r_light:02x}{g_light:02x}{b_light:02x}")
    darker_pallete.append(f"#{r_dark:02x}{g_dark:02x}{b_dark:02x}")

# Change the colors to hex
dominant_colors_in_hex = []
for r, g, b in dominant_colors_in_rgb:
    dominant_colors_in_hex.append(f"#{r:02x}{g:02x}{b:02x}")

print("Normal: ", dominant_colors_in_hex)
print("Lighter: ", lighter_palette)
print("Darker: ", darker_pallete)

# Palette:  ['#bf9979', '#545765', '#7a8d9c', '#cfbdd0', '#332b25', '#b3b3ad', '#9e8476', '#e2bf8b']
# Lighter:  ['#d3b9a3', '#646879', '#99a8b3', '#f0ebf1', '#3d332c', '#d4d4d1', '#b4a196', '#f0dfc5']
# Darker:  ['#a87950', '#434550', '#5e717f', '#ad8eae', '#28221d', '#919188', '#81685b', '#d39e50']
