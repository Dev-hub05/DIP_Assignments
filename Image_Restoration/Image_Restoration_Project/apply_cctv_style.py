import cv2
import os
import random
import datetime

def apply_cctv_style(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return

    # 1. Resize to typical CCTV resolution (e.g., 640x480 or 800x600)
    # This blurs the details slightly
    img = cv2.resize(img, (800, 600))

    # 2. Add Timestamp
    font = cv2.FONT_HERSHEY_SIMPLEX
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Text settings
    font_scale = 0.8
    thickness = 2
    color = (255, 255, 255) # White text
    
    # Shadow (black)
    cv2.putText(img, timestamp, (22, 52), font, font_scale, (0, 0, 0), thickness + 1)
    cv2.putText(img, "REC", (22, 92), font, font_scale, (0, 0, 0), thickness + 1)
    cv2.putText(img, "CAM 01", (652, 52), font, font_scale, (0, 0, 0), thickness + 1)

    # Actual text
    cv2.putText(img, timestamp, (20, 50), font, font_scale, color, thickness)
    cv2.putText(img, "REC", (20, 90), font, font_scale, (0, 0, 255), thickness) # Red REC
    cv2.putText(img, "CAM 01", (650, 50), font, font_scale, color, thickness)

    # 3. Add slight blur to mimic low-quality lens
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Overwrite the input file with the "CCTV" version
    cv2.imwrite(image_path, img)
    print(f"Applied CCTV style to {image_path}")

def main():
    folder = "inputs"
    if not os.path.exists(folder):
        print("Inputs folder not found")
        return

    for filename in os.listdir(folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, filename)
            apply_cctv_style(path)

if __name__ == "__main__":
    main()
