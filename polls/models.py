from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# USER MODEL
class CustomUser(AbstractUser):
    USER_STATUS = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    status = models.CharField(max_length=10, choices=USER_STATUS)

    def __str__(self):
        return f"{self.username} ({self.status})"


# COURSE MODEL
class Course(models.Model):
    name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField()
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'status': 'teacher'})

    def __str__(self):
        return self.name


# STUDENT PROFILE MODEL
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'status': 'student'})
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=[('active', 'Aktiv'), ('inactive', 'Passiv')], default='active')
    registered_at = models.DateTimeField(default=timezone.now)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return f"{self.user.get_full_name()} - Student"


# TEACHER PROFILE
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'status': 'teacher'})
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Teacher"


# LESSON SCHEDULE
class LessonSchedule(models.Model):
    WEEKDAYS = (
        ('monday', 'Dushanba'),
        ('tuesday', 'Seshanba'),
        ('wednesday', 'Chorshanba'),
        ('thursday', 'Payshanba'),
        ('friday', 'Juma'),
        ('saturday', 'Shanba'),
        ('sunday', 'Yakshanba'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    time = models.TimeField()
    room = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course.name} - {self.weekday} at {self.time}"


# MONTHLY TEST RESULT
class MonthlyTestResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='test_results')
    date = models.DateField()
    score = models.PositiveIntegerField()
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date} - {self.score} ball"


# MONTHLY PAYMENT
class MonthlyPayment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payments')
    month = models.CharField(max_length=20)  # Masalan: "Aprel 2025"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.month} - {'To‘langan' if self.is_paid else 'To‘lanmagan'}"
