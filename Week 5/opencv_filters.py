filters = [
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



def apply_filter(filter_name, original_image):

    dtype = cv2.CV_64F
    dx = 1
    dy = 1
    ksize = 3
    scale = 1
    delta = 0
    borderType = cv2.BORDER_DEFAULT

    filter_function = filters_func.get(filter_name, None)

    if filter_function is not None:
        return filter_function(original_image, dtype, dx, dy, ksize, scale, delta, borderType)
    
    return None


