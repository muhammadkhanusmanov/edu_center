from rest_framework import serializers
from .models import (
    CustomUser,
    StudentProfile,
    TeacherProfile,
    Course,
    LessonSchedule,
    MonthlyTestResult,
    MonthlyPayment
)

# CustomUser Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'status', 'is_active', 'is_staff')


# StudentProfile Serializer
class StudentProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    courses = serializers.StringRelatedField(many=True)

    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'phone', 'status', 'registered_at', 'courses')


# TeacherProfile Serializer
class TeacherProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ('id', 'user', 'phone', 'bio')


# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'duration_months', 'monthly_price', 'teacher')


# LessonSchedule Serializer
class LessonScheduleSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = LessonSchedule
        fields = ('id', 'course', 'weekday', 'time', 'room')


# MonthlyTestResult Serializer
class MonthlyTestResultSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = MonthlyTestResult
        fields = ('id', 'student', 'date', 'score', 'comment')


# MonthlyPayment Serializer
class MonthlyPaymentSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = MonthlyPayment
        fields = ('id', 'student', 'month', 'amount', 'is_paid', 'payment_date')
