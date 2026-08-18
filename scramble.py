import cv2
import numpy as np
import random
import os
import sys
import piexif

# Target WebP Quality (85-90 triggers optimal structural compression)
COMPRESSION_QUALITY = 79

def generate_fake_iphone_exif():
    """Generates a complete, authentic-looking EXIF metadata dictionary for an iPhone 15 Pro."""
    # 0th IFD (Primary Image Data)
    zeroth_ifd = {
        piexif.ImageIFD.Make: u"Apple",
        piexif.ImageIFD.Model: u"iPhone 15 Pro",
        piexif.ImageIFD.Software: u"18.1.1", # Simulated iOS Version
        piexif.ImageIFD.XResolution: (72, 1),
        piexif.ImageIFD.YResolution: (72, 1),
        piexif.ImageIFD.ResolutionUnit: 2,
    }
    
    # Exif IFD (Specific Camera/Lens Settings)
    exif_ifd = {
        piexif.ExifIFD.ExifVersion: b"0232",
        piexif.ExifIFD.ExposureTime: (1, 120),  # 1/120s shutter speed
        piexif.ExifIFD.FNumber: (18, 10),       # f/1.8 main lens aperture
        piexif.ExifIFD.ISOSpeedRatings: 64,     # Clean outdoor ISO
        piexif.ExifIFD.FocalLength: (686, 100), # 6.86mm physical phone focal length
        piexif.ExifIFD.LensMake: u"Apple",
        piexif.ExifIFD.LensModel: u"iPhone 15 Pro back triple camera 6.86mm f/1.78",
    }
    
    # Combine into standard EXIF package structure
    exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes

def deep_strip_scramble_and_fake(image_path, output_path, quality_setting, inject_fake_meta=True):
    """
    Reads raw pixels to drop original AI markers, shuffles the grid lattice,
    saves a fresh WebP container, and appends organic camera headers.
    """
    # 1. Read ONLY raw pixels (instantly dropping original C2PA/EXIF wrappers)
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
    # Allocate canvas memory: Height x (Width * 7) x Channels
    canvas = np.zeros((h, w * max_slots, ch), dtype=np.float32)

    # 4. Apply randomized matrix sequence selection per row block
    # axis=0 is used because indexing a single row a[y] leaves a 2D array of (Width, Channels)
    for y in range(h):
        seq_choice = random.choice([1, 2, 3])
        
        if seq_choice == 1:
            # Seq 1: 7 sub-images long
            row_data = np.concatenate([a[y], asym_ab[y], b[y], asym_bc[y], c[y], asym_cd[y], d[y]], axis=0)
            canvas[y, :row_data.shape[0]] = row_data
        elif seq_choice == 2:
            # Seq 2: 6 sub-images long
            row_data = np.concatenate([a[y], asym_ab[y], b[y], c[y], asym_cd[y], d[y]], axis=0)
            canvas[y, :row_data.shape[0]] = row_data
        elif seq_choice == 3:
            # Seq 3: 5 sub-images long
            row_data = np.concatenate([a[y], b[y], asym_bc[y], c[y], d[y]], axis=0)
            canvas[y, :row_data.shape[0]] = row_data

    # 5. Restore original spatial dimensions and aspect ratio
    final_resized = cv2.resize(canvas, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    final_output = np.clip(final_resized, 0, 255).astype(np.uint8)
    
    # 6. Save fresh file container with zero original headers
    success = cv2.imwrite(output_path, final_output, [int(cv2.IMWRITE_WEBP_QUALITY), quality_setting])
    
    if success:
        # 7. Inject the fake iPhone EXIF Profile into the freshly written file wrapper
        if inject_fake_meta:
            try:
                fake_exif_data = generate_fake_iphone_exif()
                piexif.insert(fake_exif_data, output_path)
                print(f"🔒 Sterile File Built & iPhone 15 Pro EXIF Injected -> {output_path}")
            except Exception as e:
                print(f"⚠️ Pixel processing succeeded, but EXIF injection failed: {e}")
        else:
            print(f"🔒 Sterile File Built with zero headers -> {output_path}")
        return True
    return False

if __name__ == "__main__":
    input_folder = "ipimages"
    output_folder = "opimages"
    
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    # Strictly allow ONLY standard root image files (.jpg, .jpeg, .png)
    valid_exts = ('.jpg', '.jpeg', '.png')
    images = [
        f for f in os.listdir(input_folder) 
        if f.lower().endswith(valid_exts) and os.path.isfile(os.path.join(input_folder, f))
    ]
    
    if not images:
        print("ℹ️ No matching files found directly in 'input_images' root folder.")
        sys.exit(0)
        
    for img_name in images:
        in_path = os.path.join(input_folder, img_name)
        base_name, _ = os.path.splitext(img_name)
        out_path = os.path.join(output_folder, f"{base_name}_humanized.webp")
        
        # Execute the full automated pipeline
        deep_strip_scramble_and_fake(in_path, out_path, COMPRESSION_QUALITY, inject_fake_meta=True)
    
