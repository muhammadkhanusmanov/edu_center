from django.contrib import admin
from .models import (
    CustomUser,
    StudentProfile,
    TeacherProfile,
    Course,
    LessonSchedule,
    MonthlyTestResult,
    MonthlyPayment
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status', 'is_active', 'is_staff')
    list_filter = ('status', 'is_active')
    search_fields = ('username', 'email')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'registered_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'monthly_price', 'teacher')
    search_fields = ('name',)
    list_filter = ('teacher',)


@admin.register(LessonSchedule)
class LessonScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'weekday', 'time', 'room')
    list_filter = ('weekday', 'course')


@admin.register(MonthlyTestResult)
class MonthlyTestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'score', 'comment')
    list_filter = ('date',)
    search_fields = ('student__user__username',)


@admin.register(MonthlyPayment)
class MonthlyPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'month', 'amount', 'is_paid', 'payment_date')
    list_filter = ('is_paid', 'month')
    search_fields = ('student__user__username',)
