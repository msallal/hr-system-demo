from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.reverse import reverse

from DjangoProject.settings import BASE_DIR
from hr.models import *
from hr.serializers import *
from hr.utils import resume_download_link
import logging


logger = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request, format=None):
    """
        API Root - Lists all available endpoints
        Browse through all the available API endpoints below.
        """
    candidate_id = 0
    return Response({
        'candidates': {
            'check_candidate': reverse('check-candidate', request=request, format=format),
            'new-candidate': reverse('new-candidate', request=request, format=format),
        },
        'admin': {
            'list candidates': reverse('admin-list-candidates', request=request, format=format),
            'update candidate application status': reverse('admin-update-application',
                                                           args=[candidate_id], request=request, format=format),
            'Download Candidate resume': reverse('admin-download-resume',
                                                 args=[candidate_id], request=request, format=format),
        }
    })

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_candidate(request):
    """
        Create Candidate - create new candidate application with initial status submitted
        """
    try:
        serializer = CandidateWithFileSerializer(data=request.data)
        if serializer.is_valid():
            # save new candidate details + create a record for his application with status "SUBMITTED"
            serializer.save()
            logger.info(f"Candidate with ID: {serializer.data['id']} has registered successfully!")
            return Response({"success" : "Your application has been submitted successfully!"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"failed to create new candidate {request.data['full_name']}, with error: {e}")
        return Response({"error": "Failed to create new candidate"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def candidate_application_check(request):
    """
        Application check - check candidate's application current status and history of updates
        """
    # retrieve candidate basic info: name is enough
    # retrieve application current status and feedback if exists
    # retrieve application status history and feedback with timestamps
    try:
        candidate = Candidate.objects.get(email=request.data['email'])
        if candidate is not None:
            if check_password(request.data['password'], candidate.password):
                serializer = CandidateSerializer(candidate)
                candidate_app = Application.objects.get(candidate_id=candidate.id)
                feedback = ""
                if candidate_app.feedback:
                    feedback = candidate_app.feedback
                if candidate_app.status == ApplicationStatus.SUBMITTED:
                    feedback = f"Your application has been submitted successfully!"
                application_status_history = (ApplicationSatusHistory.objects.filter(application_id=candidate_app.id).
                                              order_by("created_at"))
                statuses = []
                for application_status in application_status_history:
                    statuses.append({"updated_at" : application_status.created_at,
                                     "status" : application_status.status,
                                     "feedback" : application_status.feedback,
                                     "updated by" : application_status.created_by
                                     })

                return Response({'name': serializer.data["full_name"], "application_status": candidate_app.status,
                                 "feedback" : feedback, "history" : statuses})
        return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"failed to check candidate with email {request.data['email']}, error: {e}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def admin_list_candidates(request):
    """
        Admin [List Candidates] - List Candidate Applications for system admins
        """
    try:
        is_admin = request.headers.get('X-ADMIN', False)
        if is_admin == '1':
            candidates = Candidate.objects.all().order_by('-created_at')  # order by created_at
            department = request.GET.get('department')
            if department is not None:
                candidates = Candidate.objects.filter(department_id=department)

            # Add pagination
            paginator = LimitOffsetPagination()
            paginated_candidates = paginator.paginate_queryset(candidates, request)
            serializer = CandidateSerializer(paginated_candidates, many=True)

            return paginator.get_paginated_response(serializer.data)
            # return Response(serializer.data)
        return Response(None, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        logger.error(f"failed to list Candidate Applications for system admins, error: {e}")
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_application_status(request, candidate_id):
    """
        Admin [Update Application] - Update Candidate Application status with feedback/comments
        """
    try:
        is_admin = request.headers.get('X-ADMIN', False)
        if is_admin == '1':
            new_status = request.data.get('status', None)
            feedback = request.data.get('feedback', None)
            admin_name = request.data.get('admin_name', None)
            # validate request:
            if not feedback or not admin_name or not hasattr(ApplicationStatus, new_status):
                return Response(
                    {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
            if status is not None:
                with transaction.atomic():
                    candidate_app = Application.objects.filter(candidate=candidate_id).order_by('-created_at').first()
                    candidate_app.status = new_status
                    candidate_app.feedback = feedback
                    candidate_app.save()
                    create_new_status = ApplicationSatusHistory.objects.create(application_id=candidate_app.id, status=new_status,
                                                                               feedback=feedback, created_by=admin_name)
                    if create_new_status is not None:
                        create_new_status.save()
                        #TODO: send notification to candidate as status has been updated, such as email
                        return Response(None, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"Application status update failed!"}, status=status.HTTP_400_BAD_REQUEST)
    except Candidate.DoesNotExist:
        return Response({"error" : "Candidate ID not found"}, status=status.HTTP_404_NOT_FOUND)

    except Application.DoesNotExist:
        return Response({"error" : "Application ID not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"failed to update application status {request.data['id']}, with error: {e}")
        return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def download_candidate_resume(request, candidate_id):
    """
        Admin [Download Resume] - Download Candidate Resume
        """
    try:
        is_admin = request.headers.get('X-ADMIN', False)
        if is_admin == '1':
            candidate = Candidate.objects.get(id=candidate_id)

            # Check if candidate has a file
            if not candidate.resume_upload:
                return Response({"error": "No resume found for this candidate"}, status=status.HTTP_404_NOT_FOUND)
            file_name = resume_download_link(candidate.resume_upload)
            file_path = os.path.join(BASE_DIR, file_name)

            # check if file exists on disk
            #TODO: handle s3 storage case if would be used in future
            if not os.path.exists(file_path):
                logger.error(
                    f"failed to locate candidate resume {candidate.id}, file:({file_path})")
                return Response({"error": "resume file is not found"}, status=status.HTTP_404_NOT_FOUND)

            # return download file:
            logger.info(f"downloading resume file for candidate ID: {candidate.id}")
            return FileResponse(open(file_path, 'rb'))
        return Response({"error" : "bad request"}, status=status.HTTP_401_UNAUTHORIZED)
    except Candidate.DoesNotExist:
        return Response({"error" : "Candidate ID not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"failed to download candidate resume {request.data['id']}, with error: {e}")
        return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)