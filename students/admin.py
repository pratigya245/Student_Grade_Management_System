from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'display_gpa', 'date_enrolled']
    search_fields = ['first_name', 'last_name', 'student_id']

    def display_gpa(self, obj):
        return obj.get_gpa()
    display_gpa.short_description = 'GPA'