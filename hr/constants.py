from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.TextChoices):
    """ Department choices - enumerated"""
    IT = "IT", _("IT")
    HR = "HR", _("HR")
    FINANCE = "FIN", _("FINANCE")


class ApplicationStatus(models.TextChoices):
    """ Application status choices - enumerated"""
    SUBMITTED = "SUBMITTED", _("SUBMITTED")
    UNDER_REVIEW = "UNDER_REVIEW", _("UNDER REVIEW")
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED", _("INTERVIEW SCHEDULED")
    REJECTED = "REJECTED", _("REJECTED")
    ACCEPTED = "ACCEPTED", _("ACCEPTED")