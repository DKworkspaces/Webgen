import cv2

def wipe_logos(input_path, output_path):
    img = cv2.imread(input_path)
    h, w = img.shape[:2]
    
    # Calculate a 3% crop from every single border side
    top = int(h * 0.03)
    bottom = int(h * 0.97)
    left = int(w * 0.03)
    right = int(w * 0.97)
    
    cropped = img[top:bottom, left:right]
    cv2.imwrite(output_path, cropped)
    print("Visible edge signatures cropped out.")

if __name__ == "__main__":
    wipe_logos('output/step2_disrupted.jpg', 'output/step3_cropped.jpg')
