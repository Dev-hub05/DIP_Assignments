# Smart Document Scanner & Quality Analysis System

## Course Information

**Course**: Image Processing & Computer Vision  
**Assignment Title**: Project 1 - Document Scanner Analysis  
**Date**: 2026-02-11

---

## 1. Real-World Problem Context

In digitized document workflows (e.g., banking checks, legal contracts, archival scanning), image quality is paramount. A "Smart Document Scanner" must balance storage efficiency against legibility.

When documents are scanned:

- **Sampling (Resolution)** affects the spatial detail. Low sampling rates cause "pixelation" or aliasing, making small fonts unreadable.
- **Quantization (Bit Debth)** affects the tonal range. Low bit-depth leads to false contouring (banding) and loss of subtle shading, critical for watermarks or signatures.

This project simulates these degradations to determine the minimum viable quality for reliable Optical Character Recognition (OCR) and human readability.

## 2. Technical Explanation

### Image Acquisition & Sensing

Document images are acquired via sensors (CCD/CMOS) that convert light intensity into digital signals. In this project, we utilize a custom capture utility:

1. **Clipboard Capture**: Users can capture real-world documents using the `Print Screen` (PrtSc) button or by copying an existing image to the clipboard.
2. **Setup**: The utility `capture_inputs.py` grabs the clipboard data and saves it to the `inputs/` folder.
3. **Sampling**: Discretizing the spatial coordinates (x, y) into a grid of pixels.
4. **Quantization**: Discretizing the amplitude (intensity) of each pixel into integral values (gray levels).

### Sampling (Resolution)

Reducing resolution (e.g., 512x512 → 128x128) discards spatial information.

- **High Res (512x512)**: Preserves edge definitions and character strokes.
- **Low Res (128x128)**: Causes blocky artifacts; text characters merge, making recognition impossible.

### Quantization (Gray Levels)

Reducing gray levels (e.g., 8-bit → 2-bit) restricts the number of available shades.

- **8-bit (256 levels)**: Standard grayscale, smooth transitions.
- **2-bit (4 levels)**: Extreme contrast; only black, dark gray, light gray, and white exist. This destroys texture and subtle features like paper grain or faint stamps.

### OCR Relevance

OCR engines require:

- **Sharp Edges** (dependent on Sampling) to distinguish similar characters (e.g., 'e' vs 'c').
- **Sufficient Contrast** (dependent on Quantization) to separate text from background noise.
- **Conclusion**: A minimum of 256x256 resolution and 4-bit depth is generally required for robust OCR on standard documents.

---

## 3. Implementation Details

The system is modularized into key functions:

- `load_image()`: Preprocesses inputs to a normalized 512x512 grayscale format.
- `apply_sampling()`: Simulates resolution drops using bicubic downsampling and nearest-neighbor upscaling for visualization.
- `apply_quantization()`: Reduces bit-depth mathematically using integer division and scaling.
- `create_comparison_figure()`: Aggregates all processed states into a single diagnostic image.

## 4. Observations (Sample Runs)

### Sample 1: doc1_printed.jpg (Textbook Page)

- **Context**: High-quality print with multi-column layout and diagrams.
- **Sampling**: At 128x128, the small column text merges into gray lines. The diagram loses its sharpness.
- **Quantization**: 4-bit (16 levels) preserves the text surprisingly well due to the high initial contrast, but the diagram's shading shows banding.

### Sample 2: doc2_scanned.png (PDF Export Scan)

- **Context**: Digital-to-digital or flatbed scan. High contrast and clean white background.
- **Sampling**: Because the text is sharp and heavy, it resists aliasing better than the printed sample at 256x256, but fails at 128x128.
- **Quantization**: Banding is visible in the subtle 'off-white' background variations at 4-bit.

### Sample 3: doc3_camera.jpg (Mobile Camera Photo)

- **Context**: Natural lighting with perspective distortion and sensor noise.
- **Sampling**: The combination of perspective thinning and low resolution (128x128) makes the tilted text almost impossible to recover.
- **Quantization**: The natural light gradient across the page suffers most. At 2-bit, the shadow side of the document turns black, deleting all text in that region.

---

## 5. How to Run

### Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
```

### Execution

1. Place input images (JPG, PNG, PDF) in the `inputs/` directory.
2. Run the scanner script:

```bash
python scanner.py
```

3. Check the `outputs/` directory for:
   - Grayscale versions
   - Sampling comparisons
   - Quantization results
   - Final comparison charts

## 6. Comparison Output Structure

The final generated figure (`*_final_comparison.png`) includes 8 subplots:

1. **Original** (Color 512x512)
2. **Grayscale**
3. **Reference High-Res**
4. **Medium Resolution** (256x256)
5. **Low Resolution** (128x128)
6. **8-bit Quantized**
7. **4-bit Quantized**
8. **2-bit Quantized**

---

**References**:

1. _Digital Image Processing_, Gonzalez & Woods (Sampling & Quantization chapters).
2. OpenCV Documentation: `cv2.resize`, `cv2.threshold`.
3. NumPy Documentation: Array manipulation for quantization.
