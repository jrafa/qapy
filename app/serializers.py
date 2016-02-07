# -*- coding: utf-8 -*-
'''
Serializers module.
'''
from rest_framework import serializers
from .models import Issue, Tag


class IssueSerializer(serializers.ModelSerializer):
    '''
    Issue serializer.
    '''
    class Meta:
        model = Issue
        fields = ('id', 'title', 'answer', 'date_add')


class IssueTagsSerializer(serializers.ModelSerializer):
    '''
    Issue and Tags serializer.
    '''
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Issue
        fields = ('id', 'title', 'answer', 'date_add', 'tags')


class TagSerializer(serializers.ModelSerializer):
    '''
    Tag serializer.
    '''
    issue = IssueSerializer(many=True)

    class Meta:
        model = Tag
        fields = ('name', 'issue')
