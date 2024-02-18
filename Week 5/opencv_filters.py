filters = [
    "",
    "blur",
    "boxFilter",
    "erode",
    "dilate",
    "GaussianBlur",
    "filter2D",
    "Sobel",
    "Laplacian",
    "dft",
    "getRotationMatrix2D",
    "warpAffine",
]

import cv2

filters_func = {
    "blur": cv2.blur,
    "boxFilter": cv2.boxFilter,
    "erode": cv2.erode,
    "dilate": cv2.dilate,
    "GaussianBlur": cv2.GaussianBlur,
    "filter2D": cv2.filter2D,
    "Sobel": cv2.Sobel,
    "Laplacian": cv2.Laplacian,
    "dft": cv2.dft,
    "getRotationMatrix2D": cv2.getRotationMatrix2D,
    "warpAffine": cv2.warpAffine,
}



import numpy as np

def apply_filter(filter_name, original_image):

    dtype = np.float64
    ksize = 3
    scale = 1
    delta = 0
    borderType = cv2.BORDER_DEFAULT

    filter_function = filters_func.get(filter_name, None)

    if filter_function is not None:
        if filter_name == "blur":
            return filter_function(original_image, (ksize, ksize))
        elif filter_name == "boxFilter":
            return filter_function(original_image, -1, (ksize, ksize), normalize=True, borderType=borderType)
        elif filter_name == "GaussianBlur":
            return filter_function(original_image, (ksize, ksize), sigmaX=0)
        elif filter_name == "Sobel":
            return filter_function(original_image, cv2.CV_64F, 1, 0, ksize=3)
        elif filter_name == "Laplacian":
            ddepth = cv2.CV_64F
            return filter_function(original_image, ddepth, ksize=3)
        elif filter_name == "dilate":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            anchor = (-1, -1)
            return filter_function(original_image, kernel, anchor=anchor, iterations=1)
        elif filter_name == "erode":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            anchor = (-1, -1)
            return filter_function(original_image, kernel, anchor=anchor, iterations=1)
        elif filter_name == "filter2D":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            anchor = (-1, -1)
            return filter_function(original_image, cv2.CV_64F, kernel, anchor=anchor)
        elif filter_name == "dft":
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            return filter_function(original_image.astype(dtype), flags=cv2.DFT_COMPLEX_OUTPUT)
        elif filter_name == "getRotationMatrix2D":
            center = (original_image.shape[1] // 2, original_image.shape[0] // 2)
            angle = 30
            scale = 1.0
            return filter_function(center, angle, scale)
        elif filter_name == "warpAffine":
            M = np.float32([[1, 0, 50], [0, 1, 50]])
            return filter_function(original_image, M, (original_image.shape[1], original_image.shape[0]))
        else:
            return filter_function(original_image, dtype, ksize, scale, delta, borderType)
    
    return None










