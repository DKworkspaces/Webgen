import cv2
import numpy as np
import random
import os
import sys
import piexif

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
    """Reads raw pixels to completely drop original AI markers, shuffles the lattice,

    saves the final file, and appends organic smartphone camera profiles.
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

    canvas = np.zeros((h, w * 7, ch), dtype=np.float32)

    # 4. Row-by-row lattice scrambling sequence
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

    # 5. Restore original dimensions 
    final_resized = cv2.resize(canvas, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    final_output = np.clip(final_resized, 0, 255).astype(np.uint8)
    
    # 6. Save fresh file container
    # NOTE: If platforms strictly require EXIF insertion, JPEG offers the highest system compatibility
    success = cv2.imwrite(output_path, final_output, [int(cv2.IMWRITE_WEBP_QUALITY), quality_setting])
    
    if success:
        # 7. Inject the fake iPhone EXIF Profile into the freshly written sterile file wrapper
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
    
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_exts)]
    
    if not images:
        print("ℹ️ No images found in 'input_images' folder.")
        sys.exit(0)
        
    for img_name in images:
        in_path = os.path.join(input_folder, img_name)
        base_name = os.path.splitext(img_name)[0]
        out_path = os.path.join(output_folder, f"{base_name}_humanized.webp")
        
        # Toggle True/False here to turn fake camera injection ON/OFF dynamically
        deep_strip_scramble_and_fake(in_path, out_path, COMPRESSION_QUALITY, inject_fake_meta=True)
    
