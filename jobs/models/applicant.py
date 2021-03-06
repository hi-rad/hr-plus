from django.db import models
from django.utils.translation import gettext_lazy as _
from ..validators import validate_mobile_number, validate_pdf
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model


class Applicant(models.Model):
    class ApplicantStatus(models.TextChoices):
        APPLIED = 'APL', _('Applied')
        UNDER_EVALUATION = 'UE', _('Under Evaluation')
        ACCEPTED_FOR_FIRST_INTERVIEW = 'AF', _('Accepted for First Interview')
        ACCEPTED_FOR_SECOND_INTERVIEW = 'AS', _('Accepted for Second Interview')
        ACCEPTED_FOR_THIRD_INTERVIEW = 'AT', _('Accepted for Third Interview')
        REJECTED = 'RJ', _('Rejected')
        OFFER = 'OF', _('Offer')
        CANCELED = 'CL', _('Canceled')

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.CharField(validators=[validate_mobile_number], max_length=11)
    description = models.TextField(default="", blank=True)
    job_posting = models.ForeignKey('JobPosting', blank=False, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=4,
        choices=ApplicantStatus.choices,
        default=ApplicantStatus.APPLIED,
    )
    picture = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    cv = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=False,
                          validators=[validate_pdf, FileExtensionValidator(['pdf'])])
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applicants'
        app_label = 'jobs'

    def __str__(self):
        return self.full_name + " for " + self.job_posting.title


class ApplicantHistory(models.Model):
    status = models.CharField(
        max_length=4,
        choices=Applicant.ApplicantStatus.choices,
        default=Applicant.ApplicantStatus.APPLIED,
    )
    applicant = models.ForeignKey('Applicant', blank=False, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        db_table = 'applicants_history'
        app_label = 'jobs'

    def __str__(self):
        return self.applicant.full_name + " - " + self.status
