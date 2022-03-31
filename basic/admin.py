from django.contrib import admin
from basic import models


# Register your models here.
@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'abbreviation', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'abbreviation', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'salary', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'gender', 'salary', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']
    list_per_page = 10
