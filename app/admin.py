"""
Admin module.
"""
from django.contrib import admin
from .models import Issue, Tag
# Register your models here.

admin.site.register(Issue)
admin.site.register(Tag)
