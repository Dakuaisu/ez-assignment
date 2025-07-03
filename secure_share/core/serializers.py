from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileUpload
        fields=['file']

    def validate_file(self,value):
        allowed_extensions = ['.pptx', '.docx', '.xlsx']
        if not any(value.name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError("Only .pptx, .docx, and .xlsx files are allowed.")
        return value