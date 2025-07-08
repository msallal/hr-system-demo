from datetime import date

import pytest
from django.core.exceptions import ValidationError

from hr.constants import ApplicationStatus
from hr.models import Candidate, Application, ApplicationSatusHistory


@pytest.mark.django_db
class TestCandidateModel:
    """Test cases for Candidate model"""

    def test_create_candidate(self):
        """Test creating a candidate"""
        candidate = Candidate.objects.create(
            full_name='Mohammad Alsallal',
            email='mohammad@test.com',
            phone_number='07923112313',
            date_of_birth=date(2025, 1, 1),
            years_of_experience=10,
            department_id="IT"
        )

        assert candidate.full_name == 'Mohammad Alsallal'
        assert candidate.email == 'mohammad@test.com'
        assert candidate.phone_number == '07923112313'
        assert candidate.date_of_birth == date(2025, 1, 1)
        assert candidate.years_of_experience == 10
        assert candidate.department_id == "IT"
        assert str(candidate) == 'Mohammad Alsallal'


    def test_candidate_validation(self):
        """Test model validation"""
        with pytest.raises(ValidationError):
            candidate = Candidate(full_name='', email='mohammad@test.com', phone_number='07923112313')
            candidate.full_clean()


@pytest.mark.django_db
class TestApplicationModel:
    """Test cases for Application model"""

    def test_create_application(self):
        """Test creating an application"""
        candidate = Candidate.objects.create(
            full_name='Mohammad Alsallal',
            email='mohammad@test.com',
            phone_number='07923112313',
            date_of_birth=date(2025, 1, 1),
            years_of_experience=10,
            department_id="IT"
        )
        assert candidate.id is not None

        application = Application.objects.create(
            candidate=candidate,
            status=ApplicationStatus.SUBMITTED,
            feedback='Some feedback'
        )

        assert application.candidate_id == candidate.id
        assert application.status == ApplicationStatus.SUBMITTED
        assert application.feedback == 'Some feedback'
        assert str(application) == candidate.full_name



    def test_application_validation(self):
        """Test model validation"""
        with pytest.raises(ValidationError):
            application = Application()
            application.full_clean()


@pytest.mark.django_db
class TestApplicationStatusHistoryModel:
    """Test cases for Application model"""

    def test_create_application_status_history(self):
        """Test creating an application"""
        candidate = Candidate.objects.create(
            full_name='Mohammad Alsallal',
            email='mohammad@test.com',
            phone_number='07923112313',
            date_of_birth=date(2025, 1, 1),
            years_of_experience=10,
            department_id="IT"
        )
        assert candidate.id is not None

        application = Application.objects.create(
            candidate=candidate,
            status=ApplicationStatus.SUBMITTED,
            feedback='Some feedback'
        )

        assert application.candidate_id == candidate.id
        assert application.status == ApplicationStatus.SUBMITTED
        assert application.feedback == 'Some feedback'
        assert str(application) == candidate.full_name

        application_status = ApplicationSatusHistory.objects.create(
            application=application,
            status=ApplicationStatus.UNDER_REVIEW,
            feedback='Some feedback for an under review',
            created_by="Admin1"
        )

        assert application_status.application_id == application.id
        assert application_status.status == ApplicationStatus.UNDER_REVIEW
        assert application_status.feedback == 'Some feedback for an under review'
        assert application_status.created_by == "Admin1"
        assert str(application_status) == ApplicationStatus.UNDER_REVIEW


    def test_application_status_validation(self):
        """Test model validation"""
        with pytest.raises(ValidationError):
            application_status = ApplicationSatusHistory()
            application_status.full_clean()