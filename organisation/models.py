"""
Authored by Andre Ferreira
W1772798
"""

from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    leader = models.CharField(max_length=100)
    specialisation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "departments"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="Active")
    contact_channel = models.CharField(max_length=100, blank=True)
    skills = models.TextField(
        blank=True,
        help_text="Comma-separated list of skills, e.g. Python, AWS, Docker",
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="teams"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.department.name})"

    def skills_list(self):
        """Return skills as a clean Python list."""
        return [s.strip() for s in self.skills.split(",") if s.strip()]


class Dependency(models.Model):
    upstream_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="downstream_dependencies",
        help_text="The team that depends on another (the arrow source).",
    )
    downstream_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="upstream_dependencies",
        help_text="The team being depended on (the arrow target).",
    )
    flow_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short description of what flows between these teams.",
    )

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "dependencies"

    def __str__(self):
        return f"{self.upstream_team.name} → {self.downstream_team.name}"
