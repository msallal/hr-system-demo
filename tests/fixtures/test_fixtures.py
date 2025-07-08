# from datetime import date
#
# import pytest
#
# from hr.models import Candidate
#
#
# @pytest.fixture
# def create_candidates():
#     candidates = []
#     for i in range(100):
#         candidates.append(Candidate.objects.create(
#             full_name='Mohammad Alsallal',
#             email=f'mohammad{i}@test.com',
#             phone_number='079123{i}',
#             date_of_birth=date(2025, 1, 1),
#             years_of_experience=10,
#             department_id="IT",
#             resume_upload=f"sample_resume_candidate{i}.pdf"
#         ))
#
#     return candidates