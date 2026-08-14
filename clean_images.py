import os
import glob
import cv2
from remove_ai_watermarks import remove_all

# Directory containing images to process
IMAGE_DIR = "media/images"
SUPPORTED_EXTENSIONS = ["*.png", "*.jpg", "*.jpeg", "*.webp"]

def process_repository_images():
    print(f"Scanning for AI images in './{IMAGE_DIR}'...")
    
    # Gather all image files
    files_to_process = []
    for ext in SUPPORTED_EXTENSIONS:
        files_to_process.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
        
    if not files_to_process:
        print("No images found to process.")
        return

    for file_path in files_to_process:
        print(f"Cleaning AI artifacts from: {file_path}")
        
        # Load image array
        image_array = cv2.imread(file_path)
        if image_array is None:
            continue
            
        # Strip metadata, C2PA tracking manifests, and visible logos
        processed_image = remove_all(
            image=image_array,
            strip_ai_metadata=True,  # Clears EXIF/C2PA fingerprints
            fix_faces=True           # Protects human face geometry from distortion
        )
        
        # Overwrite the original file with the cleaned version
        cv2.imwrite(file_path, processed_image)
        print(f"Successfully cleaned: {file_path}")

if __name__ == "__main__":
    process_repository_images()
  
