import cloudinary.uploader

def upload_image_to_cloudinary(image):
    result = cloudinary.uploader.upload(image)
    return result['secure_url']