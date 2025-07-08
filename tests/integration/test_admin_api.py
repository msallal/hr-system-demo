from datetime import date

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from hr.constants import Department, ApplicationStatus
from hr.models import Candidate
from tests.integration.test_api import create_test_pdf_file


@pytest.mark.django_db
class TestAdminAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_admin_list_candidates_api(self, create_candidates):
        list_candidate_response = self.client.get(
            reverse('admin-list-candidates'),
            headers={'X-ADMIN': '1'},
        )

        # print(list_candidate_response.data)
        assert list_candidate_response.status_code == 200
        assert 'count' in list_candidate_response.data
        assert 'next' in list_candidate_response.data
        assert 'previous' in list_candidate_response.data
        assert 'results' in list_candidate_response.data
        for candidate in list_candidate_response.data['results']:
            assert 'id' in candidate
            assert 'full_name' in candidate
            assert 'email' in candidate
            assert 'phone_number' in candidate
            assert 'date_of_birth' in candidate
            assert 'department_id' in candidate
            assert 'years_of_experience' in candidate
            assert 'password' not in candidate

    def test_admin_list_candidates_pagination_first_page(self, create_candidates):
        count = len(create_candidates)
        response = self.client.get(
            reverse('admin-list-candidates'),
            {
                'limit': 10,
                'offset': 0,
            },
            headers={'X-ADMIN': '1'},
        )
        data = response.json()

        assert response.status_code == 200
        assert 'count' in data
        assert data['count'] == count
        assert 'next' in data
        assert data['next'] is not None
        assert 'previous' in data
        assert data['previous'] is None
        assert 'results' in data
        for candidate in data['results']:
            assert 'id' in candidate
            assert 'full_name' in candidate
            assert 'email' in candidate
            assert 'phone_number' in candidate
            assert 'date_of_birth' in candidate
            assert 'department_id' in candidate
            assert 'years_of_experience' in candidate
            assert 'password' not in candidate

    def test_admin_list_candidates_pagination_second_page(self, create_candidates):
        response = self.client.get(
            reverse('admin-list-candidates'),
            {
                'limit': 10,
                'offset': 10, # for testing the second page
            },
            headers={'X-ADMIN': '1'},
        )
        data = response.json()

        assert response.status_code == 200
        assert 'count' in data
        assert 'next' in data
        assert data['next'] is not None
        assert 'previous' in data
        assert data['previous'] is not None # for the second page test
        assert 'results' in data
        for candidate in data['results']:
            assert 'id' in candidate
            assert 'full_name' in candidate
            assert 'email' in candidate
            assert 'phone_number' in candidate
            assert 'date_of_birth' in candidate
            assert 'department_id' in candidate
            assert 'years_of_experience' in candidate
            assert 'password' not in candidate

    def test_admin_list_candidates_pagination_last_page(self, create_candidates):
        count = len(create_candidates)
        response = self.client.get(
            reverse('admin-list-candidates'),
            {
                'limit': 10,
                'offset': count-10, # for testing the second page
            },
            headers={'X-ADMIN': '1'},
        )
        data = response.json()

        assert response.status_code == 200
        assert 'count' in data
        assert data['count'] == count
        assert 'next' in data
        assert data['next'] is None # for the last page
        assert 'previous' in data
        assert data['previous'] is not None # for the last page
        assert 'results' in data
        for candidate in data['results']:
            assert 'id' in candidate
            assert 'full_name' in candidate
            assert 'email' in candidate
            assert 'phone_number' in candidate
            assert 'date_of_birth' in candidate
            assert 'department_id' in candidate
            assert 'years_of_experience' in candidate
            assert 'password' not in candidate


    def test_admin_list_candidates_empty_result(self):
        response = self.client.get(
            reverse('admin-list-candidates'),
            headers={'X-ADMIN': '1'},
        )
        data = response.json()

        print("Testing empty result")
        print(response.data)
        assert response.status_code == 200
        assert 'count' in data
        assert data['count'] == 0  # for empty case test
        assert 'next' in data
        assert data['next'] is None # for empty case test
        assert 'previous' in data
        assert data['previous'] is None # for empty case test
        assert 'results' in data
        assert data['results'] == [] # for empty case test


    def test_admin_not_authorized_list_candidates_api(self, create_candidates):
        list_candidate_response = self.client.get(
            reverse('admin-list-candidates'),
        )

        assert list_candidate_response.status_code == status.HTTP_403_FORBIDDEN


    def test_admin_list_candidates_with_filters_api(self, create_candidates):
        department_filters = Department.choices
        for choice in department_filters:
            list_candidate_department_filtered_response = self.client.get(
                reverse('admin-list-candidates'),
                {'department' : choice[0]},
                headers={'X-ADMIN': '1'},
            )

            # print(f" testing admin list candidates filtered with department {choice[0]}")
            assert list_candidate_department_filtered_response.status_code == 200
            assert 'count' in list_candidate_department_filtered_response.data
            assert 'next' in list_candidate_department_filtered_response.data
            assert 'previous' in list_candidate_department_filtered_response.data
            assert 'results' in list_candidate_department_filtered_response.data
            for candidate in list_candidate_department_filtered_response.data['results']:
                assert 'id' in candidate
                assert 'full_name' in candidate
                assert 'email' in candidate
                assert 'phone_number' in candidate
                assert 'date_of_birth' in candidate
                assert 'department_id' in candidate
                assert 'years_of_experience' in candidate
                assert 'password' not in candidate

    def test_admin_download_resume_api(self, create_candidate_with_resume_file):
        candidate = create_candidate_with_resume_file
        download_response = self.client.get(
            reverse('admin-download-resume', args=[candidate.id]),
            headers={'X-ADMIN': '1'},
        )

        assert download_response.status_code == status.HTTP_200_OK
        assert 'Content-Disposition' in download_response
        assert candidate.resume_upload in download_response['Content-Disposition']
        # print(candidate.resume_upload)


    def test_admin_update_application_status_api(self, create_candidate_with_resume_file):
        candidate = create_candidate_with_resume_file
        statuses = ApplicationStatus.choices
        for st in statuses:
            update_status_response = self.client.put(
                reverse('admin-update-application', args=[candidate.id]),
                {
                    'status': st[0],
                    'feedback' : f'Your application status has been updated to {st[0]} successfully.',
                    'admin_name': 'Admin Sameer'
                 },
                headers={'X-ADMIN': '1'},
            )

            assert update_status_response.status_code == status.HTTP_204_NO_CONTENT



@pytest.fixture
def create_candidates():
    candidates = []
    department_filters = Department.choices
    for choice in department_filters:
        for i in range(len(candidates), 50):
            candidates.append(Candidate.objects.create(
                full_name='Mohammad Alsallal',
                email=f'mohammad{i}@test.com',
                phone_number=f'079123{i}',
                date_of_birth=date(2025, 1, 1),
                years_of_experience=10,
                department_id=choice[0],
                resume_upload=f"sample_resume_candidate{i}.pdf"
            ))

    return candidates


@pytest.fixture(scope='function')
def create_candidate_with_resume_file():
    client = APIClient()
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

    register_response = client.post(
        reverse('new-candidate'),
        data=candidate_data,
        format='multipart'
    )
    # print(register_response.data)
    candidate =  Candidate.objects.get(email=candidate_data["email"])

    assert register_response.status_code == status.HTTP_201_CREATED
    return candidate