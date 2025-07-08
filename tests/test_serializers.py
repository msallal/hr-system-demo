from datetime import date

import pytest

from hr.constants import Department
from hr.serializers import CandidateSerializer
from hr.models import Candidate


@pytest.mark.django_db
class TestCandidateSerializer:
    """Test cases for Candidate serializer"""

    def test_candidate_serializer_valid_data(self):
        """Test serializer with valid data"""
        data = {
            'full_name': 'Ahmad Omar',
            'email': 'ahmad@test.com',
            'password': 'testpassword',
            'phone_number': '123456789',
            'date_of_birth': '2025-07-01',
            'years_of_experience': 10,
            'department_id': 'IT'
        }
        serializer = CandidateSerializer(data=data)

        assert serializer.is_valid()
        candidate = serializer.save()
        assert candidate.full_name == 'Ahmad Omar'
        assert candidate.email == 'ahmad@test.com'
        assert candidate.phone_number == '123456789'
        assert candidate.date_of_birth == date(2025, 7, 1)
        assert candidate.years_of_experience == 10
        assert candidate.department_id == Department.IT

    def test_candidate_serializer_invalid_data(self):
        """Test serializer with invalid data"""
        data = {
            'full_name': '',  # Empty title should be invalid
            'email': 'ahmad_test.com',
            'phone_number': '',
            'date_of_birth': '2025',
            'years_of_experience': -10,
            'department_id': '12345'
        }
        serializer = CandidateSerializer(data=data)

        assert not serializer.is_valid()
        assert 'full_name' in serializer.errors
        assert 'email' in serializer.errors
        assert 'phone_number' in serializer.errors
        assert 'date_of_birth' in serializer.errors
        assert 'years_of_experience' in serializer.errors
        assert 'department_id' in serializer.errors

    def test_candidate_serializer_output(self):
        """Test serializer output"""
        candidate = Candidate.objects.create(
            full_name='Mohammad Alsallal',
            email='mohammad@test.com',
            phone_number='07923112313',
            date_of_birth=date(2025, 1, 1),
            years_of_experience=10,
            department_id="IT"
        )

        serializer = CandidateSerializer(candidate)

        expected_data = {
            'id': candidate.id,
            'full_name': 'Mohammad Alsallal',
            'email': 'mohammad@test.com',
            'phone_number': '07923112313',
            'date_of_birth': '2025-01-01',
            'years_of_experience': 10,
            'department_id': 'IT'
        }
        assert serializer.data == expected_data


#TODO: Write tests for the remaining serializers
@pytest.mark.django_db
def test_check_database_name():
    """Test database check"""
    from django.conf import settings
    from django.db import connection

    print(f"Database name: {settings.DATABASES['default']['NAME']}")
    print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"Connection database: {connection.settings_dict['NAME']}")