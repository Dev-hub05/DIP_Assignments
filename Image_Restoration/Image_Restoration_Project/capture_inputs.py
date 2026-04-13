import time
from PIL import ImageGrab
import os
import shutil
import numpy as np

def main():
    input_dir = "inputs"
    # Ensure directory exists and is empty
    if os.path.exists(input_dir):
        # We don't want to delete the directory if it's locked, just files
        for f in os.listdir(input_dir):
            try:
                os.remove(os.path.join(input_dir, f))
            except Exception as e:
                print(f"Could not remove {f}: {e}")
    else:
        os.makedirs(input_dir)

    print("=== Image Capture Tool ===")
    print("This tool will capture 4 images from your clipboard.")
    print("Instructions:")
    print("1. Copy an image (Ctrl+C or Print Screen).")
    print("2. The script will detect it and save it.")
    print("3. Repeat for 4 distinct images.")
    print("--------------------------")

    target_count = 4
    captured_count = 0
    last_img_data = None

    print("Waiting for the first image...")

    while captured_count < target_count:
        try:
            img = ImageGrab.grabclipboard()
        except Exception as e:
            # Sometimes grabclipboard fails on certain content types
            img = None
        
        if img is not None:
            # grabclipboard can return a list of filenames if files were copied
            if isinstance(img, list):
                print("Detected file copy. Please copy image data (Print Screen/Right Click Copy Image).")
                time.sleep(1)
                continue
            
            # Check if this is a new image
            # We compare bytes to be sure
            try:
                # Convert to RGB to standardize
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Simple deduplication: verify it's not the exact same object capture
                # For robustness, we can check pixel data hash or simple bytes comparison
                current_img_data = img.tobytes()
                
                is_new = False
                if last_img_data is None:
                    is_new = True
                else:
                    if current_img_data != last_img_data:
                        is_new = True
                
                if is_new:
                    timestamp_str = str(int(time.time()))
                    filename = os.path.join(input_dir, f"captured_{captured_count+1}_{timestamp_str}.jpg")
                    img.save(filename, "JPEG")
                    captured_count += 1
                    last_img_data = current_img_data
                    
                    print(f"[Success] Saved {filename} ({captured_count}/{target_count})")
                    if captured_count < target_count:
                        print(f"Waiting for image {captured_count+1}...")
                
            except Exception as e:
                print(f"Error processing clipboard: {e}")
        
        time.sleep(1.0)
    
    print("\nAll 4 images captured successfully!")

if __name__ == "__main__":
    main()
