from PIL import ImageGrab, Image
import os
import time

INPUT_DIR = "inputs"
os.makedirs(INPUT_DIR, exist_ok=True)

def capture_image(filename):
    print(f"\n--- CAPTURING {filename} ---")
    print(f"Action: Please open your document image and press 'PrtSc' or copy the image to your clipboard.")
    choice = input("Press Enter to Capture, 's' to skip this one, or 'q' to quit: ")
    
    if choice.lower() == 'q':
        return "quit"
    if choice.lower() == 's':
        return "skip"
    
    # Give a tiny bit of time for clipboard to settle
    time.sleep(0.5)
    
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            path = os.path.join(INPUT_DIR, filename)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(path)
            print(f"SUCCESS: Captured and saved to {path}")
            return "done"
        else:
            print("ERROR: Clipboard does not contain an image. Please try again.")
            return "retry"
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return "retry"

def main():
    print("Welcome to Input Capture Utility (Enhanced)")
    
    images = [
        ("1", "doc1_printed.jpg"),
        ("2", "doc2_scanned.png"),
        ("3", "doc3_camera.jpg")
    ]
    
    while True:
        print("\nWhat would you like to do?")
        for key, name in images:
            status = "[Exists]" if os.path.exists(os.path.join(INPUT_DIR, name)) else "[Missing]"
            print(f"{key}. Capture/Recapture {name} {status}")
        print("4. Finish and Run Analysis")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice in ("1", "2", "3"):
            idx = int(choice) - 1
            name = images[idx][1]
            status = ""
            while status not in ("done", "skip", "quit"):
                status = capture_image(name)
        elif choice == "4":
            print("\nFinalizing... You can now run 'python scanner.py'.")
            break
        elif choice == "5":
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
