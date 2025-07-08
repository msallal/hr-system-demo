from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('candidates/', views.create_candidate, name='new-candidate'),
    path('candidate/check', views.candidate_application_check, name='check-candidate'),
    path('admin/candidates/', views.admin_list_candidates, name='admin-list-candidates'),
    path('admin/candidates/<int:candidate_id>/', views.update_application_status, name='admin-update-application'),
    path('admin/candidates/<int:candidate_id>/resume-download/', views.download_candidate_resume, name='admin-download-resume'),
]
