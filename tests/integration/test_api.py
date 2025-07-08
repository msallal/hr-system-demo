from datetime import date

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from hr.models import Candidate


def create_test_pdf_file():
    """Create a test PDF file for upload"""
    # Create a simple PDF-like content
    pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 0>>endobj\nxref\n0 3\n0000000000 65535 f\n0000000009 00000 n\n0000000074 00000 n\ntrailer<</Size 3/Root 1 0 R>>startxref\n106\n%%EOF"

    return SimpleUploadedFile(
        "sample_resume.pdf",
        pdf_content,
        content_type="application/pdf"
    )


@pytest.mark.django_db
class TestApi:
    def setup_method(self):
        self.client = APIClient()

    def test_candidate_registration_and_login(self):
        """Test candidate registration & Check Application status (basic login)"""
        # Step 1: Register new candidate
        resume_file = create_test_pdf_file()
        candidate_data = {
            'full_name': 'Mohammad Sameer',
            'email': 'mohammad2025@test.com',
            'password': 'test1234',
            'phone_number': '07923112555',
            'date_of_birth': '2025-01-01',
            'years_of_experience': 10,
            'department_id': 'IT',
            'resume_file': resume_file,
        }

        register_response = self.client.post(
            reverse('new-candidate'),
            data=candidate_data,
            format='multipart'
        )
        print(register_response.data)

        assert register_response.status_code == status.HTTP_201_CREATED

        # Step 2: Test candidate login (application status check)
        login_data = {
            'email': candidate_data.get('email'),
            'password': candidate_data.get('password')
        }

        login_response = self.client.post(
            reverse('check-candidate'),
            data=login_data,
            format='json'
        )

        assert login_response.status_code == status.HTTP_200_OK
        assert 'name' in login_response.data
        assert 'application_status' in login_response.data
        assert 'feedback' in login_response.data
        assert 'history' in login_response.data
        status_history = login_response.data.get('history', [])
        for h_status in status_history:
            assert 'status' in h_status
            assert 'feedback' in h_status
            assert 'updated_at' in h_status
            assert 'updated by' in h_status


@pytest.fixture
def create_candidate():
    password = 'test1234'
    candidate = Candidate.objects.create(
        full_name='Mohammad Alsallal',
        email='mohammad_candidate@test.com',
        password=password,
        phone_number=f'079123{i}',
        date_of_birth=date(2025, 1, 1),
        years_of_experience=10,
        department_id="IT",
        resume_upload=f"sample_resume_candidate_mohammad.pdf"
    )
    candidate.password = password
    return candidate

#TODO: write tests to validate the uploaded file size, type
#TODO: write tests cases for s3 storage, if we would use it in future, it should have some integration tests
