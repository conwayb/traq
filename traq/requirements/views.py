from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from .models import Requirement
from .forms import RequirementForm, RequirementApproveForm
from ..projects.models import Project

class RequirementBaseView(object):
    model = Requirement

    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.filter(name__in=['arc', 'arcclient']).exists():
            return super(RequirementBaseView , self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied()

    def get_context_data(self, *args, **kwargs):
        data = super(RequirementBaseView, self).get_context_data(*args, **kwargs)
        try:
            project = Project.objects.get(pk=self.object.project.pk)
        except:
            project = Project.objects.get(pk=self.kwargs['project'])
        data['project'] = project
        return data

class RequirementListView(RequirementBaseView, ListView):
    """ """

class RequirementDetailView(RequirementBaseView, DetailView):
    """ """

class RequirementEditBaseView(RequirementBaseView):
    """ """
    form_class = RequirementForm

    def get_success_url(self):
        return reverse('requirements-detail', args=(self.object.pk,))

class RequirementCreateView(RequirementEditBaseView, CreateView):
    """ """
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        project = Project.objects.get(pk=self.kwargs['project'])
        form.instance.project = project
        return super(RequirementCreateView, self).form_valid(form)

class RequirementUpdateView(RequirementEditBaseView, UpdateView):
    """ """

class RequirementApproveView(RequirementUpdateView):
    form_class = RequirementApproveForm
    http_method_names =['post']

    def form_valid(self, form):
        if form.cleaned_data['approved']:
            form.instance.approved_by = self.request.user
            form.instance.approved_on = timezone.now()
        else:
            form.instance.approved_by = None
            form.instance.approved_on = None
        response = super(RequirementApproveView, self).form_valid(form)
        try:
            user =self.object.approved_by.username
        except:
            user = None
        data = {
                'object': self.object.pk,
                'approved': self.object.approved,
                'approved_on': self.object.approved_on,
                'approved_by': user,
                }
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return response
