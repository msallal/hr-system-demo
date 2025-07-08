import os
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from rest_framework import serializers

from hr.utils import resume_uploaded_file_path, check_resume_file
from .constants import ApplicationStatus
from .models import Candidate, Application


class CandidateSerializer(serializers.ModelSerializer):
    """Candidate serializer - This serializer is created for admin list candidates usage"""
    class Meta:
        model = Candidate
        fields = ['id', 'full_name', 'email', 'phone_number', 'date_of_birth', 'department_id', 'years_of_experience']

    def validate_years_of_experience(self, years_of_experience):
        if years_of_experience <= 0:
            raise serializers.ValidationError('years of experience should be greater than 0')
        return years_of_experience


class CandidateWithFileSerializer(serializers.ModelSerializer):
    """Candidate serializer - This serializer is used to create new candidates"""
    resume_file = serializers.FileField(required=True, write_only=True)
    class Meta:
        model = Candidate
        fields = ['id', 'full_name', 'email', 'phone_number', 'date_of_birth', 'department_id', 'years_of_experience',
                  'resume_upload', 'resume_file', 'password']

    def validate_resume_file(self, file):
        return check_resume_file(file)

    def validate_years_of_experience(self, years_of_experience):
        if years_of_experience <= 0:
            raise serializers.ValidationError('years of experience should be greater than 0')
        return years_of_experience

    def create(self, validated_data):
        uploaded_resume = validated_data.pop('resume_file')
        plain_password = validated_data.pop('password')
        file_path = resume_uploaded_file_path(uploaded_resume.name)
        # store file to storage
        saved_file_path = default_storage.save(file_path, uploaded_resume)

        # create user with file information
        candidate = Candidate.objects.create(
            password=make_password(plain_password),
            #password=password,
            resume_upload=os.path.basename(saved_file_path),  # save generated UUID filename in db
            **validated_data
        )

        # create application record
        Application.objects.create(
            candidate=candidate,
            status=ApplicationStatus.SUBMITTED
        )

        return candidate