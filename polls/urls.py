from django.urls import path
from .views import (LoginView,CreateAdminView, CreateTeacherView,ModifyStudentCourseView,LessonScheduleCreateView,LessonScheduleListView,LessonScheduleDetailView,
CreateStudentView, LogoutView, CourseCreateView, CourseUpdateView, MonthlyPaymentListView, MonthlyPaymentCreateView,MonthlyPaymentDetailView,MonthlyPaymentUpdateView,
CourseDeleteView, AssignCoursesToStudentView, MonthlyTestResultListCreateView, MonthlyTestResultDetailView, MonthlyPaymentDeleteView, StudentDataView)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('create-teacher/', CreateTeacherView.as_view(), name='create-teacher'),
    path('create-student/', CreateStudentView.as_view(), name='create-student'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('courses/create/', CourseCreateView.as_view(), name='create-course'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='update-course'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='delete-course'),
    path('assign-courses/', AssignCoursesToStudentView.as_view(), name='assign-courses'),
    path('admin/modify-student-course/', ModifyStudentCourseView.as_view(), name='modify-student-course'),
    path('schedules/', LessonScheduleListView.as_view(), name='schedule-list'),
    path('schedules/create/', LessonScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/<int:pk>/', LessonScheduleDetailView.as_view(), name='schedule-detail'),
    path('monthly-tests/', MonthlyTestResultListCreateView.as_view(), name='monthly-test-list-create'),
    path('monthly-tests/<int:pk>/', MonthlyTestResultDetailView.as_view(), name='monthly-test-detail'),
    path('payments/', MonthlyPaymentListView.as_view(), name='payment-list'),
    path('payments/create/', MonthlyPaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', MonthlyPaymentDetailView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/update/', MonthlyPaymentUpdateView.as_view(), name='payment-update'),
    path('payments/<int:pk>/delete/', MonthlyPaymentDeleteView.as_view(), name='payment-delete'),
    path('data/overview/', StudentDataView.as_view(), name='data-overview'),
]
    