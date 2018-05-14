import cv2
import numpy as np

# Change this to one of your generated images:
image_file = 'example.png'

image = cv2.imread(image_file)
cv2.imshow('Original image', image)

# Convert to grayscale, followed by thresholding to black and white
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
cv2.imshow('Black and white', thresh)

# Apply opening: "erosion" followed by "dilation"
denoised = thresh.copy()
kernel = np.ones((4, 3), np.uint8)
denoised = cv2.erode(denoised, kernel, iterations=1)
kernel = np.ones((6, 3), np.uint8)
denoised = cv2.dilate(denoised, kernel, iterations=1)
cv2.imshow('Denoised', denoised)

# Now find contours and overlay them over our original image
_, cnts, _ = cv2.findContours(denoised.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contoured = image.copy()
cv2.drawContours(contoured, cnts, contourIdx=-1, color=(255, 0, 0), thickness=-1)
cv2.imshow('Contours', contoured)

# Create a fresh 'mask' image
mask = np.ones((image.shape[0], image.shape[1]), dtype="uint8") * 0
# We'll use the first contour as an example
contour = cnts[0]
# Draw this contour over the mask
cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

cv2.imshow('Denoised image', denoised)
cv2.imshow('Mask after drawing contour', mask)

result = cv2.bitwise_and(denoised, mask)
cv2.imshow('Result after and operation', result)

retain = result > 0
result = result[np.ix_(retain.any(1), retain.any(0))]
cv2.imshow('Final result', result)

cv2.waitKey(0)