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
    zeroth_ifd = {
        piexif.ImageIFD.Make: u"Apple",
        piexif.ImageIFD.Model: u"iPhone 15 Pro",
        piexif.ImageIFD.Software: u"18.1.1", 
        piexif.ImageIFD.XResolution: (72, 1),
        piexif.ImageIFD.YResolution: (72, 1),
        piexif.ImageIFD.ResolutionUnit: 2,
    }
    
    exif_ifd = {
        piexif.ExifIFD.ExifVersion: b"0232",
        piexif.ExifIFD.ExposureTime: (1, 120),  
        piexif.ExifIFD.FNumber: (18, 10),       
        piexif.ExifIFD.ISOSpeedRatings: 64,     
        piexif.ExifIFD.FocalLength: (686, 100), 
        piexif.ExifIFD.LensMake: u"Apple",
        piexif.ExifIFD.LensModel: u"iPhone 15 Pro back triple camera 6.86mm f/1.78",
    }
    
    exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes

def deep_strip_scramble_and_fake(image_path, output_path, quality_setting, inject_fake_meta=True):
    """
    Reads raw pixels, shuffles individual pixel positions randomly within 

    their micro-sequences to avoid blocking artifacts, and writes a sterile WebP.
    """
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

    # Compute asymmetric one-sided averages
    asym_ab = a + (b * 0.5)
    asym_bc = b + (c * 0.5)
    asym_cd = c + (d * 0.5)
    asym_da = d + (a * 0.5)

    max_slots = 7
    canvas = np.zeros((h, w * max_slots, ch), dtype=np.float32)

    for y in range(h):
        seq_choice = random.choice([1, 2, 3])
        
        if seq_choice == 1:
            # Stack the 7 components into a 3D matrix of shape (7, w, ch)
            stacked = np.stack([a[y], asym_ab[y], b[y], asym_bc[y], c[y], asym_cd[y], d[y]], axis=0)
        elif seq_choice == 2:
            # Stack 6 components
            stacked = np.stack([a[y], asym_ab[y], b[y], c[y], asym_cd[y], d[y]], axis=0)
        elif seq_choice == 3:
            # Stack 5 components
            stacked = np.stack([a[y], b[y], asym_bc[y], c[y], d[y]], axis=0)
            
        num_components = stacked.shape[0] # either 7, 6, or 5
        
        # Create an array of random indices to mix the pixels horizontally
        # Instead of block 1 then block 2, it picks the pixel column elements randomly
        shuffled_row = np.zeros((w * num_components, ch), dtype=np.float32)
        
        # Interleave the columns randomly
        for x in range(w):
            pixel_pool = stacked[:, x, :] # Pool of 5-7 pixels for this position
            
            # Shuffle the order of pixels inside this localized column pool
            indices = list(range(num_components))
            random.shuffle(indices)
            shuffled_pool = pixel_pool[indices]
            
            # Place them back into the expanded row layout
            start_idx = x * num_components
            end_idx = start_idx + num_components
            shuffled_row[start_idx:end_idx] = shuffled_pool
            
        canvas[y, :shuffled_row.shape[0]] = shuffled_row

    # Restore native spatial dimensions (Width, Height format for cv2.resize)
    final_resized = cv2.resize(canvas, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    final_output = np.clip(final_resized, 0, 255).astype(np.uint8)
    
    # Save sterile WebP container
    success = cv2.imwrite(output_path, final_output, [int(cv2.IMWRITE_WEBP_QUALITY), quality_setting])
    
    if success:
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
        
        deep_strip_scramble_and_fake(in_path, out_path, COMPRESSION_QUALITY, inject_fake_meta=True)
    
