import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def compress_image(image, k):
    img_array = np.array(image)
    img_array_norm = img_array / 255.0

    # Reshape the image (N_pixels, 3 channels)
    h, w, d = img_array.shape
    reshaped_img = img_array_norm.reshape(h * w, d)

    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(reshaped_img)
    new_palette = (kmeans.cluster_centers_ * 255).astype(np.uint8)
    labels = kmeans.labels_

    compressed_pixel_data = new_palette[labels]

    # Reshape the compressed pixel data back to original image dimensions
    compressed_image_array = np.reshape(compressed_pixel_data, (h, w, d))

    compressed_image = Image.fromarray(compressed_image_array)

    return compressed_image