from rest_framework import serializers
from .models import Student, Enrollment
from tutors.models import Tutor

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class EnrollmentSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'tutor', 'start_time', 'duration']

    def create(self, validated_data):
        # Ensure the authenticated user has a linked student profile
        student = self.context['request'].user.student

        # Add the student to the validated_data
        enrollment = Enrollment.objects.create(
            student=student,
            tutor=validated_data['tutor'],
            start_time=validated_data['start_time'],
            duration=validated_data['duration'],
        )
        return enrollment
