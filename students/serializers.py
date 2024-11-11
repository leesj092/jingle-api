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
        user = self.context['request'].user

        if not hasattr(user, 'student_profile'):
            raise serializers.ValidationError("Authenticated user is not a student.")

        validated_data['student'] = user.student_profile
        return super().create(validated_data)
