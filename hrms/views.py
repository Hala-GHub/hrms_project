from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView,
)

from .models import Department, Employee, Project, EmployeeLevel, ProjectStatus
from .forms import DepartmentForm, EmployeeForm, ProjectForm


# ─────────────────────────────────────────────
# HTMX Mixin
# ─────────────────────────────────────────────

class HtmxResponseMixin:
    def htmx_response(self, message: str) -> HttpResponse:
        return HttpResponse(message)

    def is_htmx(self) -> bool:
        return self.request.headers.get("HX-Request") == "true"


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────

class DashboardView(TemplateView):
    template_name = "hrms/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employee_count"] = Employee.objects.filter(is_active=True).count()
        ctx["department_count"] = Department.objects.count()
        ctx["project_count"] = Project.objects.count()
        ctx["recent_employees"] = Employee.objects.order_by("-created_at")[:5]
        ctx["active_projects"] = Project.objects.filter(status="ACTIVE")[:5]
        return ctx


# ─────────────────────────────────────────────
# Departments
# ─────────────────────────────────────────────

class DepartmentListView(ListView):
    model = Department
    template_name = "hrms/departments/department_list.html"
    context_object_name = "departments"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        if q:
            return Department.objects.filter(name__icontains=q)
        return Department.objects.filter(parent__isnull=True)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            from django.template.response import TemplateResponse
            return TemplateResponse(
                self.request,
                "hrms/departments/_table_rows.html",
                context,
            )
        return super().render_to_response(context, **response_kwargs)


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "hrms/departments/department_detail.html"


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "hrms/departments/department_form.html"


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "hrms/departments/department_form.html"


class DepartmentDeleteView(DeleteView):
    model = Department
    success_url = reverse_lazy("hrms:department_list")
    template_name = "hrms/departments/department_confirm_delete.html"


# ─────────────────────────────────────────────
# Employees
# ─────────────────────────────────────────────

class EmployeeListView(ListView):
    model = Employee
    template_name = "hrms/employees/employee_list.html"
    context_object_name = "employees"

    def get_queryset(self):
        qs = Employee.objects.select_related("department", "manager")
        q = self.request.GET.get("q", "")
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        return qs

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            from django.template.response import TemplateResponse
            return TemplateResponse(
                self.request,
                "hrms/employees/_table_rows.html",
                context,
            )
        return super().render_to_response(context, **response_kwargs)


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "hrms/employees/employee_detail.html"
    context_object_name = "emp"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        emp = self.object
        ctx["direct_reports"] = emp.direct_reports.all()
        ctx["projects"] = emp.projects.all()
        ctx["led_projects"] = emp.led_projects.all()
        return ctx


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "hrms/employees/employee_form.html"


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "hrms/employees/employee_form.html"


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = reverse_lazy("hrms:employee_list")
    template_name = "hrms/employees/employee_confirm_delete.html"


# ─────────────────────────────────────────────
# Projects
# ─────────────────────────────────────────────

class ProjectListView(ListView):
    model = Project
    template_name = "hrms/projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        qs = Project.objects.select_related("department", "lead")
        q = self.request.GET.get("q", "")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            from django.template.response import TemplateResponse
            return TemplateResponse(
                self.request,
                "hrms/projects/_table_rows.html",
                context,
            )
        return super().render_to_response(context, **response_kwargs)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "hrms/projects/project_detail.html"


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "hrms/projects/project_form.html"


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "hrms/projects/project_form.html"


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("hrms:project_list")
    template_name = "hrms/projects/project_confirm_delete.html"