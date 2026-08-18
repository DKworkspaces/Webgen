import cv2
import numpy as np
import random
import os
import sys

def asymmetrical_random_scramble(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Error: Could not read image {image_path}")
        return False

    # Extract base structural sub-grids (a, b, c, d)
    a = img[0::2, 0::2].astype(np.float32)
    b = img[0::2, 1::2].astype(np.float32)
    c = img[1::2, 0::2].astype(np.float32)
    d = img[1::2, 1::2].astype(np.float32)

    h, w, ch = a.shape

    # Compute asymmetric one-sided averages: (a + a + b) / 2 -> a + (b * 0.5)
    asym_ab = a + (b * 0.5)
    asym_bc = b + (c * 0.5)
    asym_cd = c + (d * 0.5)
    asym_da = d + (a * 0.5)

    max_slots = 7
    canvas = np.zeros((h, w * max_slots, ch), dtype=np.float32)

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

    # Restore original spatial dimensions and aspect ratio
    final_resized = cv2.resize(canvas, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    final_output = np.clip(final_resized, 0, 255).astype(np.uint8)
    
    # Save directly as WebP to compress and destroy metadata
    success = cv2.imwrite(output_path, final_output, [cv2.IMWRITE_WEBP_QUALITY, 95])
    if success:
        print(f"🎉 Core matrix processed successfully -> {output_path}")
        return True
    return False

if __name__ == "__main__":
    # Scramble all images inside the 'input_images' folder
    input_folder = "ipimages"
    output_folder = "opimages"
    
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    valid_exts = ('.png', '.jpg', '.jpeg')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_exts)]
    
    if not images:
        print("ℹ️ No images found in 'input_images' folder.")
        sys.exit(0)
        
    for img_name in images:
        in_path = os.path.join(input_folder, img_name)
        base_name = os.path.splitext(img_name)[0]
        out_path = os.path.join(output_folder, f"{base_name}_humanized.webp")
        asymmetrical_random_scramble(in_path, out_path)
    
