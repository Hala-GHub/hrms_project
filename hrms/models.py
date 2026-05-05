from django.db import models


# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class EmployeeLevel(models.TextChoices):
    L1 = "L1", "L1 – Associate"
    L2 = "L2", "L2 – Junior"
    L3 = "L3", "L3 – Mid-Level"
    L4 = "L4", "L4 – Senior IC"
    SPM = "SPM", "Senior Product Manager"
    GROUP_MANAGER = "GM", "Group Manager"
    DIRECTOR = "DIR", "Director"
    SVP = "SVP", "Senior Vice President"
    VP = "VP", "Vice President"
    CEO = "CEO", "Chief Executive Officer"
    CFO = "CFO", "Chief Financial Officer"
    CTO = "CTO", "Chief Technology Officer"
    COO = "COO", "Chief Operating Officer"


class EmployeeType(models.TextChoices):
    INDIVIDUAL_CONTRIBUTOR = "IC", "Individual Contributor"
    MIDDLE_MANAGEMENT = "MM", "Middle Management"
    SENIOR_LEADERSHIP = "SL", "Senior Leadership"
    C_SUITE = "CS", "C-Suite"


class ProjectStatus(models.TextChoices):
    PLANNING = "PLAN", "Planning"
    ACTIVE = "ACTIVE", "Active"
    ON_HOLD = "HOLD", "On Hold"
    COMPLETED = "DONE", "Completed"
    CANCELLED = "CANC", "Cancelled"


# ─────────────────────────────────────────────
# Department
# ─────────────────────────────────────────────

class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_departments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("hrms:department_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]


# ─────────────────────────────────────────────
# Employee
# ─────────────────────────────────────────────

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=200)
    employee_type = models.CharField(
        max_length=2,
        choices=EmployeeType.choices,
        default=EmployeeType.INDIVIDUAL_CONTRIBUTOR,
    )
    level = models.CharField(
        max_length=5,
        choices=EmployeeLevel.choices,
        default=EmployeeLevel.L1,
    )
    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="employees",
    )
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="direct_reports",
    )
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.level})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("hrms:employee_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["last_name", "first_name"]


# ─────────────────────────────────────────────
# Project
# ─────────────────────────────────────────────

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=6,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNING,
    )
    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )
    lead = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="led_projects",
    )
    members = models.ManyToManyField(
        Employee,
        blank=True,
        related_name="projects",
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("hrms:project_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]