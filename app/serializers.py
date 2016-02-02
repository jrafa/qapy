'''
TODO
'''
from rest_framework import serializers
from .models import Issue, Tag


class IssueSerializer(serializers.ModelSerializer):
    '''
    TODO
    '''
    class Meta:
        model = Issue
        fields = ('id', 'title', 'answer', 'date_add')


class IssueTagsSerializer(serializers.ModelSerializer):
    '''
    TODO
    '''
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Issue
        fields = ('id', 'title', 'answer', 'date_add', 'tags')


class TagSerializer(serializers.ModelSerializer):
    '''
    TODO
    '''
    issue = IssueSerializer(many=True)

    class Meta:
        model = Tag
        fields = ('name', 'issue')
