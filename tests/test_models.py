import pytest
from students.models import Student
from grades.models import Course, Grade


@pytest.mark.django_db
class TestStudentModel:
    def test_create_student(self):
        """Test creating a student"""
        student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            student_id="S001"
        )
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert str(student) == "John Doe"

    def test_student_gpa_no_grades(self):
        """Test GPA calculation with no grades"""
        student = Student.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            student_id="S002"
        )
        assert student.get_average_score() == 0
        assert student.get_gpa() == 0

    def test_student_gpa_with_hd(self):
        """Test GPA calculation with HD grade"""
        student = Student.objects.create(
            first_name="Bob",
            last_name="Johnson",
            email="bob@example.com",
            student_id="S003"
        )
        course = Course.objects.create(
            course_code="SIT223",
            course_name="Professional Practice",
            credits=1
        )
        Grade.objects.create(
            student=student,
            course=course,
            grade="HD",
            score=92.5
        )
        
        assert student.get_average_score() == 92.5
        assert student.get_gpa() == 7.0

    def test_student_gpa_multiple_grades(self):
        """Test GPA with multiple grades"""
        student = Student.objects.create(
            first_name="Alice",
            last_name="Williams",
            email="alice@example.com",
            student_id="S004"
        )
        course1 = Course.objects.create(
            course_code="SIT223",
            course_name="Professional Practice",
            credits=1
        )
        course2 = Course.objects.create(
            course_code="SIT753",
            course_name="Computer Security",
            credits=1
        )
        
        Grade.objects.create(student=student, course=course1, grade="HD", score=92.5)
        Grade.objects.create(student=student, course=course2, grade="D", score=78.0)
        
        assert student.get_average_score() == 85.25  # (92.5 + 78.0) / 2
        assert student.get_gpa() == 6.5  # (7.0 + 6.0) / 2


@pytest.mark.django_db
class TestGradeModel:
    def test_create_grade(self):
        """Test creating a grade"""
        student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            email="test@example.com",
            student_id="S005"
        )
        course = Course.objects.create(
            course_code="TEST101",
            course_name="Test Course",
            credits=3
        )
        grade = Grade.objects.create(
            student=student,
            course=course,
            grade="C",
            score=68.5
        )
        
        assert grade.score == 68.5
        assert grade.grade == "C"
        assert str(grade) == "Test Student - TEST101: C"