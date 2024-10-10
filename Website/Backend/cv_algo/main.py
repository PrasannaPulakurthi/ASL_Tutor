from PIL import Image

def cv_algo(image):
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    return grayscale_image