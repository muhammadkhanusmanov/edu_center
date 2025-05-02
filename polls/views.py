from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions,generics, viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (CustomUserSerializer, UserCreateSerializer,CourseSerializer,AssignCourseSerializer,
ModifySingleCourseSerializer, LessonScheduleSerializer, StudentNestedSerializer, CourseSerializer,
LessonScheduleFilter,MonthlyTestResultSerializer,MonthlyPaymentSerializer)

from .models import CustomUser, Course,LessonSchedule,MonthlyTestResult, MonthlyPayment,StudentProfile, TeacherProfile

class LoginView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        user_data = CustomUserSerializer(user).data

        return Response({
            'token': token.key,
            'user': user_data
        }, status=status.HTTP_200_OK)


class CreateUserBase(APIView):
    permission_classes = [permissions.IsAdminUser]  # faqat admin yaratadi

    status_type = None  # bu har bir viewda alohida belgilanadi

    def post(self, request):
        data = request.data.copy()
        data['status'] = self.status_type
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user_id": user.id,
                "username": user.username,
                "status": user.status,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Har bir tur uchun alohida view
class CreateAdminView(CreateUserBase):
    status_type = 'admin'

class CreateTeacherView(CreateUserBase):
    status_type = 'teacher'

class CreateStudentView(CreateUserBase):
    status_type = 'student'
    

class LogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)
        
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status == 'admin'

class CourseCreateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseUpdateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({'message': 'Course deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


class AssignCoursesToStudentView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AssignCourseSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "message": "Courses assigned successfully.",
                "student": student.user.get_full_name(),
                "courses": [course.name for course in student.courses.all()]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ModifyStudentCourseView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]  # faqat admin foydalana oladi

    def post(self, request):
        serializer = ModifySingleCourseSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "message": f"Course successfully {serializer.validated_data['action']}ed.",
                "student": student.user.get_full_name(),
                "current_courses": [course.name for course in student.courses.all()]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LessonScheduleCreateView(generics.CreateAPIView):
    queryset = LessonSchedule.objects.all()
    serializer_class = LessonScheduleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


# Bitta jadvalni olish, tahrirlash va o'chirish
class LessonScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonSchedule.objects.all()
    serializer_class = LessonScheduleSerializer
    permission_classes = [permissions.AllowAny]
    

class LessonScheduleListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LessonSchedule.objects.all()
    serializer_class = LessonScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonScheduleFilter
    

from rest_framework.exceptions import PermissionDenied


class MonthlyTestResultListCreateView(generics.ListCreateAPIView):
    serializer_class = MonthlyTestResultSerializer

    def get_queryset(self):
        user = self.request.user

        if user.status == 'admin':
            return MonthlyTestResult.objects.all()

        elif user.status == 'teacher':
            teacher_courses = Course.objects.filter(teacher=user)
            student_ids = StudentProfile.objects.filter(courses__in=teacher_courses).values_list('id', flat=True)
            return MonthlyTestResult.objects.filter(student_id__in=student_ids).distinct()

        elif user.status == 'student':
            return MonthlyTestResult.objects.filter(student__user=user)

        return MonthlyTestResult.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        student = serializer.validated_data['student']

        if user.status == 'teacher':
            teacher_courses = Course.objects.filter(teacher=user)
            if not student.courses.filter(id__in=teacher_courses).exists():
                raise PermissionDenied("Siz bu student uchun baho qo‘ya olmaysiz.")
        elif user.status != 'admin':
            raise PermissionDenied("Faqat teacher yoki admin baho qo‘yishi mumkin.")

        serializer.save()


class MonthlyTestResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MonthlyTestResultSerializer

    def get_queryset(self):
        user = self.request.user

        if user.status == 'admin':
            return MonthlyTestResult.objects.all()

        elif user.status == 'teacher':
            teacher_courses = Course.objects.filter(teacher=user)
            student_ids = StudentProfile.objects.filter(courses__in=teacher_courses).values_list('id', flat=True)
            return MonthlyTestResult.objects.filter(student_id__in=student_ids).distinct()

        elif user.status == 'student':
            return MonthlyTestResult.objects.filter(student__user=user)

        return MonthlyTestResult.objects.none()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.status == 'admin':
            instance.delete()
        elif user.status == 'teacher':
            teacher_courses = Course.objects.filter(teacher=user)
            if not instance.student.courses.filter(id__in=teacher_courses).exists():
                raise PermissionDenied("Siz bu student uchun testni o‘chira olmaysiz.")
            instance.delete()
        else:
            raise PermissionDenied("Siz testni o‘chira olmaysiz.")
        
        
class MonthlyPaymentCreateView(generics.CreateAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer
    permission_classes = [IsAdminUser]


# List (barcha to'lovlar ro'yxati)
class MonthlyPaymentListView(generics.ListAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer
    permission_classes = [IsAdminUser]


# Retrieve (bitta to'lov)
class MonthlyPaymentDetailView(generics.RetrieveAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer
    permission_classes = [IsAdminUser]


# Update (to'lovni yangilash)
class MonthlyPaymentUpdateView(generics.UpdateAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer
    permission_classes = [IsAdminUser]


# Delete (to'lovni o'chirish)
class MonthlyPaymentDeleteView(generics.DestroyAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer
    permission_classes = [IsAdminUser]


class StudentDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.status == 'admin':
            students = StudentProfile.objects.all()
            courses = Course.objects.all()

        elif user.status == 'teacher':
            courses = Course.objects.filter(teacher=user)
            students = StudentProfile.objects.filter(courses__in=courses).distinct()

        elif user.status == 'student':
            try:
                students = [StudentProfile.objects.get(user=user)]
                courses = students[0].courses.all()
            except StudentProfile.DoesNotExist:
                return Response({"detail": "Student profile not found."}, status=404)

        else:
            return Response({"detail": "Unauthorized"}, status=403)

        return Response({
            "courses": CourseSerializer(courses, many=True).data,
            "students": StudentNestedSerializer(students, many=True).data
        })