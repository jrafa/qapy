# -*- coding: utf-8 -*-

'''
Tests module.
'''
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Issue, Tag


class IssueTagHelp(object):
    '''
    This is a helper class.
    '''
    @staticmethod
    def create_issue(title='hello', answer='hello pep-8'):
        '''
        This method create issue in database.
        :param title:
        :param answer:
        :return:
        '''
        return Issue.objects.create(title=title, answer=answer, date_add='2016-02-06T21:09:44')

    def create_tag(self, name='pep8'):
        '''
        This method create issue and tag in database.
        :param name:
        :return:
        '''
        issue = self.create_issue()
        tag = Tag.objects.create(name=name)
        tag.issue.add(issue)
        return tag


class AppTest(TestCase, IssueTagHelp):
    """
    Class which tests models, views, urls.
    """
    def test_issue_creation(self):
        '''
        This method test model Issue.
        :return:
        '''
        issue = self.create_issue()
        self.assertTrue(isinstance(issue, Issue))
        self.assertEqual(issue.__unicode__(), issue.title)

    def test_tag_creation(self):
        '''
        This method test model Tag.
        :return:
        '''
        tag = self.create_tag()
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(tag.__unicode__(), tag.name)

    def test_issue_view(self):
        '''
        This method test view.
        :return:
        '''
        issue = self.create_issue()
        tag = self.create_tag()
        resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(issue.title, resp.content)
        self.assertIn(issue.answer, resp.content)
        self.assertIn(tag.name, resp.content)

    def test_tag_view(self):
        '''
        This method test view.
        :return:
        '''
        issue = self.create_issue()
        tag = self.create_tag()
        resp = self.client.get('/pep8')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(issue.title, resp.content)
        self.assertIn(issue.answer, resp.content)
        self.assertIn(tag.name, resp.content)

    def test_urls(self):
        '''
        This method test urls in app.
        :return:
        '''
        url = reverse('index')
        self.assertEqual(url, '/')

        url = reverse('tag', args=['django'])
        self.assertEqual(url, '/django')

        url = reverse('tag', args=['pep-8'])
        self.assertEqual(url, '/pep-8')

        url = reverse('tag', args=['django-python-pep-8'])
        self.assertEqual(url, '/django-python-pep-8')

    def test_url_connect_with_view(self):
        '''
        This method check if url connects with correct view.
        :return:
        '''
        resolver = resolve('/pep8')
        self.assertEqual(resolver.view_name, 'tag')

        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'index')


class APITest(APITestCase, IssueTagHelp):
    '''
    This class check API.
    '''
    def setUp(self):
        '''
        Method called to prepare the test fixture.
        :return:
        '''
        self.client = APIClient()
        User.objects.create_user(username='test@test.pl', password='realpassword', is_staff=True)
        self.client.login(username='test@test.pl', password='realpassword')

    def can_get_list(self, url):
        '''
        This method test view.
        :param url:
        :return:
        '''
        self.create_tag()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def can_get_content(self, url, data):
        '''
        This method check content.
        :param url:
        :param data:
        :return:
        '''
        self.create_tag()
        response = self.client.get(url, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['count'], 1)
        self.assertEqual(content['results'][0], data)

    def test_can_get_list_issues(self):
        '''
        This method test view with Issues and Tags.
        :return:
        '''
        self.can_get_list('/api/issues/')

    def test_can_get_list_tags(self):
        '''
        This method test view with Tags and Issues.
        :return:
        '''
        self.can_get_list('/api/tag/issues/')

    def test_issue_with_content(self):
        '''
        This method test content with issues.
        :return:
        '''
        self.can_get_content('/api/issues/', {u'answer': u'hello pep-8',
                                              u'date_add': u'2016-02-06T21:09:44Z',
                                              u'tags': [u'pep8'],
                                              u'id': 3,
                                              u'title': u'hello'})

    def test_tag_with_content(self):
        '''
        This method test content with tags.
        :return:
        '''
        self.can_get_content('/api/tag/issues/', {u'issue': [{u'answer': u'hello pep-8',
                                                              u'date_add': u'2016-02-06T21:09:44Z',
                                                              u'id': 4,
                                                              u'title': u'hello'}],
                                                  u'name': u'pep8'})
