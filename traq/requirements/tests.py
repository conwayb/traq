from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, Permission

from ..utils.tests import TraqCustomTest
from traq.projects.models import Project
from .models import Requirement

class RequirementBaseTestCase(TraqCustomTest):
    def setUp(self):
        super(RequirementBaseTestCase, self).setUp()
        requirement_permissions = Permission.objects.filter(content_type__model='requirement').values_list('pk', flat=True)
        self.admin.user_permissions.add(*requirement_permissions)
        self.admin.save()

class RequirementCreateViewTestCase(RequirementBaseTestCase):
    # test form valid and success url
    def tearDown(self):
        self.client.logout()

    def test_403(self):
        self.client.login(username='raygun', password='foo')
        response = self.client.get(reverse('requirements-create', kwargs={'project':self.project.pk}))
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        self.client.login(username='moltres', password='foo')
        response = self.client.get(reverse('requirements-create', kwargs={'project':self.project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], self.project)

    def test_form_valid(self):
        self.client.login(username='moltres', password='foo')
        data = {'title':'robot', 'description':'all about robots'}
        response = self.client.post(reverse('requirements-create', kwargs={'project':self.project.pk}), data)
        r = Requirement.objects.get(title='robot')
        self.assertEqual(r.created_by, self.admin)
        self.assertEqual(r.modified_by, self.admin)
        self.assertEqual(r.project, self.project)
        self.assertRedirects(response, reverse('requirements-detail', kwargs={'pk':r.pk}))

class RequirementApproveViewTestCase(RequirementBaseTestCase):
    #test form_valid and negative assertion on http GET method.
    def setUp(self):
        super(RequirementApproveViewTestCase, self).setUp()
        requirement = Requirement(title='robot', description='is cools', project=self.project,
                                  created_by=self.admin, modified_by=self.admin)
        requirement.save()
        self.requirement = requirement
        self.client.login(username='moltres', password='foo')

    def test_get_not_allowed(self):
        response = self.client.get(reverse('requirements-approve', kwargs={'pk':self.requirement.pk}))
        self.assertEqual(response.status_code, 405)

    def test_form_valid(self):
        data = {'approved':True}
        r = Requirement.objects.get(pk=self.requirement.pk)
        self.assertFalse(r.approved)
        response = self.client.post(reverse('requirements-approve', kwargs={'pk':self.requirement.pk}), data)
        r = Requirement.objects.get(pk=self.requirement.pk)
        self.assertTrue(r.approved)
        self.assertEqual(r.modified_by, self.admin)
