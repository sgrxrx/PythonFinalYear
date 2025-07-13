from django.contrib import admin

from .models import Issue, Authority

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'issue_type',
        'status',
        'priority',
        'title',
        'description',
        'latitude',
        'longitude',
        'image',
        'assigned_to',
        'authority_comment',
        'reported_by',
        'created_at',
    )

@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'issue_type',
    )