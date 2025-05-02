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

    class Meta:
        model = Course
        fields = ('id', 'name', 'duration_months', 'monthly_price', 'teacher')


# LessonSchedule Serializer
class LessonScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonSchedule
        fields = '__all__'


# MonthlyTestResult Serializer
class MonthlyTestResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyTestResult
        fields = ('id', 'student', 'date', 'score', 'comment', 'course')


# MonthlyPayment Serializer
class MonthlyPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyPayment
        fields = ('id', 'student', 'month', 'amount', 'is_paid', 'payment_date', 'course')

from .models import CustomUser

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'status']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AssignCourseSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    course_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def validate(self, data):
        try:
            self.student = StudentProfile.objects.get(id=data['student_id'])
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("Student not found.")
        
        self.courses = Course.objects.filter(id__in=data['course_ids'])
        if not self.courses.exists():
            raise serializers.ValidationError("No valid courses found.")

        return data

    def save(self):
        self.student.courses.set(self.courses)
        return self.student

class ModifySingleCourseSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['add', 'remove'])

    def validate(self, data):
        try:
            self.student = StudentProfile.objects.get(id=data['student_id'])
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("Student not found.")
        
        try:
            self.course = Course.objects.get(id=data['course_id'])
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course not found.")
        
        return data

    def save(self):
        if self.validated_data['action'] == 'add':
            self.student.courses.add(self.course)
        else:  # 'remove'
            self.student.courses.remove(self.course)
        return self.student
    
import django_filters
from .models import LessonSchedule

class LessonScheduleFilter(django_filters.FilterSet):
    class Meta:
        model = LessonSchedule
        fields = {
            'course': ['exact'],
            'weekday': ['exact'],
            'time': ['exact', 'gte', 'lte'],
        }
        

class StudentNestedSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    test_results = MonthlyTestResultSerializer(many=True, read_only=True)
    payments = MonthlyPaymentSerializer(many=True, read_only=True)
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'phone', 'status', 'registered_at', 'courses', 'test_results', 'payments']
