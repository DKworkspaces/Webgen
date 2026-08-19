import cv2
import numpy as np

def disrupt_pixels(input_path, output_path):
    img = cv2.imread(input_path)
    
    # 1. Bilateral Filter to smooth micro-frequencies while preserving sharp edges
    bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
    
    # 2. Simulate Smart Blur/Cutout via a stylized kernel smoothing
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) # Sharpening kernel matrix
    sharpened = cv2.filter2D(bilateral, -1, kernel)
    
    # 3. Scale down the image resolution by exactly 2x to discard pixel intervals
    height, width = sharpened.shape[:2]
    downscaled = cv2.resize(sharpened, (width // 2, height // 2), interpolation=cv2.INTER_AREA)
    
    cv2.imwrite(output_path, downscaled)
    print("Pixel geometry disruption complete.")

if __name__ == "__main__":
    disrupt_pixels('output/step1_meta.jpg', 'output/step2_disrupted.jpg')
