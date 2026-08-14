import os
import glob
import cv2
from remove_ai_watermarks import remove_all

# Input and output directory definitions
INPUT_DIR = "src/images"
OUTPUT_DIR = "src/images/clean"
SUPPORTED_EXTENSIONS = ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.tiff"]

def process_repository_images():
    print(f"Scanning for AI images in './{INPUT_DIR}'...")
    
    # Ensure the output workspace directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Gather all image files from the source directory
    files_to_process = []
    for ext in SUPPORTED_EXTENSIONS:
        files_to_process.extend(glob.glob(os.path.join(INPUT_DIR, ext)))
        
    if not files_to_process:
        print("No images found to process.")
        return

    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        # Define the target destination path inside the clean folder
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"Cleaning AI artifacts from: {file_path}")
        
        # Load image array
        image_array = cv2.imread(file_path)
        if image_array is None:
            print(f"Skipping unreadable file: {file_path}")
            continue
            
        # Strip metadata, C2PA tracking manifests, and visible logos
        processed_image = remove_all(
            image=image_array,
            strip_ai_metadata=True,  # Clears EXIF/C2PA fingerprints
            fix_faces=True           # Protects human face geometry from distortion
        )
        
        # Save the processed result into the clean folder
        cv2.imwrite(output_path, processed_image)
        print(f"Successfully saved clean file to: {output_path}")

if __name__ == "__main__":
    process_repository_images()
    
