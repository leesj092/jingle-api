from rest_framework import serializers
from .models import Tutor, Availability

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'name']

class AvailabilitySerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all())

    class Meta:
        model = Availability
        fields = ['id', 'tutor', 'start_time', 'duration']
