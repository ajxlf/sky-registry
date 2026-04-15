from django.contrib import admin
from .models import Department, Team, Dependency

class TeamInline(admin.TabularInline):
    model = Team
    extra = 0

class DependencyInline(admin.TabularInline):
    model = Dependency
    extra = 0

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "created_at")
    search_fields = ("name", "leader", "specialisation")
    inlines = [TeamInline, DependencyInline]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "status", "department")
    list_filter = ("status", "department")
    search_fields = ("name", "manager", "department__name")

@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ("description", "department")
    list_filter = ("department",)
    search_fields = ("description", "department__name")