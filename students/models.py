from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_average_score(self):
        """Calculate average score across all courses"""
        grades = self.grades.all()
        if not grades:
            return 0
        total = sum(grade.score for grade in grades)
        return round(total / len(grades), 2)

    def get_gpa(self):
        """Calculate GPA on a 7.0 scale (Australian system)"""
        grade_points = {
            'HD': 7.0,   # High Distinction (85-100)
            'D': 6.0,    # Distinction (75-84)
            'C': 5.0,    # Credit (65-74)
            'P': 4.0,    # Pass (50-64)
            'N': 0.0     # Fail (0-49)
        }
        grades = self.grades.all()
        if not grades:
            return 0
        total = sum(grade_points.get(grade.grade, 0) for grade in grades)
        return round(total / len(grades), 2)