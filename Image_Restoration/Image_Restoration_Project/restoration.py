import cv2
import numpy as np
import os

"""
Name: [Satdev]
Roll No: [2301010298]
Course: Image Processing & Computer Vision
Unit: [Unit 2]
Assignment Title: Noise Modeling and Image Restoration using Python
Date: 2026-02-12
"""

def add_gaussian_noise(image, mean=0, sigma=25):
    """Adds Gaussian noise to an image."""
    row, col = image.shape
    gauss = np.random.normal(mean, sigma, (row, col))
    noisy = image + gauss
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)

def add_salt_and_pepper_noise(image, salt_prob, pepper_prob):
    """Adds Salt-and-Pepper noise to an image."""
    noisy = np.copy(image)
    row, col = image.shape
    
    # Salt noise
    num_salt = np.ceil(salt_prob * image.size)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy[coords[0], coords[1]] = 255

    # Pepper noise
    num_pepper = np.ceil(pepper_prob * image.size)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy[coords[0], coords[1]] = 0
    
    return noisy

def calculate_mse(original, restored):
    """Computes Mean Squared Error."""
    return np.mean((original - restored) ** 2)

def calculate_psnr(original, restored):
    """Computes Peak Signal-to-Noise Ratio."""
    mse = calculate_mse(original, restored)
    if mse == 0:
        return 100
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))

def process_image(image_path, output_dir):
    """Processes a single image: adds noise, restores, evaluates."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    
    print(f"\nProcessing: {filename}")
    
    # Task 1: Load and Preprocess
    original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original is None:
        print(f"Error: Could not load {image_path}")
        return

    cv2.imwrite(os.path.join(output_dir, f"{name}_original{ext}"), original)

    # Task 2: Noise Modeling
    # Gaussian Noise
    noisy_gauss = add_gaussian_noise(original, sigma=25)
    cv2.imwrite(os.path.join(output_dir, f"{name}_noisy_gaussian{ext}"), noisy_gauss)
    
    # Salt and Pepper Noise
    noisy_sp = add_salt_and_pepper_noise(original, 0.02, 0.02)
    cv2.imwrite(os.path.join(output_dir, f"{name}_noisy_sp{ext}"), noisy_sp)

    # Task 3: Restoration
    # Mean Filter
    restored_mean_gauss = cv2.blur(noisy_gauss, (3, 3))
    restored_mean_sp = cv2.blur(noisy_sp, (3, 3))
    
    # Median Filter
    restored_median_gauss = cv2.medianBlur(noisy_gauss, 3)
    restored_median_sp = cv2.medianBlur(noisy_sp, 3)
    
    # Gaussian Filter
    restored_gauss_gauss = cv2.GaussianBlur(noisy_gauss, (3, 3), 0)
    restored_gauss_sp = cv2.GaussianBlur(noisy_sp, (3, 3), 0)

    # Save Restored Images
    cv2.imwrite(os.path.join(output_dir, f"{name}_restored_mean_gauss{ext}"), restored_mean_gauss)
    cv2.imwrite(os.path.join(output_dir, f"{name}_restored_mean_sp{ext}"), restored_mean_sp)
    cv2.imwrite(os.path.join(output_dir, f"{name}_restored_median_gauss{ext}"), restored_median_gauss)
    cv2.imwrite(os.path.join(output_dir, f"{name}_restored_median_sp{ext}"), restored_median_sp)
    cv2.imwrite(os.path.join(output_dir, f"{name}_restored_gauss_gauss{ext}"), restored_gauss_gauss)
    cv2.imwrite(os.path.join(output_dir, f"{name}_restored_gauss_sp{ext}"), restored_gauss_sp)

    # Task 4 & 5: Evaluation and Discussion
    results = {
        "Gaussian Noise": {
            "Mean Filter": (calculate_mse(original, restored_mean_gauss), calculate_psnr(original, restored_mean_gauss)),
            "Median Filter": (calculate_mse(original, restored_median_gauss), calculate_psnr(original, restored_median_gauss)),
            "Gaussian Filter": (calculate_mse(original, restored_gauss_gauss), calculate_psnr(original, restored_gauss_gauss))
        },
        "Salt & Pepper Noise": {
            "Mean Filter": (calculate_mse(original, restored_mean_sp), calculate_psnr(original, restored_mean_sp)),
            "Median Filter": (calculate_mse(original, restored_median_sp), calculate_psnr(original, restored_median_sp)),
            "Gaussian Filter": (calculate_mse(original, restored_gauss_sp), calculate_psnr(original, restored_gauss_sp))
        }
    }
    
    # Analytical Discussion snippet
    output_text = []
    output_text.append("-" * 60)
    output_text.append(f"{'Noise Type':<20} | {'Filter':<15} | {'MSE':<10} | {'PSNR (dB)':<10}")
    output_text.append("-" * 60)
    
    for noise_type, filters in results.items():
        for filter_name, (mse, psnr) in filters.items():
            output_text.append(f"{noise_type:<20} | {filter_name:<15} | {mse:<10.2f} | {psnr:<10.2f}")
            
    output_text.append("-" * 60)
    output_text.append("\nObservation:")
    output_text.append("Gaussian noise is generally better handled by Gaussian or Mean filters.")
    output_text.append("Salt-and-Pepper noise is effectively removed by Median filtering.")

    # Print to console
    print("\n".join(output_text))

    # Save to file
    with open(os.path.join(output_dir, f"{name}_performance.txt"), "w") as f:
        f.write("\n".join(output_text))



def main():
    input_dir = "inputs"
    output_dir = "outputs"
    
    # Create input directory if not exists (for user convenience)
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created '{input_dir}' directory. Please place images there.")
        return

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not image_files:
        print(f"No images found in '{input_dir}'. Please add surveillance-style images.")
        return
        
    for image_file in image_files:
        process_image(os.path.join(input_dir, image_file), output_dir)

if __name__ == "__main__":
    main()
