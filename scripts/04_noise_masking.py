import cv2
import numpy as np

def apply_noise_masking(input_path, real_path, output_path):
    img = cv2.imread(input_path)
    h, w, c = img.shape
    
    # 1. Generate 3% pure Gaussian noise
    gaussian_noise = np.random.normal(0, 15, (h, w, c)).astype('uint8')
    img_with_gauss = cv2.addWeighted(img, 0.97, gaussian_noise, 0.03, 0)
    
    # 2. Overlay actual organic camera grain from reference image
    real_grain = cv2.imread(real_path)
    real_grain_resized = cv2.resize(real_grain, (w, h), interpolation=cv2.INTER_LINEAR)
    
    # Advanced Soft-Light blending matrix formula for physical grain injection
    final_image = cv2.addWeighted(img_with_gauss, 0.95, real_grain_resized, 0.05, 0)
    
    # 3. Simple brightness adjustments to offset the noise dark-mapping
    final_image = cv2.convertScaleAbs(final_image, alpha=1.02, beta=2)
    
    cv2.imwrite(output_path, final_image)
    print("Final structural noise overlay complete.")

if __name__ == "__main__":
    apply_noise_masking('output/step3_cropped.jpg', 'reference/real_camera.jpg', 'output/final_bypass_image.jpg')
