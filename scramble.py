import cv2
import numpy as np
import random
import os
import sys

# Target WebP Quality (85-90 triggers optimal structural compression)
COMPRESSION_QUALITY = 79

def deep_strip_and_scramble(image_path, output_path, quality_setting):
    """
    Extracts raw pixels, drops the file wrapper, strips ALL metadata headers 
    (EXIF, C2PA, XMP), scrambles the lattice, and builds a brand-new file.
    """
    # 1. Read ONLY the raw pixel matrix data into memory
    # cv2.imread inherently discards all metadata containers (EXIF, C2PA, etc.)
    # It loads nothing but a pure, raw NumPy array of values (Height, Width, Channels)
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Error: Could not read image {image_path}")
        return False

    # 2. Extract base structural sub-grids (a, b, c, d)
    a = img[0::2, 0::2].astype(np.float32)
    b = img[0::2, 1::2].astype(np.float32)
    c = img[1::2, 0::2].astype(np.float32)
    d = img[1::2, 1::2].astype(np.float32)

    h, w, ch = a.shape

    # 3. Compute asymmetric one-sided averages: a + (b * 0.5)
    asym_ab = a + (b * 0.5)
    asym_bc = b + (c * 0.5)
    asym_cd = c + (d * 0.5)
    asym_da = d + (a * 0.5)

    max_slots = 7
    canvas = np.zeros((h, w * max_slots, ch), dtype=np.float32)

    # 4. Apply randomized matrix sequence selection per row block
    for y in range(h):
        seq_choice = random.choice([1, 2, 3])
        
        if seq_choice == 1:
            row_data = np.concatenate([a[y], asym_ab[y], b[y], asym_bc[y], c[y], asym_cd[y], d[y]], axis=1)
            canvas[y, :row_data.shape[1]] = row_data
        elif seq_choice == 2:
            row_data = np.concatenate([a[y], asym_ab[y], b[y], c[y], asym_cd[y], d[y]], axis=1)
            canvas[y, :row_data.shape[1]] = row_data
        elif seq_choice == 3:
            row_data = np.concatenate([a[y], b[y], asym_bc[y], c[y], d[y]], axis=1)
            canvas[y, :row_data.shape[1]] = row_data

    # 5. Restore native spatial dimensions
    final_resized = cv2.resize(canvas, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    final_output = np.clip(final_resized, 0, 255).astype(np.uint8)
    
    # 6. Instantiate a completely new file container
    # Writing to a new path via cv2 creates completely sterile, fresh WebP headers
    # Any original C2PA Manifests or EXIF packets are fundamentally gone
    success = cv2.imwrite(output_path, final_output, [int(cv2.IMWRITE_WEBP_QUALITY), quality_setting])
    if success:
        print(f"🔒 Sterile File Built Successfully -> {output_path}")
        return True
    return False

if __name__ == "__main__":
    input_folder = "ipimages"
    output_folder = "opimages"
    
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_exts)]
    
    if not images:
        print("ℹ️ No images found in 'input_images' folder.")
        sys.exit(0)
        
    for img_name in images:
        in_path = os.path.join(input_folder, img_name)
        base_name = os.path.splitext(img_name)[0]
        out_path = os.path.join(output_folder, f"{base_name}_humanized.webp")
        deep_strip_and_scramble(in_path, out_path, COMPRESSION_QUALITY)
    
