from rest_framework import serializers
from .models import Student, Enrollment
from tutors.models import Tutor

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'tutor', 'start_time', 'duration']
