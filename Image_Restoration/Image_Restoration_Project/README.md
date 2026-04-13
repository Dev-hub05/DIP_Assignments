# Image Restoration for Surveillance Camera Systems

## Project Overview
This project simulates and restores surveillance camera footage. It demonstrates the entire pipeline of:
1.  **Acquisition:** Downloading realistic stock images (Parking, Street, Store, Office).
2.  **Preprocessing:** Converting to grayscale and applying a "CCTV Style" overlay (Timestamp, REC indicator, Blur, Low Resolution) to mimic authentic security footage.
3.  **Degradation:** Adding synthetic noise (Gaussian Noise for sensor imperfection, Salt-and-Pepper Noise for transmission errors).
4.  **Restoration:** Applying spatial filters (Mean, Median, Gaussian) to recover the image quality.
5.  **Evaluation:** Calculating Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR) to measure restoration performance.

## features
- **Realistic Data:** Uses real-world images processed to look like CCTV footage.
- **Noise Modeling:** Simulates common surveillance noise types.
- **Restoration Algorithms:** Implements and compares 3 standard spatial filters.
- **Quantitative Metrics:** Automatically generates performance reports (MSE/PSNR).

## Project Structure
- `inputs/`: Contains the 4 input surveillance images.
- `outputs/`: Contains the processed images (Noisy, Restored) and performance text files.
- `restoration.py`: Main script for noise modeling, restoration, and evaluation.
- `download_real_images.py`: Script to fetch the test images from online sources.
- `apply_cctv_style.py`: Helper script to apply the CCTV visual effects (overlay, blur).

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Matplotlib (optional, for visualization)

## Usage
1.  **Setup:**
    ```bash
    pip install opencv-python numpy matplotlib
    ```
2.  **Run the Pipeline:**
    ```bash
    # 1. Download images
    python download_real_images.py
    
    # 2. Apply CCTV effects
    python apply_cctv_style.py
    
    # 3. Process and Restore
    python restoration.py
    ```
3.  **Check Results:**
    - View generated images in the `outputs/` folder.
    - Check `outputs/sample_{scene}_performance.txt` for detailed metrics.

## Future Improvements
- Implement temporal filtering for video inputs.
- Explore deep learning-based denoising (e.g., Autoencoders, UNet).
