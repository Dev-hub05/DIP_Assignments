import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# -----------------------------------------------------------------------------
INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"
TARGET_SIZE = (512, 512)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# TASK 1: PROJECT SETUP & INTRODUCTION
# -----------------------------------------------------------------------------
def print_header():
    """Prints the assignment header information."""
    print("="*60)
    print(" Name: [SATDEV]")
    print(" Roll No: [2301010298]")
    print(" Course: Image Processing & Computer Vision")
    print(" Unit: [UNIT NUMBER - 1]")
    print(" Assignment Title: Smart Document Scanner & Quality Analysis System")
    print(" Date: 2026-02-12")
    print("="*60)
    print("\n--- Welcome to Smart Document Scanner ---")
    print("Purpose: To analyze document image quality through sampling and quantization.")
    print("Importance: Understanding how resolution and bit-depth affect readability and OCR accuracy.")
    print("Effect: Lower sampling reduces detail; lower quantization causes banding and contrast loss.")
    print("-" * 60 + "\n")

# -----------------------------------------------------------------------------
# TASK 2: IMAGE ACQUISITION
# -----------------------------------------------------------------------------
def load_image(filename):
    """
    Loads an image from the inputs folder, resizes it to 512x512, 
    and converts it to grayscale.
    """
    path = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(path):
        print(f"Error: File {filename} not found in {INPUT_DIR}")
        return None, None
    
    # Load image
    original = cv2.imread(path)
    if original is None:
        print(f"Error: Could not load image {filename}")
        return None, None

    # Resize to 512x512
    original_resized = cv2.resize(original, TARGET_SIZE)
    
    # Convert to Grayscale
    grayscale = cv2.cvtColor(original_resized, cv2.COLOR_BGR2GRAY)
    
    # Save grayscale output
    base_name = os.path.splitext(filename)[0]
    gray_path = os.path.join(OUTPUT_DIR, f"{base_name}_grayscale.png")
    cv2.imwrite(gray_path, grayscale)
    
    print(f"Loaded {filename}: Resized to {TARGET_SIZE} and converted to Grayscale.")
    print(f"Saved grayscale image to: {gray_path}")
    
    return original_resized, grayscale

# -----------------------------------------------------------------------------
# TASK 3: IMAGE SAMPLING (RESOLUTION ANALYSIS)
# -----------------------------------------------------------------------------
def apply_sampling(grayscale_img, filename):
    """
    Simulates resolution reduction by downsampling and then upscaling back to 512x512.
    Returns the resampled images.
    """
    # 512x512 is the original grayscale (High Res)
    high_res = grayscale_img
    
    # Downsample to 256x256 (Medium Res)
    med_res_small = cv2.resize(grayscale_img, (256, 256), interpolation=cv2.INTER_LINEAR)
    med_res = cv2.resize(med_res_small, TARGET_SIZE, interpolation=cv2.INTER_NEAREST) # Upscale for visualization
    
    # Downsample to 128x128 (Low Res)
    low_res_small = cv2.resize(grayscale_img, (128, 128), interpolation=cv2.INTER_LINEAR)
    low_res = cv2.resize(low_res_small, TARGET_SIZE, interpolation=cv2.INTER_NEAREST) # Upscale
    
    # Save comparison image for Sampling
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    titles = ["High Res (512x512)", "Med Res (256x256)", "Low Res (128x128)"]
    images = [high_res, med_res, low_res]
    
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
        
    base_name = os.path.splitext(filename)[0]
    out_path = os.path.join(OUTPUT_DIR, f"{base_name}_sampling_comparison.png")
    plt.savefig(out_path)
    plt.close()
    
    print(f"Saved sampling comparison to: {out_path}")
    return med_res, low_res

# -----------------------------------------------------------------------------
# TASK 4: IMAGE QUANTIZATION (GRAY LEVEL REDUCTION)
# -----------------------------------------------------------------------------
def apply_quantization(grayscale_img, filename):
    """
    Quantizes the grayscale image into 8-bit, 4-bit, and 2-bit levels.
    """
    # 8-bit (256 levels) - Original grayscale
    # We can assume the input is already 8-bit (0-255)
    quant_8bit = grayscale_img 

    # 4-bit (16 levels)
    # Mapping 0-255 to 0-15 and back
    # Formula: floor(img / (256/levels)) * (255/(levels-1))
    levels_4bit = 16
    div_4bit = 256 / levels_4bit
    quant_4bit = np.floor(grayscale_img / div_4bit) * (255 / (levels_4bit - 1))
    quant_4bit = quant_4bit.astype(np.uint8)

    # 2-bit (4 levels)
    # Mapping 0-255 to 0-3 and back
    levels_2bit = 4
    div_2bit = 256 / levels_2bit
    quant_2bit = np.floor(grayscale_img / div_2bit) * (255 / (levels_2bit - 1))
    quant_2bit = quant_2bit.astype(np.uint8)
    
    # Save comparison for Quantization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    titles = ["8-bit (256 levels)", "4-bit (16 levels)", "2-bit (4 levels)"]
    images = [quant_8bit, quant_4bit, quant_2bit]
    
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
        
    base_name = os.path.splitext(filename)[0]
    out_path = os.path.join(OUTPUT_DIR, f"{base_name}_quantization_results.png")
    plt.savefig(out_path)
    plt.close()
    
    print(f"Saved quantization results to: {out_path}")
    return quant_8bit, quant_4bit, quant_2bit

