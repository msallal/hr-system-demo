from django.db import models
from hr.constants import ApplicationStatus, Department


class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    years_of_experience = models.IntegerField()
    # enumerated department ID (IT, HR, Finance):
    department_id = models.CharField(
        max_length=100,
        choices=Department,
        # default=Department.IT,
    )

    resume_upload = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']
        verbose_name_plural = 'candidates'


class Application(models.Model):
    """Application model - each candidate has its own application.
        Built as one to many, so a candidate could have many applications to allow business scalability.
    """
    id = models.AutoField(primary_key=True)
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=100,
        choices=ApplicationStatus,
        default=ApplicationStatus.SUBMITTED,
    )
    feedback = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.candidate.full_name


class ApplicationSatusHistory(models.Model):
    """Application Status History model.
    bounded to Application model, one to many (One Application, can have many statuses, business requirement)
    currently, no restrictions on changing statuses from one to another, based on the current phase of requirements.
    However, statuses are enumerated and being validated as well
    """
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=ApplicationStatus,
        default=None,
    )
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.status
