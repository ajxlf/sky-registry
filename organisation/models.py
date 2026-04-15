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
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="teams"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class Dependency(models.Model):
    description = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="dependencies"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.description
