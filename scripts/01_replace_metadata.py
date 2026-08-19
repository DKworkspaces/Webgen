import os
from PIL import Image
import piexif

def replace_metadata(ai_path, real_path, output_path):
    # Load the real photo's EXIF data
    try:
        real_exif = piexif.load(real_path)
        # Convert EXIF dictionary to bytes
        exif_bytes = piexif.dump(real_exif)
    except Exception:
        # Fallback empty EXIF if reference fails
        exif_bytes = piexif.dump({})

    # Open AI image, strip everything, save with real EXIF
    with Image.open(ai_path) as img:
        # Re-saving strips native software/C2PA tags if saved without them
        img.save(output_path, "JPEG", exif=exif_bytes, quality=95)
    print("Metadata replacement complete.")

if __name__ == "__main__":
    os.makedirs('output', exist_ok=True)
    replace_metadata('input/ai_image.jpg', 'reference/real_camera.jpg', 'output/step1_meta.jpg')
