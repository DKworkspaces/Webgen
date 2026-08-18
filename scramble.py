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

def apply_image_blending_hack(base_image_matrix, opacity=0.045):
    """
    NEW SEPARATE FUNCTION: Generates a high-frequency, non-uniform human 
    camera sensor noise envelope and blends it at a micro-opacity over the matrix.
    This disrupts global FFT patterns and invisible watermarks without altering the base logic.
    """
    # 1. Generate standard normal distribution noise matching the image dimensions
    grain_base = np.random.normal(127, 8, base_image_matrix.shape).astype(np.float32)
    
    # 2. Smooth out boundaries using localized Gaussian blur
    grain_blur = cv2.GaussianBlur(grain_base, (3, 3), 0)
    
    # 3. Equalize the histogram to distribute frequencies uniformly across the monochrome plane
    gray_grain = cv2.cvtColor(grain_blur.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    texture_noise = cv2.equalizeHist(gray_grain)
    
    # 4. Expand back to 3-channel color format for blending
    texture_noise_3ch = cv2.cvtColor(texture_noise, cv2.COLOR_GRAY2BGR).astype(np.float32)

    # 5. Execute adversarial spatial blending overlay
    blended_matrix = cv2.addWeighted(
        base_image_matrix.astype(np.float32), 1.0 - opacity, 
        texture_noise_3ch, opacity, 0
    )
    return blended_matrix

def deep_strip_scramble_and_fake(image_path, output_path, quality_setting, inject_fake_meta=True):
    """
    Executes original 4-stage matrix extraction, spatial pixel interlacing,
    then processes the matrix through the isolated image blending hack function.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Error: Could not read image {image_path}")
        return False

    # --- UNTOUCHED ORIGINAL SPATIAL INTERLACING LOGIC ---
    a = img[0::2, 0::2].astype(np.float32)
    b = img[0::2, 1::2].astype(np.float32)
    c = img[1::2, 0::2].astype(np.float32)
    d = img[1::2, 1::2].astype(np.float32)

    h, w, ch = a.shape

    asym_ab = a + (b * 0.5)
    asym_cd = c + (d * 0.5)

    canvas = np.zeros((h * 2, w * 2, ch), dtype=np.float32)
    canvas[0::2, 0::2] = a
    canvas[0::2, 1::2] = asym_ab
    canvas[1::2, 0::2] = c
    canvas[1::2, 1::2] = asym_cd

    final_resized = cv2.resize(canvas, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)
    
    # --- ISOLATED CALL TO NEW BLENDING FUNCTION ---
    # The matrix array is passed to the new dedicated function, keeping logic separate.
    post_processed_matrix = apply_image_blending_hack(final_resized, opacity=0.045)
    
    # Clip numerical ranges back to valid integer dimensions
    final_output = np.clip(post_processed_matrix, 0, 255).astype(np.uint8)
    
    # --- CONTAINER COMPILATION AND META INJECTION ---
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
    
