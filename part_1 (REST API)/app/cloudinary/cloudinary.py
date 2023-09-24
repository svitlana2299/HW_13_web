import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from fastapi import UploadFile
from .config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

# Ініціалізація Cloudinary з даними із конфігурації
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


def upload_file_to_cloudinary(file: UploadFile):
    """
    Завантаження файлу на Cloudinary і повернення посилання на нього.
    """
    response = upload(file.file)
    url, options = cloudinary_url(
        response['public_id'], format=response['format'])
    return url
