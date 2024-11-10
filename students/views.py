from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Student, Enrollment
from .serializers import StudentSerializer, EnrollmentSerializer
from datetime import timedelta
from django.contrib.auth.models import User

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        student = serializer.validated_data['student']
        tutor = serializer.validated_data['tutor']
        start_time = serializer.validated_data['start_time']
        duration = serializer.validated_data['duration']
        end_time = start_time + timedelta(minutes=duration)

        # Check for overlapping enrollments for this student
        student_enrollments = Enrollment.objects.filter(student=student)
        for enrollment in student_enrollments:
            existing_start = enrollment.start_time
            existing_end = existing_start + timedelta(minutes=enrollment.duration)

            if start_time < existing_end and existing_start < end_time:
                raise ValidationError("You already have an overlapping enrollment.")

        # Check for tutor availability
        tutor_availabilities = Enrollment.objects.filter(tutor=tutor)
        for availability in tutor_availabilities:
            availability_start = availability.start_time
            availability_end = availability_start + timedelta(minutes=availability.duration)

            if start_time < availability_end and availability_start < end_time:
                raise ValidationError("Tutor is not available for this time slot.")

        # Save the enrollment
        serializer.save()

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

"""
API to register a new student user.
"""
class StudentRegistrationView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new user
        user = User.objects.create_user(username=username, password=password)

        # Create and link a student profile
        student = Student.objects.create(user=user)

        return Response(
            {
                "id": student.id,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )
