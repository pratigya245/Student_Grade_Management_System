from django.db import models
from students.models import Student

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Grade(models.Model):
    GRADE_CHOICES = [
        ('HD', 'High Distinction (85-100)'),
        ('D', 'Distinction (75-84)'),
        ('C', 'Credit (65-74)'),
        ('P', 'Pass (50-64)'),
        ('N', 'Fail (0-49)'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} - {self.course.course_code}: {self.grade}"