# -----------------------------------------------------------------------------
# TASK 5: QUALITY OBSERVATION & ANALYSIS
# -----------------------------------------------------------------------------
def create_comparison_figure(original, gray, med_res, low_res, q_8bit, q_4bit, q_2bit, filename):
    """
    Generate a single comparison figure with all requested variations.
    """
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    # Flatten axes for easier indexing
    axes = axes.flatten()
    
    # List of images and titles
    # 1. Original (Color)
    # 2. Grayscale
    # 3. 512x512 (Same as Grayscale for structure, or maybe explicitly High Res)
    # 4. 256x256 (Sampled)
    # 5. 128x128 (Sampled)
    # 6. 8-bit (Quantized)
    # 7. 4-bit (Quantized)
    # 8. 2-bit (Quantized)
    
    # Convert BGR to RGB for matplotlib
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    
    img_list = [
        (original_rgb, "Original (512x512)"),
        (gray, "Grayscale (512x512)"),
        (gray, "High Res (512x512)"), # Using Grayscale as the High Res reference
        (med_res, "Med Res (256x256)"),
        (low_res, "Low Res (128x128)"),
        (q_4bit, "Quantized 4-bit"),
        (q_2bit, "Quantized 2-bit"),
        (q_8bit, "Quantized 8-bit") # Swapped slightly to fit grid? 
        # Actually let's follow the user list order if possible, filling 8 slots
        # User list: Original, Grayscale, 512, 256, 128, 8-bit, 4-bit, 2-bit (Total 8 items)
    ]
    
    # Re-ordering to match the prompt list exactly:
    # 1. Original
    # 2. Grayscale
    # 3. 512x512 (which is basically grayscale or original? Prompt implies sampling context, usually gray)
    # 4. 256x256
    # 5. 128x128
    # 6. 8-bit
    # 7. 4-bit
    # 8. 2-bit
    
    images_to_plot = [
        original_rgb, gray, gray, med_res, low_res, q_8bit, q_4bit, q_2bit
    ]
    titles_to_plot = [
        "Original", "Grayscale", "512x512 (Ref)", "256x256", "128x128", "8-bit", "4-bit", "2-bit"
    ]
    
    for ax, img, title in zip(axes, images_to_plot, titles_to_plot):
        if len(img.shape) == 3: # Color
            ax.imshow(img)
        else: # Grayscale
            ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
        
    plt.tight_layout()
    base_name = os.path.splitext(filename)[0]
    out_path = os.path.join(OUTPUT_DIR, f"{base_name}_final_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved final comparison to: {out_path}")

def print_observations(filename):
    print(f"\n--- Observations for {filename} ---")
    print("1. Sampling Analysis:")
    print("   - At 256x256, text remains readable but edges begin to soften.")
    print("   - At 128x128, significant aliasing (jaggies) appears; small text becomes illegible.")
    print("   - Fine details are lost rapidly as resolution decreases.")
    
    print("2. Quantization Analysis:")
    print("   - 8-bit (256 levels) provides smooth gradients and natural appearance.")
    print("   - 4-bit (16 levels) introduces noticeable false contouring (banding) in gradient areas.")
    print("   - 2-bit (4 levels) destroys most visual information, leaving only high-contrast shapes.")
    
    print("3. OCR Suitability:")
    print("   - High Res / 8-bit is ideal for OCR.")
    print("   - 128x128 resolution will likely fail OCR for standard document text.")
    print("   - 2-bit quantization leads to loss of character connectivity, causing OCR failure.")
    print("-" * 40)

# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------
def main():
    print_header()
    
    # Get all images from input directory
    input_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.pdf'))]
    
    if not input_files:
        print(f"No images found in '{INPUT_DIR}'. Please add images to run analysis.")
        return

    for filename in input_files:
        print(f"\nProcessing: {filename}...")
        
        # Task 2
        original, gray = load_image(filename)
        if original is None: continue
        
        # Task 3
        med_res, low_res = apply_sampling(gray, filename)
        
        # Task 4
        q_8bit, q_4bit, q_2bit = apply_quantization(gray, filename)
        
        # Task 5
        create_comparison_figure(original, gray, med_res, low_res, q_8bit, q_4bit, q_2bit, filename)
        print_observations(filename)

    print("\nProcessing Complete for all images.")

if __name__ == "__main__":
    main()
