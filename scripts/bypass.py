import os
import random
import numpy as np
from PIL import Image

def bypass_detection_6x(image_path):
    with Image.open(image_path) as img:
        # 1. Convert to RGB to strip hidden alpha channel profiles
        img = img.convert("RGB")
        
        # 2. Lazy Resizing (Changes pixel grids slightly)
        w, h = img.size
        img = img.resize((w + random.choice([-2, 2]), h + random.choice([-2, 2])), Image.Resampling.LANCZOS)
        
        # Convert to numpy array for fast math processing
        data = np.array(img).astype('int16')
        
        # 3. Apply Micro-Noise 6 Times with Decay
        # Pass 1-2: Subtle variance (-2 to 2)
        # Pass 3-4: Micro variance (-1 to 1)
        # Pass 5-6: Binary variance (0 or 1) to break color consistency
        noise_ranges = [(-2, 3), (-2, 3), (-1, 2), (-1, 2), (0, 2), (0, 2)]
        
        for low, high in noise_ranges:
            noise = np.random.randint(low, high, data.shape, dtype='int16')
            data = np.clip(data + noise, 0, 255)
        
        # Convert back to image
        img = Image.fromarray(data.astype('uint8'))
        
        # 4. Save clean (Strips EXIF data completely)
        img.save(image_path, "JPEG", quality=95, optimize=True)

if __name__ == "__main__":
    bypass_detection_6x('output/final_bypass_image.jpg')
