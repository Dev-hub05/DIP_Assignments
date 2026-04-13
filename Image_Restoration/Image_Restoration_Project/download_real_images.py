import subprocess
import os

def download_image(url, filename):
    print(f"Downloading {url} -> {filename}...")
    try:
        # Pexels blocks python-urllib, so use curl with a user agent
        command = ["curl", "-L", "-A", "Mozilla/5.0", "-o", filename, url]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Done.")
        else:
            print(f"Failed: {result.stderr}")
    except Exception as e:
        print(f"Failed with exception: {e}")


def main():
    output_dir = "inputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dictionary of Scene -> URL
    # Using Pexels images and applying CCTV style in post-processing
    # Corridor removed as per user request
    images = {
        "sample_parking.jpg": "https://images.unsplash.com/photo-1506521781263-d8422e82f27a?q=80&w=1200",
        "sample_street.jpg": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?q=80&w=1200",
        "sample_store.jpg": "https://images.unsplash.com/photo-1534723452862-4c874018d66d?q=80&w=1200",
        "sample_office.jpg": "https://images.pexels.com/photos/3184325/pexels-photo-3184325.jpeg?auto=compress&cs=tinysrgb&w=1200"
    }

    for filename, url in images.items():
        download_image(url, os.path.join(output_dir, filename))

if __name__ == "__main__":
    main()
