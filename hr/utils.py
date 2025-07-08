import os
import uuid
from rest_framework import serializers


def resume_uploaded_file_path(filename):
    """ This prepares the relative path of the uploaded file.
    Note: All resume uploads are saved in UUID.ext format in under the path: media/resumes/
    """
    ext = filename.split('.')[-1]
    uuid_filename = f"{uuid.uuid4()}.{ext}"
    return f'resumes/{uuid_filename}'

def resume_download_link(filename):
    return f'media/resumes/{filename}'


def check_resume_file(file):
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if file.size > max_size:
        raise serializers.ValidationError("file size exceeds maximum size(5MB)")

    # Check file extension
    allowed_extensions = ['.pdf', '.docx']
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in allowed_extensions:
        raise serializers.ValidationError("only pdf and docx files are allowed")

    # Check file MIME type for more security
    allowed_mime_types = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    if hasattr(file, 'content_type') and file.content_type not in allowed_mime_types:
        raise serializers.ValidationError("invalid file type, only pdf and docx are allowed")

    return file