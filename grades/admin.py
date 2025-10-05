from django.contrib import admin
from .models import Course, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'credits']
    search_fields = ['course_code', 'course_name']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'score', 'date_recorded']
    list_filter = ['grade', 'course']
    search_fields = ['student__first_name', 'student__last_name']