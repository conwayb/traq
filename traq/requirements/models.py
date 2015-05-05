from django.db import models
from django.contrib.auth.models import User
from traq.projects.models import Project, Milestone

class MetaDataBaseModel(models.Model):
    """Base class that could be used elsewhere if you like refactoring"""
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='+')
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='+')

    class Meta:
        abstract=True

class Requirement(MetaDataBaseModel):
    """Acceptance Criteria for a Project or Development Phase"""
    title = models.CharField(max_length=255)
    description = models.TextField()

    project = models.ForeignKey(Project)
    milestone = models.ForeignKey(Milestone, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True,blank=True, related_name='requirements_approved')
    approved_on = models.DateTimeField(null=True, blank=True)
