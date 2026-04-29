"""
Authored by Andre Ferreira
W1772798
"""

from django.contrib import admin
from .models import Department, Team, Dependency


class TeamInline(admin.TabularInline):
    model = Team
    extra = 0
    fields = ("name", "manager", "status", "contact_channel", "skills")


class DependencyInline(admin.TabularInline):
    model = Dependency
    fk_name = "upstream_team"
    extra = 0
    fields = ("upstream_team", "downstream_team", "flow_description")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "created_at")
    search_fields = ("name", "leader", "specialisation")
    inlines = [TeamInline]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "status", "contact_channel", "department")
    list_filter = ("status", "department")
    search_fields = ("name", "manager", "contact_channel", "department__name")
    inlines = [DependencyInline]


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ("upstream_team", "downstream_team", "flow_description")
    list_filter = ("upstream_team__department",)
    search_fields = ("upstream_team__name", "downstream_team__name", "flow_description")
