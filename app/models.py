# -*- coding: utf-8 -*-
'''
Models module.
'''
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Issue(models.Model):
    """
    Model Issue Q&A question and answer.
    """
    title = models.CharField(max_length=200, verbose_name=u'Pytanie')
    answer = models.TextField(verbose_name=u'Odpowiedz')
    date_add = models.DateTimeField()

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    """
    Model Tag, relation with Issue.
    """
    name = models.CharField(max_length=50)
    issue = models.ManyToManyField(Issue, related_name='tags')

    def __unicode__(self):
        return self.name

    def get_issue(self):
        """
        This method return issues by tag.
        :return:
        """
        return [item for item in self.issue.all()]
