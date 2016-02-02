'''
Module views.
'''
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from .models import Issue, Tag
from .serializers import IssueTagsSerializer, TagSerializer


# Create your views here.
class IssuesView(TemplateView):
    '''
    View shows question and answer with tags.
    '''
    template_view = 'app/index.html'

    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        tags = Tag.objects.all()
        return render(request, self.template_view, {'issues': issues, 'tags': tags})


class TagView(TemplateView):
    '''
    View shows issue filter by tag.
    '''
    template_view = 'app/tag.html'

    def get(self, request, tag, *args, **kwargs):
        issues = Tag.objects.filter(name=tag)
        tags = Tag.objects.all()
        return render(request, self.template_view, {'issues': issues, 'tag': tag, 'tags': tags})


class ListIssuesViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This API view shows issues with tags.
    '''
    serializer_class = IssueTagsSerializer
    queryset = Issue.objects.all()


class ListTagsIssuesViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This API view shows issues with tags.
    '''
    serializer_class = TagSerializer
    queryset = Tag.objects.all().prefetch_related('issue')
