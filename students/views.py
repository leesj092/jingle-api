from rest_framework import generics
from .models import Student, Enrollment
from .serializers import StudentSerializer, EnrollmentSerializer
from datetime import timedelta
from rest_framework.exceptions import ValidationError

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
