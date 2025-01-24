import os
import uuid
from werkzeug.utils import secure_filename


def generate_unique_filename(filename):
    secured_name = secure_filename(filename)

    if not secured_name:
        secured_name = "default"

    unique_suffix = uuid.uuid4().hex

    name, ext = os.path.splitext(secured_name)
    unique_name = f"{name}_{unique_suffix}{ext}"

    return unique_name