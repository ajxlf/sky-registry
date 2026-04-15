from django.contrib import admin
from .models import Department, Team, Dependency

class TeamInline(admin.TabularInline):
    model = Team
    extra = 0
    fields = ('name', 'manager', 'status')

class DependencyInline(admin.TabularInline):
    model = Dependency
    extra = 0
    fields = ('description',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'leader', 'specialisation')
    inlines = [TeamInline, DependencyInline]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'status', 'department', 'get_team_count')
    list_filter = ('status', 'department')
    search_fields = ('name', 'manager')
    list_select_related = ('department',)

    def get_team_count(self, obj):
        return f"{obj.department.name}"
    get_team_count.short_description = 'Department'

admin.site.register(Dependency)