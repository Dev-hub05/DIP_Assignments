
import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

print("=== Intelligent Image Processing System Started ===")

# ---------- Load Image ----------
img = cv2.imread("img.png")

if img is None:
    print("Image not found!")
    exit()

img = cv2.resize(img, (512, 512))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ---------- Create Output Folder ----------
os.makedirs("outputs", exist_ok=True)

# ---------- Noise Addition ----------
gaussian_noise = gray + np.random.normal(0, 25, gray.shape)
gaussian_noise = np.clip(gaussian_noise, 0, 255).astype(np.uint8)

sp_noise = gray.copy()
num = 1500
coords = [np.random.randint(0, i - 1, num) for i in gray.shape]
sp_noise[coords[0], coords[1]] = 255

# ---------- Filtering ----------
mean_filter = cv2.blur(sp_noise, (5, 5))
median_filter = cv2.medianBlur(sp_noise, 5)
gaussian_filter = cv2.GaussianBlur(sp_noise, (5, 5), 0)

# ---------- Enhancement ----------
equalized = cv2.equalizeHist(gray)

# ---------- Segmentation ----------
_, global_thresh = cv2.threshold(equalized, 127, 255, cv2.THRESH_BINARY)
_, otsu_thresh = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# ---------- Morphology ----------
kernel = np.ones((3, 3), np.uint8)
dilation = cv2.dilate(otsu_thresh, kernel, iterations=1)
erosion = cv2.erode(otsu_thresh, kernel, iterations=1)

# ---------- Edge Detection ----------
sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 1)
canny = cv2.Canny(gray, 100, 200)

# ---------- Feature Extraction ----------
orb = cv2.ORB_create()
kp, des = orb.detectAndCompute(gray, None)
feature_img = cv2.drawKeypoints(img, kp, None)

# ---------- Evaluation Metrics ----------
def mse(img1, img2):
    return np.mean((img1 - img2) ** 2)

mse_val = mse(gray, equalized)
psnr = 10 * np.log10((255 ** 2) / mse_val)
ssim_val = ssim(gray, equalized)

print("\n--- Metrics ---")
print("MSE :", mse_val)
print("PSNR:", psnr)
print("SSIM:", ssim_val)

# ---------- Save Outputs ----------
cv2.imwrite("outputs/original.jpg", gray)
cv2.imwrite("outputs/noisy.jpg", sp_noise)
cv2.imwrite("outputs/mean.jpg", mean_filter)
cv2.imwrite("outputs/median.jpg", median_filter)
cv2.imwrite("outputs/gaussian.jpg", gaussian_filter)
cv2.imwrite("outputs/enhanced.jpg", equalized)
cv2.imwrite("outputs/global.jpg", global_thresh)
cv2.imwrite("outputs/otsu.jpg", otsu_thresh)
cv2.imwrite("outputs/dilation.jpg", dilation)
cv2.imwrite("outputs/erosion.jpg", erosion)
cv2.imwrite("outputs/sobel.jpg", sobel)
cv2.imwrite("outputs/canny.jpg", canny)
cv2.imwrite("outputs/features.jpg", feature_img)

print("\nAll outputs saved successfully ✔")