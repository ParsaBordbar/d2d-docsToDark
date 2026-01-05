import mimetypes
import os


def get_file_extension(file_path: str):
    return os.path.splitext(file_path)[1].lower()

def is_supported_image(extension: str):
    supported_list = [".png", ".jpg", ".jpeg", ".bmp"]
    if (supported_list.count(extension) == 1):
        return True
    False

def get_mime_type(file_path: str):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type